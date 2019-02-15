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

import datetime
import json


class Interval:
    def __init__(self, start: datetime.time, end: datetime.time):
        if end > start:
            self.start = start
            self.end = end
        else:
            raise ValueError('start time can\'t be larger than end time')

    def contains(self, time: datetime.time):
        return self.start < time < self.end


class AutoplayController:
    def __init__(self, __intervals=None):
        self.always_play = __intervals is None
        self.intervals = __intervals

    def should_play(self):
        if self.always_play:
            return True

        now = datetime.datetime.now()
        time = now.time()
        for interval in self.intervals[now.weekday()]:
            if interval.contains(time):
                return True

        return False

    def time_left(self):
        if self.always_play:
            return datetime.timedelta.max

        now = datetime.datetime.now()
        time = now.time()
        eligible_intervals = [i for i in self.intervals[now.weekday()] if
                              i.contains(time)]

        end = None
        for interval in eligible_intervals:
            if end is None or interval.end > end:
                end = interval.end

        if end is None:
            return datetime.timedelta()

        return datetime.datetime.combine(datetime.date.today(), end) - now

    @staticmethod
    def from_json(json_data):
        data = json.loads(json_data)
        intervals = {}
        for day in range(0, 7):
            intervals[day] = [Interval(datetime.time.fromisoformat(i[0]),
                                       datetime.time.fromisoformat(i[1])) for i
                              in data[str(day)]]
        return AutoplayController(intervals)
