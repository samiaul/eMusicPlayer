
from lib.emp.network.codec import Codec
from lib.emp.network.network import receive

import threading
import socket as socket_module

import typing
if typing.TYPE_CHECKING:
    from src.network import server_network_instance as server_network_instance_class


class ClientInstance(threading.Thread):

    def __init__(self,
                 network_instance: 'server_network_instance_class.ServerNetworkInstance',
                 socket: socket_module.socket,
                 address,
                 id_: int):

        threading.Thread.__init__(self)

        self.network_instance = network_instance

        self.socket = socket
        self.ip, self.port = address
        self.id_ = id_

        self.state = False

    def run(self):

        self.state = True

        self.loop()

        self.quit()

    def loop(self):

        while self.state:
            self.update()

    def update(self):

        self.receive(Codec.command_byte_length)

    def stop(self):

        self.state = False

    def quit(self):
        pass

    def receive(self, buff):

        self.network_instance.reception_queue.append((self, receive(self.socket, buff)))

