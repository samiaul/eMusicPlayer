
from lib.emp.network.ticket import Ticket


class ServerTicket(Ticket):

    def __init__(self, network_instance, id_: int, source_id: int, destination_id: int):

        Ticket.__init__(self, network_instance, id_, source_id, destination_id)