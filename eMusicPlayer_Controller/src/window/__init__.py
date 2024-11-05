
import tkinter as tk

import typing


def get_state(state):
    return tk.NORMAL if state else tk.DISABLED


def get_root(widget: tk.Misc):

    from src.window.window_manager import WindowManager

    return widget if isinstance(widget, WindowManager) else get_root(widget.master)


def get_icon(widget: 'tk.Misc',
             name: str,
             icon: typing.Union[str, bool] = None,
             factor: int = 8):

    return get_root(widget).get_icon(name=(name if icon is None else icon),
                                     factor=factor) if icon is not False else None
