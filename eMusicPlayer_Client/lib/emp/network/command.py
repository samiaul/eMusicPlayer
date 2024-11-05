
from lib.emp.network.network import ClosedNetworkException

import typing
if typing.TYPE_CHECKING:
    from lib.emp.network import network as network_class


class NetworkCommand:

    def __init__(self,
                 network_manager: 'network_class.Network'):

        self.network_manager = network_manager

    def __call__(self, command, arg):

        if self.network_manager.state is False:
            raise ClosedNetworkException()

        try:
            getattr(self, command)(arg)

        except AttributeError as error:
            raise error

        except TypeError:
            pass
