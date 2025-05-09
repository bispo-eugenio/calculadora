#Imports
from PySide6.QtWidgets import QPushButton, QGridLayout, QMessageBox
from PySide6.QtCore import Slot, Qt
from constants import MEDIUM_SIZE
from utils import is_valid_number, is_numeric_or_dont
from typing import TYPE_CHECKING
from math import pow

#-> Verificando Type Checking
if TYPE_CHECKING:
    from display import Display
    from info_result import InfoResult
    from main_window import MainWindow

#Button Class
class Button(QPushButton):
    #Definição de Métodos
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_style()
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    #-> Configuração do Estilo
    def config_style(self):
        #- Variável font
        font = self.font()
        #- Definindo Tamanho da font
        font.setPixelSize(MEDIUM_SIZE)
        #- SetFont
        self.setFont(font)
        #- Definindo Tamanho Mínimo da Fonte
        self.setMinimumSize(75,75)

#GridButtons Class
class GridButtons(QGridLayout):
    #Definição dos Métodos
    def __init__(self,display: "Display", info: "InfoResult", 
                 window: "MainWindow", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        #- Grid Mask
        self._grid_mask = [
             ['C', '◀', '^', '/'],
             ['7', '8', '9', 'x'],
             ['4', '5', '6', '-'],
             ['1', '2', '3', '+'],
             ['+/-',  '0', '.', '='],
         ]
        #-> Display
        self.display = display
        #-> Info
        self.info = info
        #-> Main Window
        self.window = window
        #-> Equation
        self._equation = ""
        #-> Equation Initial Value
        self._equation_initial_value = ""
        #-> Equation Getter e Setter
        self.equation = self._equation_initial_value
        #-> Left Number
        self. _left = None
        #-> Right Number
        self. _right = None
        #-> Operator
        self._operator = None
        #-> Make Grid
        self._make_grid()
    #-> Equation (property)
    @property
    def equation(self) -> str | None:
        return self._equation
    #-> Equation (setter)
    @equation.setter
    def equation(self, value) -> any:
        self._equation = value
        self.info.setText(value)
        return self._equation
    
    #-> Make Grid
    def _make_grid(self) -> None:
        #- Conectando as teclas com os slots
        self.display.eq_pressed.connect(self._eq)
        self.display.del_pressed.connect(self._backspace)
        self.display.clear_pressed.connect(self._clear)
        self.display.input_pressed.connect(self._insert_display)
        self.display.operator_pressed.connect(self._insert_operator)

        #- Lógica para Pegar linha e texto do _grid_mask
        for index_row, row in enumerate(self._grid_mask):
            for index_text, button_text in enumerate(row):

                #- Definindo Variável Button
                button = Button(button_text)

                #- Filtro de Botões Especiais
                if not is_numeric_or_dont(button_text) or button_text == "+/-":
                    #- Adicionando Estilo nos Botões Numéricos
                    button.setProperty("cssClass", "specialButton")
                    #- Configura os Botões Especiais
                    self._config_special_button(button)
                
                #- Adicionando os Botões
                self.addWidget(button, index_row, index_text)

                #- Coloca um Slot no botão
                slot = self._make_slot(self._insert_display, button_text)
                self._connect_button_clicked(button, slot)

    #-> Connect Button Clicked
    def _connect_button_clicked(self, button, slot) -> None:
        button.clicked.connect(slot)
        return

    #-> Config Special Button
    def _config_special_button(self, button) -> None:
        #- Verifica se os botões são especiais 
        #- para emitir slots diferentes
        text = button.text()
        if text == "C":
            self._connect_button_clicked(button, self._clear)
        if text in "+-/x^":
            self._connect_button_clicked(
                button, self._make_slot(self._insert_operator, text))
        if text == "=":
            self._connect_button_clicked(
                button, self._eq)
        if text == "◀":
            self._connect_button_clicked(button, self._backspace)
        if text == "+/-":
            self._connect_button_clicked(button, self._invert_number)

    #-> Make Slot
    def _make_slot(self, method, *args, **kwargs) -> any:
        #- Fabrica os slots
        @Slot()
        def insert_slot():
            method(*args, **kwargs)
            return
        return insert_slot

    #-> Insert Text Display
    @Slot()
    def _insert_display(self, text) -> None:
        #- Insere o texto dentro do display
        display_text = self.display.text() + text
        #- Verifica se não é número
        if not is_valid_number(display_text):
            return
        self.display.insert(text)
        return

    #-> Clear
    @Slot()
    def _clear(self) -> None:
        #- Left Number
        self. _left = None
        #- Right Number
        self. _right = None
        #- Operator
        self._operator = None
        #- Equation
        self.equation = self._equation_initial_value
        #- Limpa o display
        self.display.clear()
        return
    #-> Backspace
    @Slot()
    def _backspace(self) -> None:
        self.display.backspace()
        return
    #-> Invert Number
    @Slot()
    def _invert_number(self) -> None:
        display_text = self.display.text()
        if is_valid_number(display_text):
            if float(display_text) < 0:
                self.display.setText(display_text.replace("-", ""))
                return
            display_text = f"-{display_text}"
            self.display.setText(display_text)
            return
    
    #-> Operator Clicked
    def _insert_operator(self, text) -> None: #- operadores (+,-,/,x...)
        #- número da esquerda
        display_text = self.display.text()
        #- limpa o terminal
        self.display.clear()

        #- Verifica se clicou sem número na esquerda
        #- Caso verdade, faz nada
        if not is_valid_number(display_text) and self._left is None:
            self._show_information("Digite algum valor")
            return
            
        #- Se houver algum número na esquerda, adiciona ao número da esquerda
        #- e aguarda o número da direita
        if self._left is None: #type:ignore
            self._left = float(display_text)

        #- Adiciona valor no operador
        self._operator = text

        #- Adiciona valor na equation para mostrar no display
        self.equation = f"{self._left} {self._operator}"
        return
    #-> Equal
    @Slot()
    def _eq(self) -> None:
        display_text = self.display.text()

        if not is_valid_number(display_text):
            self._show_information("Conta incompleta.")
            return 
        
        if not self._left is None:
            self._right = float(display_text)
            #- Adiciona valor na equation para mostrar no display
            self.equation = f"{self._left} {self._operator} {self._right} ="
            #- Coloca parentese "()" se o número for menor que zero
            if self._right < 0:
                self.equation = f"{self._left} {self._operator} "\
                f"({self._right}) ="
            operator = f"{self._left} {self._operator} {self._right}"
            
        try:
            if self._left is not None and self._right is not None:
                if "^" in operator and isinstance(self._left, float) and \
                    isinstance(self._right, float):
                    result = pow(self._left, self._right)
                else:
                    #- Faz a operação
                    result = eval(operator.replace("x", "*"))
            else:
                return
        #- Captura o erro de divisão por zero e faz o tratamento
        except ZeroDivisionError:
            self._show_critical_error("Divisão por zero.")
            return 
        #- Captura o erro de número muito grande
        except OverflowError:
            self._show_critical_error("Não é possível realizar a conta.")
            return
        
        #- Limpa o terminal
        self.display.clear()
        #- Insere o resultado no display
        self.display.insert(str(result))
        #- Pega o valor do resultado no número esquerdo
        self._left = str(result)
        #- Serve para continuar o calculo
        return

    #-> Make Dialog
    def _make_dialog(self, text, title) -> QMessageBox:
        #-Definindo msg_box
        msg_box = self.window.make_message_box()
        #-Definindo text dentro do msg_box
        msg_box.setText(text)
        #-Definindo title dentro do msg_box
        msg_box.setWindowTitle(title)
        #-Definindo botão dentro do msg_box
        msg_box.setStandardButtons(msg_box.StandardButton.Ok)
        #- Retornando msg_box
        return msg_box

    #-> Show Critical Error
    def _show_critical_error(self, text) -> None:
        #- Define o Título
        msg_box = self._make_dialog(text, "Aviso")
        #- Define o ícone de Critical
        msg_box.setIcon(msg_box.Icon.Critical)
        #- Executa o msg_box
        msg_box.exec()
        return

    #-> Show Information
    def _show_information(self, text) -> None:
        #- Define o Título
        msg_box = self._make_dialog(text, "Informação")
        #- Define o ícone de Information
        msg_box.setIcon(msg_box.Icon.Information)
        #- Executa o msg_box
        msg_box.exec()
        return