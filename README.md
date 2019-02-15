# Idle Music Player

Music player focused on autoplay functionality

# Dependencies

* [Python 3.7+](https://www.python.org/)
* [aiofiles](https://pypi.org/project/aiofiles/)
* [aiohttp](https://pypi.org/project/aiohttp/)
* [pafy](https://pypi.org/project/pafy/)
* [python-vlc](https://pypi.org/project/python-vlc/)
* [aiodns](https://pypi.org/project/aiodns/) (optional, speeds up DNS resolution)
* [cchardet](https://pypi.org/project/cchardet/) (optional, speeds up character encoding detection)
* [pytaglib](https://pypi.org/project/pytaglib/) (optional, used to extract metadata from audio files not downloaded from YouTube)
* [youtube-dl](https://pypi.org/project/youtube_dl/) (optional, but highly recommended, used as a pafy backend)

To install all dependencies, run `pip install -r requirements.txt`.  
Required dependencies will be automatically installed if using pip as described in the next section.

# Installing

To install as a module:

    python3 setup.py install

You should be able to run Idle using `idlemp` or `python3 -m idlemp`.

Note: it can also be executed without installing with `python3 idlemp.py`.

# Running

Several command line arguments can be passed to `idlemp`.  
You can see a list of them by running `idlemp --help`.

Idle stores its downloaded audio files and its configuration files in the same directory.
The path to this directory is controlled by the `library_path` command line argument (by default, it's the current directory).

Logs are writtten to the `log.txt` file.  
Music information is stored in the `library.json` file.  
The autoplay schedule is read from the `schedule.json` file. See the `schedule.json.example` file for how to configure it.  
If present, the file specified by the `--urllist` argument, which should contain a list of URLs to musics (separated by newlines), will be used to download musics automatically.  
This file will be read periodically and downloaded URLs will be deleted.

---

Copyright © 2019 Joaquim Monteiro

Idle Music Player is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Idle Music Player is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Idle Music Player.  If not, see <https://www.gnu.org/licenses/>.
