
from src.window import get_state, get_icon
from src.funcs import each

import tkinter as tk

import typing
if typing.TYPE_CHECKING:
    import src.window.window_manager as window_manager_class


def test_arguments(func_name, name, text, max_arg, args, kwargs):

    if name is ...:
        raise TypeError(f"{func_name}() missing 1 required positional argument: 'name'")
    if text is ...:
        raise TypeError(f"{func_name}() missing 1 required positional argument: 'text'")
    if args:
        raise TypeError(f"{func_name}() takes from 2 to {max_arg} positional arguments but "
                        f"{max_arg+len(args)} were given")
    if kwargs:
        raise TypeError(f"{func_name}() got an unexpected keyword argument '{[*kwargs.keys()][0]}'")


class MenuWidget(tk.Menu):

    master: typing.Union['MenuWidget', 'window_manager_class.WindowManager']

    def __init__(self,
                 master: typing.Union['MenuWidget', 'window_manager_class.WindowManager'],
                 top_menu=False):

        tk.Menu.__init__(self, master=master)

        self.items: typing.List[typing.Union[str, None]] = list()
        self.variables: typing.Dict[str, tk.BooleanVar] = dict()

        self.top_menu = top_menu

        if self.top_menu:
            self.master['menu'] = self

    def add_cascade(self,
                    name: str = ...,
                    text: str = ...,
                    icon: typing.Union[str, bool] = None,
                    menu: 'MenuWidget' = None,
                    state=True,
                    *args,
                    **kwargs) -> 'MenuWidget':

        test_arguments('add_cascade', name, text, 5, args, kwargs)

        menu = MenuWidget(self) if menu is None else menu

        tk.Menu.add_cascade(self,
                            label=str(text),
                            menu=menu,
                            image=get_icon(self, name, icon, 10),
                            compound=tk.LEFT,
                            state=get_state(state))

        self.items.append(name)

        return menu

    def add_command(self,
                    name: str = ...,
                    text: str = ...,
                    command: typing.Callable = None,
                    icon: typing.Union[str, bool] = None,
                    state=True,
                    popup=False,
                    *args,
                    **kwargs):

        test_arguments('add_command', name, text, 6, args, kwargs)

        tk.Menu.add_command(self,
                            label=f"{text}{'...' if popup else ''}",
                            command=command,
                            image=get_icon(self, name, icon, 10),
                            compound=tk.LEFT,
                            state=get_state(state))

        self.items.append(name)

    def add_checkbutton(self,
                        name: str = ...,
                        text: str = ...,
                        command: typing.Callable = None,
                        state=True,
                        variable: typing.Union[str, bool] = False,
                        default_value=False,
                        *args,
                        **kwargs):

        test_arguments('add_checkbutton', name, text, 6, args, kwargs)

        if variable:
            self.variables[name] = tk.BooleanVar(self)
            self.variables[name].set(default_value)

        tk.Menu.add_checkbutton(self,
                                label=str(text),
                                variable=self.variables[str(name)] if variable else None,
                                onvalue=True,
                                offvalue=False,
                                command=command,
                                state=get_state(state))

        self.items.append(name)

    def add_separator(self, *args, **kwargs):

        tk.Menu.add_separator(self)

        self.items.append(None)

    def get_var(self,
                name: str):

        return self.variables[name].get()

    def set_var(self,
                name: str,
                value):

        return self.variables[name].set(value)

    def get_index(self,
                  name: str):

        return self.items.index(name)

    def set_button_state(self,
                         name: str,
                         state: bool):

        self.entryconfigure(index=self.get_index(name), state=get_state(state))

    def set_all_state(self,
                      state: bool):

        each(lambda name: self.set_button_state(name, state) if name is not None else None, tuple(self.items))
