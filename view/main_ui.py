from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QLayout, QLabel, QSplitter, QTextEdit, QWidget,
    QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton
)
from view.simulator_ui import SimulatorUI


class MainUI(QWidget):
    def __init__(self, app_control, size) -> None:
        super().__init__()
        self.control = app_control
        self.simulator_ui = SimulatorUI(self, app_control, size)
        self.reg_def_text = QTextEdit()
        self.token_text = QTextEdit()
        self.keywords_text = QTextEdit()
        self.simulation_btn = QPushButton("Simulador")
        self.initUI(size)

    def initUI(self, size) -> None:
        self.resize(QSize(size[0], size[1]))
        self.center_window()
        self.setWindowTitle("Analisador Léxico")
        self.create_main_layout()
        self.show()

    def center_window(self) -> None:
        fg = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(center)
        self.move(fg.topLeft())

    def create_main_layout(self) -> QLayout:
        layout = QVBoxLayout()

        reg_def = self.create_text_area('Definições Regulares', self.reg_def_text)
        tokens = self.create_text_area('Tokens', self.token_text)
        keywords = self.create_text_area('Palavras Reservadas (Tokens especiais)', self.keywords_text)
        
        ###################### TESTE ######################
        # mesmo caso de teste que está 
        # sendo feito em lexico.py 
        # (simula os exemplos como um texto unico)
        reg_def_ex = 'a : [a]\nb : [b]'
        tokens_ex = 'X : {a}\nY : {a}{b}{b}\nZ :  {a}*{b}+'
        keyword_ex = 'bbb = Z : "bbb"\nabb = Y : "abb"'
        self.reg_def_text.setText(reg_def_ex)
        self.token_text.setText(tokens_ex)
        self.keywords_text.setText(keyword_ex)
        ###################### TESTE ######################

        splitter = QSplitter(Qt.Horizontal)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([300, 300])
        ss = QSplitter(Qt.Vertical)
        ss.addWidget(reg_def)
        ss.addWidget(tokens)
        splitter.addWidget(ss)
        splitter.addWidget(keywords)
        
        hbox = QHBoxLayout()
        hbox.addWidget(splitter)
        layout.addLayout(hbox)

        self.simulation_btn.clicked.connect(self.start_simulator)
        layout.addWidget(self.simulation_btn, Qt.AlignCenter)
        self.setLayout(layout)

    def create_text_area(self, title: str, text_widget: QWidget) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(title))
        layout.addWidget(text_widget)
        widget.setLayout(layout)
        return widget

    def start_simulator(self) -> None:
        reg_defs = self.reg_def_text.toPlainText()
        tokens = self.token_text.toPlainText()
        keywords = self.keywords_text.toPlainText()
        self.control.start_simulator(reg_defs, tokens, keywords)
        self.simulator_ui.exec()
