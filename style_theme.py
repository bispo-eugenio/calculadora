#Imports
import qdarkstyle 
from constants import (DARK_PRIMARY, DARKEST_PRIMARY_COLOR,
                       PRIMARY_COLOR)

#Configuração das Cores dos Botões

qss = f"""
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
        border-radius: 5px;
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARK_PRIMARY};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}
"""
 
#Função para adicionar o style no app(Qapplication)
def setup_theme(app):
    #-> Aplicar o estilo escuro do qdarkstyle
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
 
    #-> Sobrepor com o QSS personalizado para estilização adicional
    app.setStyleSheet(app.styleSheet() + qss)