
from src.window.button_bar_widget import ButtonBarWidget
from src.window.tools_panel.player_tab.volume_scale import VolumeScale

import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.tools_panel.player_tab.player_tab as player_tab_class


class ControlBar(ButtonBarWidget):

    master: 'player_tab_class.PlayerTab'

    def __init__(self,
                 master: 'player_tab_class.PlayerTab'):

        ButtonBarWidget.__init__(self,
                                 master)

        self['bd'] = 2
        self['relief'] = tk.GROOVE

        self.add_radiobutton(name='play',
                             text='Play',
                             command=self.play,
                             variable='state',
                             value=1)

        self.add_radiobutton(name='pause',
                             text='Pause',
                             command=self.pause,
                             variable='state',
                             value=2)

        self.add_button(name='stop',
                        text='Stop',
                        command=self.stop)

        self.add_separator()

        self.add_button(name='previous',
                        text='Previous',
                        command=self.previous_song)

        self.add_button(name='next',
                        text='Next',
                        command=self.next_song)

        self.add_separator()

        self.add_checkbutton(name='loop',
                             text='Loop',
                             command=lambda: self.loop(self.vars['loop'].get()))

        self.add_checkbutton(name='random',
                             text='Random',
                             command=lambda: self.random(self.vars['random'].get()))

        self.volume_scale = VolumeScale(self)

        self.set_state(False)

        self.pack(fill=tk.X)

    def set_state(self, state):

        self.update_lock()

        self.set_button_state('loop', state)
        self.set_button_state('random', state)

        # self.volume_scale.set_state(state)

    def play(self, forced=False):

        self.set_var('state', 1)
        self.button_pressed(forced)

    def pause(self, forced=False):

        self.set_var('state', 2)
        self.button_pressed(forced)

    def stop(self, forced=False):

        self.set_var('state', 0)

        self.buttons['loop'].deselect()
        self.buttons['random'].deselect()

        # self.master.progress_bar_frame.set_position()
        # self.master.progress_bar_frame.set_duration()

        self.button_pressed(forced)

    def previous_song(self):

        if self.get_var('state') == 2:
            self.buttons['play'].invoke()

        else:
            self.button_pressed()

    def next_song(self):

        if self.get_var('state') == 2:
            self.buttons['play'].invoke()

        else:
            self.button_pressed()

    def loop(self, state):
        pass
        # self.master.master.menu_bar.loop_var.set(state)

    def random(self, state):
        pass
        # self.master.master.menu_bar.random_var.set(state)

    def update_lock(self):

        pass
        """
        if not self.master.playlist_frame.playlist:
            state = False

        elif (self.main.settings_manager.schedule.player_lock.action(2) == 2 and
              not self.main.schedule_manager.pause_state):
            state = False

        elif self.main.network_manager.state_is(False):
            state = False

        else:
            state = True

        self.set_button_state('play', state)
        self.set_button_state('pause', state)
        self.set_button_state('stop', state)
        self.set_button_state('previous', state)
        self.set_button_state('next', state)
        """

    def button_pressed(self, forced=False):

        pass
        """
        self.master.playlist_frame.update_visual()

        if self.main.settings_manager.schedule.player_lock.action(2) and not forced:
            self.main.io_manager.commands('schedule_pause', True)
        """