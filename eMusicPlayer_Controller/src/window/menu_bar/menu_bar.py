
from src.window.menu_bar.menu_widget import MenuWidget
from src.window.menu_bar.menu_menu import MenuMenu
from src.window.menu_bar.help_menu import HelpMenu

import typing
if typing.TYPE_CHECKING:
    import src.window.window_manager as window_manager_class


class MenuBar(MenuWidget):

    def __init__(self,
                 master: 'window_manager_class.WindowManager'):

        MenuWidget.__init__(self,
                            master,
                            top_menu=True)

        self.menu_menu = self.add_cascade(name='menu',
                                          text='Menu',
                                          icon=False,
                                          menu=MenuMenu(master=self))

        self.help_menu = self.add_cascade(name='help',
                                          text='Help',
                                          icon=False,
                                          menu=HelpMenu(master=self))
