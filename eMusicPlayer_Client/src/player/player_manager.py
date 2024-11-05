from lib.managers.thread import Thread

from pygame import mixer

import typing
if typing.TYPE_CHECKING:
    from src import main_manager as main_manager_class


class PlayerManager(Thread):

    __doc__ = """
    Manage audio streaming :
        - Play / Pause / Stop
        - Volume
        - Duration
        - Effects (Fading)
    """

    main_manager: 'main_manager_class.MainManager'

    def __init__(self,
                 main_manager: 'main_manager_class.MainManager'):

        Thread.__init__(self, main_manager=main_manager)

        mixer.init()

        self.play_state = False
        self.pause_state = False

    def update(self):

        Thread.update(self)

        if self.play_state:

            if not self.pause_state:

                if not mixer.music.get_busy():
                    self.next_music()

    def next_music(self):
        """Start streaming next music"""

        self.log("Next music")

        self.main_manager.playlist_manager.playlist.next()

        if self.main_manager.playlist_manager.playlist.current is None:
            self.stop_music()
        else:
            self.start_music()

    def previous_music(self):
        """Start streaming previous music"""

        self.log("Previous music")

        self.main_manager.playlist_manager.playlist.previous()

        self.start_music()

    def start_music(self):
        """Load and play current music"""

        self.log(f"Playing: '{self.main_manager.playlist_manager.playlist.get_current().name}'")

        if not self.play_state:
            self.play_state = True

        if self.pause_state:
            self.pause_state = False

        mixer.music.load(self.main_manager.playlist_manager.playlist.get_current().filepath)

        mixer.music.play()

    def stop_music(self):
        """Stop streaming and clear playlist queue"""

        self.log("Stopped streaming")

        self.play_state = False
        self.pause_state = False
        self.main_manager.playlist_manager.playlist.clear_playlist()

        mixer.music.stop()

    def pause_music(self):
        """Pause streaming"""

        self.log("Paused streaming")

        self.pause_state = True

        mixer.music.pause()

    def play_music(self):
        """Start / unpause streaming"""

        self.log("Start streaming")

        if not self.play_state:

            self.play_state = True

            if self.main_manager.playlist_manager.playlist.current is None:
                self.next_music()
            else:
                self.start_music()

        elif self.pause_state:
            self.pause_state = False
            mixer.music.unpause()

    def begin(self):
        """Begin streaming"""

        if not self.play_state or self.pause_state:

            self.play_music()

    def end(self):
        """End streaming"""

        if self.play_state and not self.pause_state:

            self.pause_music()

    def quit(self):

        self.log("Quitting...")

        mixer.stop()
        mixer.quit()