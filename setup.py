#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(name='IdleMusicPlayer',
                 version='1.0',
                 author='Joaquim Monteiro',
                 author_email='joaquim.monteiro@protonmail.com',
                 license='GPLv3+',
                 description='Music player focused on autoplay functionality',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 url='https://github.com/gmes78/IdleMusicPlayer',
                 packages=['idlemp'],
                 entry_points={
                     'console_scripts': ['idlemp = idlemp.__main__']},
                 python_requires='>=3.7',
                 install_requires=['aiofiles>=0.4', 'aiohttp>=3.5.4',
                                   'pafy>=0.5.4', 'python-vlc>=3.0.4106'],
                 extras_require={
                     'taglib': ['pytaglib>=1.4.4'],
                     'aiohttp_recommends': ['aiodns>=1.2', 'cchardet>=2.1.4'],
                     'youtube_dl': ['youtube_dl>=2019.2.8'],
                 })
