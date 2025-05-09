#Imports
import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from constants import WINDOW_ICON
from components.main_window import MainWindow
from components.display import Display
from components.info_result import InfoResult
from style_theme import setup_theme
from components.buttons import GridButtons


if __name__ == "__main__":

    #Criação da aplicação
    app = QApplication(sys.argv)

    #Adicionando Style no app
    setup_theme(app)
    window = MainWindow()
    icon = QIcon(str(WINDOW_ICON))

    #Adicionando Ícone
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    #Info Result
    info_result = InfoResult()
    window.add_widget_vlayout(info_result)

    #Display
    display = Display()
    window.add_widget_vlayout(display)

    #GridButton
    buttons_grid = GridButtons(display, info_result, window)
    window.add_layout(buttons_grid)

    #Ajuste na GUI - Interface Gráfica do Usuário
    window.adjust_fixed_size()

    #Exercução da aplicação
    window.show()
    app.exec()