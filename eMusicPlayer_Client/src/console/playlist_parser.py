
from lib.console.manager_parser import ManagerParser
from lib.console import type_parser, parser as parser_class

import typing
if typing.TYPE_CHECKING:
    pass


class PlaylistParser(ManagerParser):

    name = 'playlist'
    doc = "Controls the playlist calendar. "

    def __init__(self,
                 parser: 'parser_class.Parser'):

        ManagerParser.__init__(self,
                               parser)

    def cmd_get(self):

        name_list = self.parser.console_manager.main_manager.playlist_manager.playlist.get_name_list()

        self.parser.console_manager.prompt('\n'.join(name_list))

    @type_parser.set_args(state=type_parser.Boolean())
    def cmd_set_random_mode(self, state):
        """Tell if playlist random mode is on"""

        self.parser.console_manager.main_manager.playlist_manager.playlist.random_mode = state

    def cmd_get_random_mode(self):

        self.parser.console_manager.prompt(
            f"playlist random_mode = {self.parser.console_manager.main_manager.playlist_manager.playlist.random_mode}")

    @type_parser.set_args(state=type_parser.Boolean())
    def cmd_set_loop_mode(self, state):
        """Tell if playlist loop mode is on"""

        self.parser.console_manager.main_manager.playlist_manager.playlist.loop_mode = state

    def cmd_get_loop_mode(self):

        self.parser.console_manager.prompt(
            f"playlist loop_mode = {self.parser.console_manager.main_manager.playlist_manager.playlist.loop_mode}")

    @type_parser.set_args(filepath=type_parser.Filepath())
    def cmd_open_folder(self, filepath):
        """Add all music files in a folder to playlist"""
        self.parser.console_manager.main_manager.playlist_manager.playlist.open_folder(filepath)
