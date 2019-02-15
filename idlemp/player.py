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

import vlc

logger = logging.getLogger(__name__)
SLEEP_DELAY = 3
INITIAL_WAIT = 5


class Player:
    def __init__(self):
        self.vlc_instance = vlc.Instance()
        if self.vlc_instance is None:
            raise Exception('Failed to initialize VLC instance')

        self.mediaplayer = vlc.MediaPlayer(self.vlc_instance)
        if self.mediaplayer is None:
            raise Exception('Failed to initialize VLC MediaPlayer')

    async def play(self, path: str):
        logger.info(f'Playing file {path}')

        media = self.mediaplayer.set_mrl(path)
        if media is None:
            logger.error(f'Failed to get Media for {path}')
            return

        result = self.mediaplayer.play()
        if result == -1:
            logger.error(
                f'Failed to play {path}: MediaPlayer.play() returned -1')
            return

        # We need to wait because it doesn't start playing immediately
        await asyncio.sleep(INITIAL_WAIT)
        while self.mediaplayer.is_playing():
            await asyncio.sleep(SLEEP_DELAY)

        logger.info(f'Finished playing file {path}')
