
import typing
from math import log10
import pickle


class Codec:

    byteorder = 'big'
    ticket_byte_length = 1
    com_byte_length = 1
    arg_byte_length = 2

    com_str_length = int(log10(2 ** (8 * com_byte_length))) + 1

    UnpicklingError = pickle.UnpicklingError

    command_byte_length = ticket_byte_length + com_byte_length + arg_byte_length

    @classmethod
    def encode_command(cls, ticket_id: int, com_code: str, arg: int) -> bytes:
        return cls.encode_ticket(ticket_id) + cls.encode_comcode(com_code) + cls.encode_arg(arg)

    @classmethod
    def decode_command(cls, packet: bytes) -> typing.Tuple[int, str, int]:
        return (
            cls.get_ticket(packet),
            cls.get_comcode(packet),
            cls.get_arg(packet))

    @classmethod
    def encode_ticket(cls, ticket_id: int) -> bytes:
        return ticket_id.to_bytes(cls.ticket_byte_length, cls.byteorder)

    @classmethod
    def get_ticket(cls, packet: bytes):
        return cls.decode_ticket(packet[0:cls.ticket_byte_length])

    @classmethod
    def decode_ticket(cls, ticket_id: bytes) -> int:
        return int.from_bytes(ticket_id, cls.byteorder)

    @classmethod
    def encode_comcode(cls, com_code: str) -> bytes:
        return int(com_code).to_bytes(cls.com_byte_length, cls.byteorder)

    @classmethod
    def get_comcode(cls, packet: bytes):
        return cls.decode_comcode(packet[cls.ticket_byte_length:cls.ticket_byte_length + cls.com_byte_length])

    @classmethod
    def decode_comcode(cls, com_code: bytes) -> str:
        return str(int.from_bytes(com_code, cls.byteorder)).zfill(cls.com_str_length)

    @classmethod
    def encode_arg(cls, arg: int) -> bytes:
        return arg.to_bytes(cls.arg_byte_length, cls.byteorder)

    @classmethod
    def get_arg(cls, packet: bytes) -> int:
        return cls.decode_arg(packet[cls.ticket_byte_length + cls.com_byte_length:])

    @classmethod
    def decode_arg(cls, arg: bytes) -> int:
        return int.from_bytes(arg, cls.byteorder)

    @classmethod
    def encode_datas(cls, datas) -> bytes:
        return pickle.dumps(datas)

    @classmethod
    def decode_datas(cls, packet: bytes):
        return pickle.loads(packet)