#Imports
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal
from constants import BIG_SIZE, TEXT_MARGIN, MINIMUM_WIDTH, PRIMARY_COLOR
from utils import is_empty, is_numeric_or_dont

#Display Class 
class Display(QLineEdit):
    eq_pressed = Signal()
    del_pressed = Signal()
    clear_pressed = Signal()
    input_pressed = Signal(str)#-> Define o dado que precisa passar no Signal
    operator_pressed = Signal(str)#-> Define o dado que precisa passar no Signal
    #Definição dos Métodos
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config_style()

    #-> Configuração do Estilo 
    def config_style(self)-> None:
        #- Margin
        margin_text:list[int] = [TEXT_MARGIN for _ in range(4)]
        #- Style
        self.setStyleSheet(
            f"font-size: {BIG_SIZE}px; border-color: {PRIMARY_COLOR};"
            )
        #- MinimumHeight
        self.setMinimumHeight(BIG_SIZE*2)
        #- MinimumWidth
        self.setMinimumWidth(MINIMUM_WIDTH)
        #- Aligment
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        #- Add Margin
        self.setTextMargins(*margin_text)
        #- Set Read Only
        # self.setReadOnly(True)

    #-> Key Press Event
    def keyPressEvent(self, event: QKeyEvent) -> None:
        #- Definindo key
        key = event.key()
        #- Definindo text
        text = event.text()
        #- Definindo constante KEY
        KEY = Qt.Key
        #- Definindo verificadores de teclas
        is_enter = key in [KEY.Key_Enter, KEY.Key_Return]
        is_delete = key in [KEY.Key_Backspace, KEY.Key_Delete, KEY.Key_D]
        is_esc = key in [KEY.Key_Escape, KEY.Key_C]
        is_operator = key in [
            KEY.Key_Plus,KEY.Key_Minus, KEY.Key_Slash, KEY.Key_X, KEY.Key_P
            ]
        #- Filtros de verificação
        if is_enter or text == "=":
            #- Emite o sinal de eq_pressed
            self.eq_pressed.emit()
            return event.ignore()
        
        elif is_delete or text.lower() == "d":
            #- Emite o sinal de del_pressed
            self.del_pressed.emit()
            return event.ignore()
        
        elif is_esc or text.lower() == "c":
            #- Emite o sinal de clear_pressed
            self.clear_pressed.emit()
            return event.ignore()
        
        elif is_operator or text ==  "+-/xp":
            #- Verifica se text é (p)otencial
            if text.lower() == "p":
                text = "^"
            #- Emite o sinal de operator_pressed
            self.operator_pressed.emit(text)
            return event.ignore()
        
        #- Verifica se o text está vazio
        elif is_empty(text):
            return event.ignore()
        
        #- Verifica se o text é número ou ponto
        elif is_numeric_or_dont(text):
            self.input_pressed.emit(text)
            return event.ignore()