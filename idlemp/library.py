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

import json
import random

import aiofiles


class MusicInfo:
    def __init__(self, title: str, length: int, file_name: str, url: str):
        self.title = title
        self.length = length
        self.file_name = file_name
        self.url = url


class MusicInfoEncoder(json.JSONEncoder):
    def default(self, o: MusicInfo):
        return {'title': o.title, 'length': o.length, 'file_name': o.file_name,
                'url': o.url}


class MusicLibrary:
    def __init__(self, musics: [MusicInfo] = []):
        self.musics = musics

    def add(self, music: MusicInfo):
        self.musics.append(music)

    def get(self, video_id: str):
        for music in self.musics:
            if music.id == video_id:
                return music

    def get_random(self):
        return random.choice(self.musics)

    def get_random_with_max_len(self, max_length: int):
        eligible_musics = [m for m in self.musics if m.length <= max_length]
        return random.choice(eligible_musics)

    def into_json(self, pretty=True):
        if pretty:
            return MusicInfoEncoder(indent=4).encode(self.musics)
        else:
            return MusicInfoEncoder().encode(self.musics)

    async def write_to_file(self, path):
        json_data = self.into_json()
        async with aiofiles.open(path, 'w') as file:
            await file.write(json_data)

    @staticmethod
    def from_json(json_data):
        data = json.loads(json_data)
        musics = [
            MusicInfo(o['title'], o['length'], o['file_name'], o['url'])
            for o in data]
        return MusicLibrary(musics)
