from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from constants import SMALL_SIZE

class InfoResult(QLabel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config_style()
        
    #-> Configuração do Estilo Padrão
    def config_style(self) -> None:
        #- Style
        self.setStyleSheet(f"font-size: {SMALL_SIZE}px")
        #- Aligment
        self.setAlignment(Qt.AlignmentFlag.AlignRight)