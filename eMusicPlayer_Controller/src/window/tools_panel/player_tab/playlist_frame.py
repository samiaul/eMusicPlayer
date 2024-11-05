
import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.tools_panel.player_tab.player_tab as player_tab_class


class PlaylistFrame(tk.Frame):

    master: 'player_tab_class.PlayerTab'

    def __init__(self,
                 master: 'player_tab_class.PlayerTab'):

        tk.Frame.__init__(self,
                          master)

        self.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)

        self.playlist: typing.Tuple[str] = tuple()
        self.previous: typing.Tuple[str] = tuple()
        self.current: typing.Optional[int] = None
        self.state = False

        self.listbox = tk.Listbox(self,
                                  selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(fill=tk.Y, expand=True)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.bind('<<ListboxSelect>>', lambda event: self.set_current(int(event.widget.curselection()[0])
                                                                      if event.widget.curselection()
                                                                      else None))

        self.set_playlist(tuple([f"music_{i}" for i in range(100)]))  # TODO DEBUG

        self.set_state(False)

    def set_playlist(self, playlist=tuple()):

        self.playlist = playlist

        self.listbox.delete(0, tk.END)

        for name in self.playlist:
            self.listbox.insert(tk.END, name)

        self.current = None
        self.previous = tuple()

        self.update_visual()

        self.set_state(bool(self.playlist))

    def set_current(self, index=None):

        self.current = index

        self.update_visual()

    def set_previous(self, previous=tuple()):

        self.previous = previous

        self.update_visual()

    def update_visual(self):

        for index in range(len(self.playlist)):

            if index in self.previous:
                self.listbox.itemconfig(index, background='grey', foreground='black')
            elif index is self.current:
                self.listbox.itemconfig(self.current, background='grey25', foreground='dodger blue')
            elif not self.state:
                self.listbox.itemconfig(index, background='grey', foreground='grey25')
            else:
                self.listbox.itemconfig(index, background='white', foreground='black')

    def set_state(self, state):

        self.state = state

        if state:
            self['bg'] = "white"
        else:
            self['bg'] = "grey75"

        self.update_visual()
