
from src.playlist.playlist import Playlist
from lib.managers.manager import Manager

import typing
if typing.TYPE_CHECKING:
    from src import main_manager as main_manager_class


class PlaylistManager(Manager):

    __doc__ = """
    Manage sounds datas :
        - Playlists
        - Adverts
        - Top-Of-The-Hours
    """

    def __init__(self,
                 main_manager: 'main_manager_class.Main'):

        Manager.__init__(self, main_manager)

        self.playlist = Playlist()

    def quit(self):

        self.log("Quitting...")