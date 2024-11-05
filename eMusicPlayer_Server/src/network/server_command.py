
from lib.emp.network.command import NetworkCommand

import typing

if typing.TYPE_CHECKING:
    from src.network import network_manager as network_manager_class


class ServerCommand(NetworkCommand):

    def __init__(self,
                 network_manager: 'network_manager_class.NetworkManager'):

        NetworkCommand.__init__(self, network_manager)

    def test(self):
        pass