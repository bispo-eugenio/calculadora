#Imports 
from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, 
                               QWidget, QLayout, QMessageBox)

#Classe MainWindow
class MainWindow(QMainWindow):

    #Definição de Métodos
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        #-> Título
        self.setWindowTitle("Calculadora")

        #-> Configuração básica do Layout
        self.central_widgets: QWidget = QWidget()
        self.layout_v_box: QVBoxLayout = QVBoxLayout()
        self.central_widgets.setLayout(self.layout_v_box)
        self.setCentralWidget(self.central_widgets)

    #-> Ajuste da GUI
    def adjust_fixed_size(self) -> None:
        #- AdjustSize
        self.adjustSize()
        #- FixedSize
        self.setFixedSize(self.width(), self.height())
        return

    #-> Adiciona widget
    def add_widget_vlayout(self, widget: QWidget) -> None:
        #- addWidget
        self.layout_v_box.addWidget(widget)
        return
    #-> Adiciona Layout
    def add_layout(self, layout: QLayout) -> None:
        #- addLayout
        self.layout_v_box.addLayout(layout)
        return
    
    #-> Make Message Box
    def make_message_box(self) -> QMessageBox:
        return QMessageBox(self)