
from lib.emp.network.codec import Codec
from lib.emp.network.ticket import Ticket

from src.funcs import filter_1

import threading
import socket as socket_module
from time import monotonic, sleep

import typing
if typing.TYPE_CHECKING:
    from lib.emp.network import network as network_class


class NetworkInstance(threading.Thread):

    __doc__ = """
    Socket instance for transferring commands and datas between clients and controllers
    """

    def __init__(self,
                 network_manager: 'network_class.Network'):

        threading.Thread.__init__(self)

        self.network_manager = network_manager

        self.socket = socket_module.socket(socket_module.AF_INET, socket_module.SOCK_STREAM)
        self.socket.settimeout(1)

        self.tickets: typing.Set[Ticket] = set()

        self.state = False
        self.closed = False

        self.ping_state = False
        self.ping_time = 0
        self.ping_last = monotonic()
        self.ping_trials = 0

        self.socket = socket_module.socket(socket_module.AF_INET, socket_module.SOCK_STREAM)
        self.socket.settimeout(1)

    def run(self):
        """Called when the thread is started"""

        self.state = True

        self.loop()

        self.quit()

    def loop(self):
        """Calls update each loop while state is True"""

        while self.state:
            self.update()

    def update(self):
        """Called each loop while state is True"""

        self.receive()

    def stop(self):
        """Stops the thread loop"""

        self.state = False

    def quit(self):
        """Called after the loop is stopped"""

        self.closed = True

    def get_ticket(self, id_: int):
        """Return the ticket with corresponding id"""

        return filter_1(lambda t: t.id_ == id_, self.tickets)

    def receive(self):
        """Check for any message received by client and start decoding them"""
        pass

    @staticmethod
    def decode(packet):
        """Called when a message is received.
        Transfers it to corresponding ticket or create one if needed"""

        if packet == b'':
            pass  # TODO ERROR

        elif packet is None:
            pass

        else:

            try:
                ticket_id = Codec.get_ticket(packet)

            except TypeError:
                pass  # TODO ERROR

            else:
                return ticket_id

    def ticket_command(self, ticket_id: int, packet: bytes, *args, **kwargs):
        """Transfer a message to the corresponding ticket or create one"""
        pass

    def new_ticket(self, packet: bytes, *args, **kwargs):
        """Creates a new ticket"""
        pass