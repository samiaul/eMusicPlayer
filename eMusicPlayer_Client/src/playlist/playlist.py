
from src.funcs import filter_1
from src.playlist.music import Music

from os import listdir
from random import randint

import typing


class Playlist:

    __doc__ = """
    Stores music files, data & info
    """

    def __init__(self):

        self.musics: typing.List[Music] = list()
        self.queue: typing.List[str] = list()

        self.loop_mode = False
        self.random_mode = False

        self.current: typing.Optional[str] = None
        self.previous_list: typing.List[str] = list()

    def clear(self):
        """Clear playlist"""

        self.musics.clear()
        self.clear_playlist()

    def clear_playlist(self):

        self.current = None
        self.queue.clear()
        self.previous_list.clear()

    def open_folder(self, filepath):
        """Loads all music from a folder and set playlist"""

        files = listdir(filepath)

        path_list = filter(lambda file: file.endswith('.mp3'), files)

        self.open_path_list([f"{filepath}\\{file}" for file in path_list])

    def open_path_list(self, path_list):
        """Loads musics from a path list and set playlist"""
        if path_list:
            self.set_playlist([Music(filepath) for filepath in path_list])

    def get_music(self, name: str) -> Music:
        """Return the music file from its name"""
        return filter_1(lambda music: music.name == name, self.musics)

    def get_current(self):
        if self.current is not None:
            return self.get_music(self.current)

    def get_path_list(self):
        """Return a list of songs path"""
        return [music.filepath for music in self.musics]

    def get_name_list(self):
        """Return a list of songs names"""
        return [music.name for music in self.musics]

    def set_playlist(self, music_list):

        self.clear()

        self.musics = [music for music in music_list]
        self.queue = self.get_name_list()

    def next(self):

        # Add current to previous list
        if self.current is not None:
            self.previous_list.append(self.current)

        # Verify if end of playlist
        if not self.queue:

            if self.loop_mode:
                self.loop()

            else:
                self.current = None
                return

        # Pick next song
        if self.random_mode:
            index = randint(0, len(self.queue)-1)
        else:
            index = 0

        self.current = self.queue.pop(index)

    def previous(self):

        # TODO REWIND

        if self.previous_list:
            self.queue.insert(0, self.current)
            self.current = self.previous_list.pop(-1)

    def loop(self):

        self.clear_playlist()
        self.queue = self.get_name_list()
