# -*- coding: utf-8 -*-
#   Copyright © 2019 Joaquim Monteiro
#
#   This file is part of Idle Music Player.
#
#   Idle Music Player is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Idle Music Player is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Idle Music Player.  If not, see <https://www.gnu.org/licenses/>

import asyncio
import logging
import pathlib
import urllib.parse

import aiofiles
import aiohttp
import vlc

try:
    import taglib
except ImportError:
    taglib = None

from .library import MusicInfo, MusicLibrary
from . import youtube

CHUNK_SIZE = 131072  # 128KiB
SLEEP_DELAY = 60
YOUTUBE = ['youtube.com', 'www.youtube.com', 'm.youtube.com',
           'gaming.youtube.com', 'youtu.be', 'www.youtu.be']

logger = logging.getLogger(__name__)


async def download_file(session: aiohttp.ClientSession, url: str,
                        file_path: pathlib.Path):
    logger.info(f'Downloading {url}')
    async with session.get(url) as resp:
        logger.info(f'Opening file {file_path}')
        async with aiofiles.open(file_path, 'wb') as file:
            while True:
                chunk = await resp.content.read(CHUNK_SIZE)
                if not chunk:
                    break
                await file.write(chunk)

    logger.info(f'Finished downloading {url}')


async def download(session: aiohttp.ClientSession, url: str,
                   download_dir: pathlib.Path):
    parsedurl = urllib.parse.urlsplit(url)
    if parsedurl.netloc in YOUTUBE:
        # YouTube download

        # Get info and stream link from YouTube
        stream_url, info = youtube.get_stream(url)
        if stream_url is None:
            logger.error(f'No stream found for {url}')
            return

        # Download
        await download_file(session, stream_url,
                            download_dir.joinpath(info.file_name))
    else:
        # Generic download

        # Try to get file name
        file_name = None
        async with session.head(url, allow_redirects=True) as resp:
            if resp.content_disposition is not None:
                file_name = resp.content_disposition.filename

        if file_name is None:
            file_name = pathlib.PurePosixPath(parsedurl.path).name

        file_path = download_dir.joinpath(file_name)

        # Download
        await download_file(session, url, file_path)

        # Try to get title and length
        title = ''
        length = None
        if taglib is not None:
            tags = taglib.File(file_path).tags
            if 'TITLE' in tags:
                title = tags['TITLE'][0]
            if 'LENGTH' in tags:
                length = int(tags['LENGTH'][0])

        if length is None:
            vlc_instance = vlc.Instance()
            if vlc_instance is not None:
                media = vlc_instance.media_new(str(file_path))
                media_length = media.get_duration()

                # -1 length indicates an error
                if media_length != -1:
                    # Convert from milliseconds to seconds
                    length = int(media_length / 1000)

        if length is None:
            # Give up, assign the maximum length that's played when
            # AutoplayController's always_play is True
            length = 4294967294
            logger.warning(f'Failed to get length for {file_name}.')

        info = MusicInfo(title, length, file_name, url)

    return info


async def download_task(download_path: pathlib.Path,
                        url_list_file: pathlib.Path, library: MusicLibrary,
                        library_file: pathlib.Path):
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        while True:
            try:
                # Get next URL to download
                with url_list_file.open('r', encoding='utf-8') as file:
                    url = file.readline()

                # If there's nothing to download, wait
                if url.strip() == '':
                    await asyncio.sleep(SLEEP_DELAY)
                    continue

                # Download and get information
                music = await download(session, url.strip(), download_path)

                sync_task = None

                if music is not None:
                    # Add to library if download was successful
                    library.add(music)

                    logger.info(f'Added music from {url} to the library')

                    # Sync the changes to the library file
                    sync_task = asyncio.create_task(
                        library.write_to_file(library_file))

                # Remove used URL from list
                async with aiofiles.open(url_list_file, 'r+',
                                         encoding='utf-8') as file:
                    content = await file.readlines()
                    await file.seek(0)
                    for line in content:
                        if line != url:
                            await file.write(line)
                    await file.truncate()

                if sync_task is not None:
                    await asyncio.wait_for(sync_task, timeout=None)
            except asyncio.CancelledError:
                logger.info('Ending download task')
                raise
            except Exception as e:
                logger.error(f'Exception occured while downloading: {e}')
