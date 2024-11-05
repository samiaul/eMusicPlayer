
from string import ascii_lowercase, ascii_uppercase, digits

import typing
if typing.TYPE_CHECKING:

    NumType = typing.Union[int, float]
    RangeType = typing.Tuple[NumType, NumType]


class ParseException(Exception):
    """Base class for parsing exception"""

    def __init__(self,
                 msg: str):

        self.msg = msg

        Exception.__init__(self, msg)


class InvalidArgumentException(ParseException):
    """Base class for invalid argument"""

    def __init__(self,
                 arg,
                 err: str,
                 desc: str):

        self.arg = arg
        self.desc = desc

        ParseException.__init__(self, f"*** Invalid argument {err} ({self.desc}): '{self.arg}'")


class MissingArgumentException(InvalidArgumentException):

    def __init__(self, name):

        self.name = name

        InvalidArgumentException.__init__(self,
                                          arg=name,
                                          err='count',
                                          desc="Missing argument")


class TooManyArgumentsException(InvalidArgumentException):

    def __init__(self,
                 arg):

        InvalidArgumentException.__init__(self,
                                          arg,
                                          err='count',
                                          desc="Too many argument")


class InvalidTypeException(InvalidArgumentException):
    """Inappropriate argument type"""

    def __init__(self,
                 arg,
                 type_: str):

        InvalidArgumentException.__init__(self,
                                          arg,
                                          err='type',
                                          desc=f"must be {type_}")

        self.type = type_


class InvalidValueException(InvalidArgumentException):
    """Inappropriate argument value"""

    def __init__(self,
                 arg,
                 desc: str):

        InvalidArgumentException.__init__(self,
                                          arg,
                                          err='value',
                                          desc=desc)


class OutOfRangeException(InvalidValueException):
    """Argument is not in required ranged"""

    def __init__(self,
                 arg,
                 range_: 'RangeType'):

        InvalidValueException.__init__(self,
                                       arg,
                                       desc=f"must be in range [{self.range[0], self.range[1]}]")

        self.range = range_


class Type:
    """Default class for parse type"""

    basetype = False

    def __init__(self,
                 default=False):

        self.default = default

        self.doc = self.get_doc()

    def get_doc(self,
                cls: type = None,
                arguments: str = None):

        return (self.__class__ if cls is None else cls).__name__ + \
               ("" if arguments is None else f"[{arguments}]") + \
               ("" if self.default is False else f"={self.default}")

    def parse(self, arg):
        return arg

    def raise_invalid_type(self, arg):

        raise InvalidTypeException(arg, self.__class__.__name__)


class RangedType(Type):
    """Any numeric type between two number"""

    basetype = True

    def __init__(self,
                 minimum: int,
                 maximum: int,
                 default=False):

        self.minimum = minimum
        self.maximum = maximum

        Type.__init__(self, default)

    def get_doc(self, *args, **kwargs):

        name = tuple(filter(lambda cls: issubclass(cls, Type) and not cls.basetype, self.__class__.__mro__))[0]
        arguments = f"{self.minimum};{self.maximum}"

        return Type.get_doc(self, name, arguments)

    def parse(self, arg):

        if self.minimum <= arg <= self.maximum:
            return arg

        else:
            raise OutOfRangeException(arg, (self.minimum, self.maximum))


class Boolean(Type):
    """Only accept the strings 'true' or 'false'"""

    def __init__(self,
                 default=False):

        Type.__init__(self, default)

    def parse(self, arg: str):

        if arg == 'true':
            return True

        elif arg == 'false':
            return False

        else:
            self.raise_invalid_type(arg)


class Integer(Type):
    """Any integer number (1, -33, ...)"""

    def parse(self, arg):

        if arg[0] == "-":
            t = arg[1:]
        else:
            t = arg

        if t.isnumeric():
            return int(arg)

        else:
            self.raise_invalid_type(arg)


class RangedInteger(RangedType, Integer):
    """Any integer between a minimum and maximum"""

    def __init__(self,
                 minimum: int,
                 maximum: int,
                 default=False):

        super().__init__(minimum=minimum,
                         maximum=maximum,
                         default=default)

    def parse(self, arg):

        return RangedType.parse(self,
                                Integer.parse(self, arg))


def verify_filter(whitelist, blacklist):
    for char in whitelist:
        if char in blacklist:
            return False
    return True


class String(Type):
    """Any string"""

    def __init__(self,
                 default=False,
                 whitelist: str = None,
                 blacklist: str = None):

        super().__init__(default=default)

        whitelist = [] if whitelist is None else whitelist
        blacklist = [] if blacklist is None else blacklist

        if not verify_filter(whitelist, blacklist):
            raise ValueError("Can't have identical character in both whitelist and blacklist")

        self.whitelist = whitelist
        self.blacklist = blacklist

    def parse(self, arg):

        for char in arg:

            if char not in self.whitelist:
                raise InvalidValueException(char, "Character not in whitelist")

            if char in self.blacklist:
                raise InvalidValueException(char, "Character in blacklist")

        return arg


class Filepath(String):
    """A string with only characters : letters, numbers, spaces, and ( ) _ - , . : / \\ """

    allow_chars = ascii_lowercase + ascii_uppercase + digits + ' ()_-,.:\\/'

    def __init__(self,
                 default=False):

        super().__init__(
            default=default,
            whitelist=self.allow_chars)

    def parse(self, arg):

        return String.parse(self, arg)


def verify_defaults(type_kwargs):

    default = False
    for name, value in type_kwargs.items():
        if value.default is False:
            if default:
                raise SyntaxError(f"non-default argument follows default argument : '{name}'")
        else:
            default = True


def parse_args(type_kwargs, args):

    cmd_kwargs = {}
    i = 0
    for i, (name, type_) in enumerate(type_kwargs.items()):

        if i >= len(args):

            if type_.default is not False:
                value = type_.default
            else:
                raise MissingArgumentException(name)

        else:
            value = type_.parse(args[i])

        cmd_kwargs[name] = value

    if len(args) > len(type_kwargs):
        raise TooManyArgumentsException(args[i+1])

    return cmd_kwargs


def get_syntax(name: str,
               type_kwargs: typing.Dict[str, Type]):

    arguments = ' '.join([f"[{name} ({type_.doc})]" for name, type_ in type_kwargs.items()])
    return f"\nsyntax: {name.removeprefix('cmd_')} {arguments}"


def set_args(**type_kwargs: Type):
    """Define command arguments types (and names)"""

    verify_defaults(type_kwargs)

    def wrapper(func):

        def command(self, *args):

            func(self, **parse_args(type_kwargs, args))

        command.__name__ = func.__name__
        command.__doc__ = func.__doc__ + get_syntax(func.__name__, type_kwargs)
        return command

    return wrapper
