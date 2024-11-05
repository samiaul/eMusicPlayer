
from lib.managers.manager import Manager

import json
from os import listdir, mkdir

import typing
if typing.TYPE_CHECKING:
    from src import main_manager as main_manager_class


class InvalidSessionException(Exception):

    def __init__(self, reason):
        Exception.__init__(self, reason)


class SessionNotFoundException(Exception):

    def __init__(self, session_name):
        Exception.__init__(self, f"Can't find session '{session_name}'")


class SessionManager(Manager):

    __doc__ = """
    Manage session datas :
        - Settings
        - Playlists
        - Schedules
    """

    main_manager: 'main_manager_class.MainManager'

    def __init__(self,
                 main_manager: 'main_manager_class.MainManager'):

        Manager.__init__(self, main_manager)

        self.session_name: typing.Optional[str] = None
        self.session_path: typing.Optional[str] = None
        self.last_session: typing.Optional[str] = None
        self.adverts: typing.Optional[dict] = None

        self.available_sessions = self.get_available_sessions()

    def load(self):

        self.load_session()

    @staticmethod
    def open_session(directory_name):

        try:
            with open(f"sessions/{directory_name}/session.json", 'r') as file:
                return json.load(file)

        except FileNotFoundError:
            raise InvalidSessionException("session.json not found")

        except json.decoder.JSONDecodeError as error:
            raise InvalidSessionException(f"invalid json format ({error.args[0]})")

    def save_session(self,
                     path: str,
                     name: str,
                     is_last=True):

        with open(f"sessions/{path}/session.json", 'w') as file:
            json.dump(self.encode(name, is_last), file)

        # self.log(f"Saving session : {self.name}")

    def get_available_sessions(self) -> typing.Dict[str, str]:

        available_sessions = dict()

        try:
            directory_list = listdir('sessions')

        except FileNotFoundError:
            mkdir('sessions')
            directory_list = list()

        for directory_name in directory_list:

            try:
                session_datas = self.open_session(directory_name)

            except InvalidSessionException as error:
                self.log(f"Invalid session '{directory_name}' : {error}", is_error=True)

            else:

                if session_datas['last'] and not directory_name == "last":
                    self.last_session = session_datas['name']

                available_sessions[session_datas['name']] = directory_name

        return available_sessions

    def load_session(self, session_name=None):

        if session_name is None:
            if self.last_session is not None:
                session_name = self.last_session
            else:
                session_name = 'Last'

        try:
            directory_name = self.available_sessions[session_name]
        except KeyError:
            raise SessionNotFoundException(session_name)

        # self.adverts = self.load_adverts(self.dir_name)

        try:
            self.decode(self.open_session(directory_name))

        except Exception as error:
            self.log(f"Session load error : {error}", is_error=True)

        else:
            self.log(f"Loading session : {session_name}")

        self.session_name = session_name
        self.session_path = directory_name

    def decode(self, datas):

        # Schedule
        schedule = datas.get('schedule', {})
        #   Calendar
        self.main_manager.schedule_manager.calendar.decode(schedule.get('calendar', []))

        #   Exceptions
        self.main_manager.schedule_manager.decode_exceptions(schedule.get('exceptions', []))
        """

        #   Advertising
        self.main_manager.window.schedule_panel.get_frame(2).set(schedule.get('advertising'))
        """

        # Network
        network = datas.get('network', {})
        """
        self.main_manager.network_manager.update_hostname(network.get('name'))
        self.main_manager.network_manager.update_password(network.get('password'))
        self.main_manager.network_manager.update_server_address(network.get('address'))
        """

        # Playlist
        playlist = datas.get('playlist', {})

        self.main_manager.playlist_manager.playlist.open_path_list(playlist.get('pathlist'))

    def encode(self,
               session_name: str,
               is_last=True):

        datas = dict()

        datas['name'] = session_name
        datas['last'] = is_last

        # Schedule
        datas['schedule'] = dict()

        #   Calendar
        datas['schedule']['calendar'] = self.main_manager.schedule_manager.calendar.encode()

        #   Exceptions
        datas['schedule']['exceptions'] = self.main_manager.schedule_manager.encode_exceptions()

        #   Advertising
        datas['schedule']['advertising'] = list()
        """
        for advert in self.main_manager.window.schedule_panel.get_frame(2).adverts:
            datas['schedule']['advertising'].append(advert.schedule.get_values())
        """

        # Network
        datas['network'] = dict()
        """
        datas['network']['name'] = self.main_manager.network_manager.get_hostname()
        datas['network']['password'] = self.main_manager.network_manager.get_password()
        datas['network']['address'] = self.main_manager.network_manager.get_server_address()
        """

        # Playlist
        datas['playlist'] = dict()

        datas['playlist']['pathlist'] = self.main_manager.playlist_manager.playlist.get_path_list()

        return datas

    def quit(self):

        self.save_session(self.session_path, self.session_name)