
import typing
if typing.TYPE_CHECKING:
    from lib.emp.network import network_instance as network_instance_class
    import lib as socket_module


class Ticket:

    def __init__(self,
                 network_instance: 'network_instance_class.NetworkInstance',
                 id_: int,
                 source_id: int,
                 destination_id: int):

        self.network_instance = network_instance

        self.id_ = id_

        self.source_id = None
        self.destination_id = None

    def command(self, *args, **kwargs):
        pass