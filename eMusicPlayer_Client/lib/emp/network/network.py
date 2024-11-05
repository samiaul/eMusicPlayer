
from lib.managers.thread import Thread
from lib.emp.network.network_instance import NetworkInstance

from src.funcs import get_public_ip

from socket import gethostname, gethostbyname, timeout as socket_timeout
from string import ascii_lowercase, digits
from random import randint, choices, shuffle

import typing
if typing.TYPE_CHECKING:
    from socket import socket as socket_class
    from src import main_manager as main_manager_class


class ClosedNetworkException(Exception):
    pass


def receive(socket: socket_class, buff: int, trials_count=5):

    for trials in range(5):

        try:
            packet = socket.recv(buff)

        except socket_timeout:
            continue

        except ConnectionAbortedError as error:
            pass
            raise error

        else:
            return packet

    else:
        raise socket_timeout()


class Network(Thread):

    __doc__ = """
    Manage networking :
        - Data I/O
        - Files I/O
        - Commands I/O
    """

    verification_code = '20200611'
    port = 15555
    ping_delay = 6e1
    ping_max_trials = 3

    manager: 'main_manager_class.MainManager'

    network_instance_class = NetworkInstance
    command_class = None

    def __init__(self,
                 main_manager: 'main_manager_class.MainManager'):

        Thread.__init__(self, main_manager)

        self.network_instance = None
        self.command = self.command_class(self)

        self.default_hostname = gethostname()
        self.hostname = None

        self.default_password = self.gen_password()
        self.password = None

        self.host_address = get_public_ip()
        # self.host_address = gethostbyname(self.default_hostname)

        self.state = False

    # Infos

    @staticmethod
    def gen_password(length=8):
        """Return a randomized password composed of lowercase letters and digits"""

        chars_count = randint(1, length-1)
        digits_count = length - chars_count

        chars_list = choices(population=ascii_lowercase, k=chars_count)
        digits_list = choices(population=digits, k=digits_count)

        password_list = chars_list + digits_list

        shuffle(password_list)

        password = ''.join(password_list)

        return password

    def get_hostname(self):
        return self.get_default_hostname(self.hostname)

    def set_hostname(self, hostname):
        self.hostname = hostname

    def get_default_hostname(self, hostname):
        return self.default_hostname if hostname is None else hostname

    def get_password(self):
        return self.get_default_password(self.password)

    def set_password(self, password):
        self.password = password

    def get_default_password(self, password):
        return self.default_password if password is None else password

    def open(self):

        if self.state:
            raise Exception("Network already opened")

        self.network_instance = self.network_instance_class(self)
        self.network_instance.start()

        self.state = True

    def close(self):

        if not self.state:
            raise Exception("Network already closed")

        self.network_instance.close()
        self.network_instance.join()
        self.network_instance = None

        self.state = False
