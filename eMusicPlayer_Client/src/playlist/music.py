
from src.funcs import get_file_name


class Music:

    __doc__ = """
    Stores data of a 'music' type audio file
    """

    def __init__(self, filepath):

        self.filepath = filepath

        self.name = get_file_name(filepath)
