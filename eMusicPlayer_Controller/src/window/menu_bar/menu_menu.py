

from src.window.menu_bar.menu_widget import MenuWidget
from src.window import get_root


class MenuMenu(MenuWidget):

    def __init__(self, master):

        MenuWidget.__init__(self, master=master)

        self.add_command(name='settings',
                         text='Settings',
                         command=None)

        self.add_separator()

        self.add_command(name='exit',
                         text='Exit',
                         command=get_root(self).main_manager.stop)
