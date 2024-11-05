
from lib.emp.network.network_instance import NetworkInstance
from lib.emp.network.codec import Codec

from src.funcs import filter_1
from src.network.client_instance import ClientInstance
from src.network.server_ticket import ServerTicket

import socket as socket_module

import typing
if typing.TYPE_CHECKING:
    from src.network import network_manager as network_manager_class


class ServerNetworkInstance(NetworkInstance):

    def __init__(self,
                 network_manager: 'network_manager_class.NetworkManager'):

        NetworkInstance.__init__(self, network_manager)

        self.socket.setsockopt(socket_module.SOL_SOCKET, socket_module.SO_REUSEADDR, 1)
        self.socket.bind(('', self.network_manager.port))

        self.clients_sockets: typing.Set[ClientInstance] = set()

        self.reception_queue: typing.List[typing.Tuple[ClientInstance, typing.Any]] = list()

        self.clients_ids: typing.Dict[int, str] = dict()

    def gen_ticket_id(self):
        """Return the smallest integer (>0) not used as ticket id"""

        used_ids = list(map(lambda t: t.id_, self.tickets))

        i = 1
        for i, e in enumerate(sorted(used_ids) + [None], 1):
            if i != e:
                break

        if i > 255:
            raise ValueError("No id available !")

        return i

    def gen_client_id(self):
        """Return a unique id, increasing by one"""

        return max(list(self.clients_ids.keys()) + [0]) + 1

    def get_client_by_id(self, id_: int):

        return filter_1(lambda c: c.id_ == id_, self.clients_sockets)

    def update(self):

        self.listen()

        NetworkInstance.update(self)

    def listen(self):

        try:
            client_datas = self.socket.accept()

        except socket_module.timeout:
            pass

        except OSError as error:
            self.network_manager.log(f"{error}", is_error=True)

        else:

            self.connect(*client_datas)

    def connect(self, socket: socket_module.socket, address):

        client_instance = ClientInstance(self,
                                         socket,
                                         address,
                                         self.gen_client_id())

        self.clients_sockets.add(client_instance)

        client_instance.start()

    def receive(self):

        reception_queue = self.reception_queue.copy()
        self.reception_queue.clear()

        for client, packet in reception_queue:
            ticket_id = self.decode(packet)
            self.ticket_command(ticket_id, packet, sender=client)

    def ticket_command(self, ticket_id: int, packet: bytes, sender: ClientInstance = None, *args, **kwargs):

        if ticket_id == 0:
            self.new_ticket(packet, sender)

        else:
            self.get_ticket(ticket_id).command(packet, sender)

    def new_ticket(self, packet: bytes, sender: ClientInstance = None, *args, **kwargs):

        ticket_id = self.gen_ticket_id()

        destination_id = Codec.decode_arg(packet)

        ticket = ServerTicket(self, ticket_id, sender.id_, destination_id)

        self.tickets.add(ticket)
