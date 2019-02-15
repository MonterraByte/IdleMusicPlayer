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

import logging

try:
    import youtube_dl
except ImportError:
    # Use the Pafy backend instead
    import os
    os.environ['PAFY_BACKEND'] = 'internal'

import pafy

from .library import MusicInfo

CHUNK_SIZE = 131072  # 128KiB
SLEEP_DELAY = 60

logger = logging.getLogger(__name__)


def get_stream(url: str):
    try:
        video = pafy.new(url)
    except Exception as e:
        logger.error(f'Failed to get video info: {e}')
        return

    stream = video.getbestaudio(ftypestrict=False)
    if stream is None:
        logger.error(f'Video {video.videoid} does not have any audio streams')
        return

    file_name = video.videoid + '.' + stream.extension
    return stream.url, MusicInfo(video.title, video.length, file_name, url)
