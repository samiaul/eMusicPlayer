
from lib.emp.network.network import Network

from src.network.server_network_instance import ServerNetworkInstance
from src.network.server_command import ServerCommand

import typing
if typing.TYPE_CHECKING:
    from src import main_manager as main_manager_class


class NetworkManager(Network):

    __doc__ = """
    Manage server networking :
        - Data I/O
        - Files I/O
        - Commands I/O
    """

    network_instance_class = ServerNetworkInstance
    command_class = ServerCommand

    def __init__(self,
                 main_manager: 'main_manager_class.MainManager'):

        Network.__init__(self, main_manager)
