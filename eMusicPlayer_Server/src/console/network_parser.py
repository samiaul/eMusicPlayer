
from lib.console.manager_parser import ManagerParser
from lib.console import type_parser

import typing
if typing.TYPE_CHECKING:
    from lib.console import parser as parser_class


class NetworkParser(ManagerParser):

    name = 'network'
    doc = "Controls the network"

    def __init__(self,
                 parser: 'parser_class.Parser'):

        ManagerParser.__init__(self,
                               parser)