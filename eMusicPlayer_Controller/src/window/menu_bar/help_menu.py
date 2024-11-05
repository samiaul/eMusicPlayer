
from src.window.menu_bar.menu_widget import MenuWidget
from src.window import get_root


class HelpMenu(MenuWidget):

    def __init__(self, master):

        MenuWidget.__init__(self, master=master)

        self.add_command(name='about',
                         text='About',
                         command=None,
                         popup=True)  # TODO
