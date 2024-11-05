
from src.window import get_root, get_state

import tkinter as tk
from idlelib.tooltip import Hovertip


import typing
if typing.TYPE_CHECKING:
    import src.window.tools_panel.player_tab.control_frame as control_frame_class


class VolumeScale(tk.Frame):

    master: 'control_frame_class.ControlBar'

    def __init__(self,
                 master: 'control_frame_class.ControlBar'):

        tk.Frame.__init__(self, master=master)

        self.last_volume = None
        self.volume_var = tk.IntVar(self)

        self.scale = tk.Scale(master=self,
                              orient=tk.HORIZONTAL,
                              showvalue=False,
                              command=self.set_volume,
                              variable=self.volume_var)
        self.scale.pack(side=tk.LEFT)

        self.text_var = tk.StringVar(master=self)

        self.button = tk.Button(master=self,
                                relief=tk.FLAT,
                                command=self.mute,
                                bd=0)
        self.button.pack(side=tk.LEFT)

        Hovertip(anchor_widget=self.button,
                 text='Mute',
                 hover_delay=500)

        self.label = tk.Label(master=self,
                              textvariable=self.text_var)
        self.label.pack(side=tk.LEFT)

        self.set_volume(25)

        self.pack(anchor=tk.N, side=tk.RIGHT)

    def set_volume(self, value):

        self.last_volume = self.volume_var.get()

        self.volume_var.set(value)

        self.text_var.set(f"{value}%")

        self.update_button_image()

    def mute(self):

        if self.volume_var.get() == 0:
            self.set_volume(self.last_volume)
            # self.master.master.master.menu_bar.mute_var.set(False)
        else:
            self.set_volume(0)
            # self.master.master.master.menu_bar.mute_var.set(True)

    def set_state(self, state):

        self.scale['state'] = get_state(state)
        self.button['state'] = get_state(state)
        self.label['state'] = get_state(state)

        self.update_button_image()

    def update_button_image(self):

        if self.button['state'] == tk.DISABLED:
            self.button.config(image=get_root(self).get_icon('no_volume'))
        elif self.volume_var.get() == 0:
            self.button.config(image=get_root(self).get_icon('mute'))
        elif self.volume_var.get() <= 50:
            self.button.config(image=get_root(self).get_icon('low_volume'))
        elif self.volume_var.get() < 100:
            self.button.config(image=get_root(self).get_icon('medium_volume'))
        elif self.volume_var.get() == 100:
            self.button.config(image=get_root(self).get_icon('full_volume'))
