
from lib.emp.network.network import Network

from src.network.client_network_instance import ClientNetworkInstance
from src.network.client_command import ClientCommand

import typing
if typing.TYPE_CHECKING:
    from src import main_manager as main_manager_class


class NetworkManager(Network):

    __doc__ = """
    Manage client networking :
        - Data I/O
        - Files I
        - Commands I
    """

    network_instance_class = ClientNetworkInstance
    command_class = ClientCommand

    def __init__(self,
                 main_manager: 'main_manager_class.MainManager'):

        Network.__init__(self, main_manager)

        self.default_server_address = 'localhost'
        self.server_address = None

    def get_server_address(self):
        return self.get_default_server_address(self.server_address)

    def set_server_address(self, server_address):
        self.server_address = server_address

    def get_default_server_address(self, server_address):
        return self.default_server_address if server_address is None else server_address

