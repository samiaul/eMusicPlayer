
from lib.emp.network.network_instance import NetworkInstance
from lib.emp.network.codec import Codec
from lib.emp.network.network import receive

from src.network.client_ticket import ClientTicket

from socket import timeout as socket_timeout

import typing
if typing.TYPE_CHECKING:
    from src.network import network_manager as network_manager_class


class ClientNetworkInstance(NetworkInstance):

    __doc__ = """
    Socket instance for receiving commands and (or sending) datas to server.
    """

    connection_max_trials = float('inf')

    network_manager: 'network_manager_class.NetworkManager'

    def __init__(self,
                 network_manager: 'network_manager_class.NetworkManager'):

        NetworkInstance.__init__(self, network_manager)

        self.connected = False
        self.connection_trial = 0

    def update(self):

        if not self.connected:
            self.connect()

        NetworkInstance.update(self)

    def connect(self):
        """Try to establish connection with server"""

        if self.connection_trial > self.connection_max_trials:

            self.stop()

        self.connection_trial += 1

        try:
            self.socket.connect((self.network_manager.get_server_address(), self.network_manager.port))

        except socket_timeout:
            pass

        except OSError as error:

            if error.errno == 10022:
                pass

            else:
                pass #TODO

        else:
            self.connected = True

    def receive(self):

        if self.connected:
            try:
                packet = receive(self.socket, Codec.command_byte_length)

            except socket_timeout:
                pass

            else:
                ticket_id = self.decode(packet)

    def ticket_command(self, ticket_id: int, packet: bytes, *args, **kwargs):

        if ticket_id == 0:
            self.new_ticket(packet)

        else:
            self.get_ticket(ticket_id).command(packet)

    def new_ticket(self, packet, *args, **kwargs):

        ticket = ClientTicket(self, packet)

        self.tickets.add(ticket)
