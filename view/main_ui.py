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
        self.nonterminals_text = QTextEdit()
        self.grammar_text = QTextEdit()
        self.simulation_btn = QPushButton("Simulador")
        self.initUI(size)

    def initUI(self, size) -> None:
        self.resize(QSize(size[0], size[1]))
        self.center_window()
        self.setWindowTitle("Analisador Léxico e Sintático (Preditivo LL1)")
        self.create_main_layout()
        self.show()

    def center_window(self) -> None:
        fg = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(center)
        self.move(fg.topLeft())

    def create_main_layout(self) -> QLayout:
        layout = QVBoxLayout()

        splitter = QSplitter(Qt.Vertical)
        splitter.setStretchFactor(1, 1)
        splitter.addWidget(self.create_regex_layout())
        splitter.addWidget(self.create_grammar_layout())
        layout.addWidget(splitter)
        
        self.simulation_btn.clicked.connect(self.start_simulator)
        layout.addWidget(self.simulation_btn, Qt.AlignCenter)
        self.setLayout(layout)

    def create_regex_layout(self) -> QWidget:
        reg_def = self.create_text_area('Definições Regulares', self.reg_def_text)
        tokens = self.create_text_area('Tokens', self.token_text)
        keywords = self.create_text_area('Palavras Reservadas', self.keywords_text)
        
        self.load_regex_example()

        splitter = QSplitter(Qt.Horizontal)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([300, 300, 300])
        splitter.addWidget(reg_def)
        splitter.addWidget(tokens)
        splitter.addWidget(keywords)

        return splitter

    def load_regex_example(self) -> None:
        ###################### TESTE ######################
        self.reg_def_text.append(
            'L : [b,c,e,f,v]\n' +
            'M : [o,m]\n' +
            'P : [;]'
        )     
        self.token_text.append(
            'com : {L}{M}{M}\n' +
            'b : {L}\n' +
            '; : {P}'
        )
        self.keywords_text.append(
            'com = com : "com"\n' +
            'b = b : "b"\n' +
            'c = b : "c"\n' +
            'e = b : "e"\n' +
            'f = b : "f"\n' +
            'v = b : "v"'
        )
        ###################### TESTE ######################

    def create_grammar_layout(self) -> QWidget:
        nonterminals = self.create_text_area('Não Terminais', self.nonterminals_text)
        grammar = self.create_text_area('Gramática', self.grammar_text)
        
        self.load_grammar_example()

        splitter = QSplitter(Qt.Horizontal)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([300, 300])
        splitter.addWidget(nonterminals)
        splitter.addWidget(grammar)

        return splitter

    def load_grammar_example(self) -> None:
        ###################### TESTE ######################
        nonterminals_ex = "{P}\n{K}\n{V}\n{F}\n{C}"
        grammar_ex = ("{P} -> {K} {V} {C}\n"
                      "{K} -> c {K} | &\n"
                      "{V} -> v {V} | {F}\n"
                      "{F} -> f {P} ; {F} | &\n"
                      "{C} -> b {V} {C} e | com ; {C} | &\n")
        self.nonterminals_text.setText(nonterminals_ex)
        self.grammar_text.setText(grammar_ex)
        ###################### TESTE ######################

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
        nonterminals = self.nonterminals_text.toPlainText()
        grammar = self.grammar_text.toPlainText()
        self.control.start_simulator(reg_defs, tokens, keywords, nonterminals, grammar)