from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QDialog, QLabel, QTextEdit, QSplitter, QTableWidget, QTableWidgetItem,
    QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QLayout
)

class SimulatorUI(QDialog):
    def __init__(self, mainUI, app_control, size) -> None:
        super().__init__()
        self.control = app_control
        self.main_UI = mainUI
        self.scode_text = QTextEdit()
        self.symbols_table = QTableWidget()
        self.token_list_table = QTableWidget()
        self.exec_lex_btn = QPushButton("Analisar Léxico")
        self.exec_syntax_btn = QPushButton("Analisar Sintático")
        self.parsing_table_btn = QPushButton("Exibir tabela de parsing")
        self.parsing_table_ui = QDialog()
        self.parsing_table = QTableWidget()
        self.reset_btn = QPushButton("Resetar simulação")
        self.close_btn = QPushButton("Encerrar")
        self.initUI(size)
        self.init_parsing_table_UI(size)

    def initUI(self, size) -> None:
        self.setWindowTitle("Testar Analisador Léxico e Sintático [Preditivo LL1]")
        self.resize(QSize(size[0] + 250, size[1]))
        self.center_window()
        self.create_simulator_layout()

    def center_window(self) -> None:
        fg = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(center)
        self.move(fg.topLeft())

    def create_simulator_layout(self) -> QLayout:
        s_code = self.main_UI.create_text_area('Código Fonte', self.scode_text)
        ###################### TESTE ######################
        # self.scode_text.setText('c v f b e ;')
        ###################### TESTE ######################
        self.scode_text.setText('456 + (5 * 19)')
        ###################### TESTE ######################

        s_table = self.create_symbols_table_widget()
        tk_table = self.create_token_list_widget()

        splitter = QSplitter(Qt.Horizontal)
        splitter.setStretchFactor(1, 1)
        splitter.addWidget(s_code)
        splitter.addWidget(s_table)
        splitter.addWidget(tk_table)
        splitter.setSizes([310, 230, 310])
        
        hbox = QHBoxLayout()
        hbox.addWidget(splitter)

        layout = QVBoxLayout()
        layout.addLayout(hbox, 5)
        layout.addWidget(self.create_buttons_layout())
        self.setLayout(layout)

    def create_buttons_layout(self) -> QWidget:
        self.exec_lex_btn.clicked.connect(self.exec_lexical_analysis)
        self.reset_btn.clicked.connect(self.reset_simulation)
        self.close_btn.clicked.connect(self.close_simulator)
        lex_layout = QHBoxLayout()
        lex_layout.addWidget(self.exec_lex_btn)
        lex_layout.addWidget(self.reset_btn)
        lex_layout.addWidget(self.close_btn)

        self.exec_syntax_btn.clicked.connect(self.exec_syntactic_analysis)
        self.parsing_table_btn.clicked.connect(self.show_parsing_table)
        syn_layout = QHBoxLayout()
        syn_layout.addWidget(self.exec_syntax_btn)
        syn_layout.addWidget(self.parsing_table_btn)

        widget = QWidget()
        btns_layout = QVBoxLayout()
        btns_layout.addLayout(lex_layout)
        btns_layout.addLayout(syn_layout)
        widget.setLayout(btns_layout)
        return widget

    def create_symbols_table_widget(self) -> QWidget:
        if self.symbols_table.columnCount() < 2:
            self.symbols_table.setColumnCount(2)

        tokens = QTableWidgetItem('Token')
        self.symbols_table.setHorizontalHeaderItem(0, tokens)
        lexemes = QTableWidgetItem('Lexema')
        self.symbols_table.setHorizontalHeaderItem(1, lexemes)
        
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Tabela de Símbolos'))
        layout.addWidget(self.symbols_table)
        widget.setLayout(layout)
        return widget

    ## recebe uma lista de entradas para a tabela de simbolos
    def insert_symbols_table(self, entries) -> None:
        self.clear_symbols_table()
        size = len(entries)
        self.symbols_table.setRowCount(size)

        i = 0
        for k, v in entries.items():
            self.symbols_table.setItem(i, 0, QTableWidgetItem(','.join(v)))
            self.symbols_table.setItem(i, 1, QTableWidgetItem(k))
            i += 1

    def clear_symbols_table(self) -> None:
        self.symbols_table.clearContents()        
        self.symbols_table.setRowCount(0)


    def create_token_list_widget(self) -> QWidget:
        if self.token_list_table.columnCount() < 3:
            self.token_list_table.setColumnCount(3)

        tokens = QTableWidgetItem('Token')
        self.token_list_table.setHorizontalHeaderItem(0, tokens)
        lexemes = QTableWidgetItem('Lexema')
        self.token_list_table.setHorizontalHeaderItem(1, lexemes)
        position = QTableWidgetItem('Posição')
        self.token_list_table.setHorizontalHeaderItem(2, position)
        
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Lista de Tokens'))
        layout.addWidget(self.token_list_table)
        widget.setLayout(layout)
        return widget

    ## recebe uma lista de entradas para a lista de tokens
    def insert_token_list(self, entries) -> None:
        self.clear_token_list()
        size = len(entries)
        self.token_list_table.setRowCount(size)

        for i in range(size):
            self.token_list_table.setItem(i, 0, QTableWidgetItem(entries[i][0]))
            self.token_list_table.setItem(i, 1, QTableWidgetItem(entries[i][1]))
            self.token_list_table.setItem(i, 2, QTableWidgetItem(str(entries[i][2])))

    def clear_token_list(self) -> None:
        self.token_list_table.clearContents()        
        self.token_list_table.setRowCount(0)

    def close_simulator(self) -> None:
        self.clear_symbols_table()
        self.clear_token_list()
        self.clear_parsing_table()
        self.parsing_table_ui.close()
        self.control.end_simulation()
        self.close()

    def exec_syntactic_analysis(self) -> None:
        self.control.exec_syntactic_analysis()

    def exec_lexical_analysis(self) -> None:
        self.reset_simulation()
        text = self.scode_text.toPlainText()
        self.control.exec_lexical_analysis(text)

    def reset_simulation(self) -> None:
        self.clear_symbols_table()
        self.clear_token_list()
        keywords = self.main_UI.keywords_text.toPlainText()
        self.control.reset_simulation(keywords)

    def create_parsing_table(self, parsing_table_dict: dict, terminals: list) -> None:
        self.clear_parsing_table()
        terminals = sorted(set(terminals))
        col = len(terminals)
        if self.parsing_table.columnCount() < col:
            self.parsing_table.setColumnCount(col)

        row = len(parsing_table_dict)
        if self.parsing_table.rowCount() < row:
            self.parsing_table.setRowCount(row)

        self.parsing_table.setHorizontalHeaderLabels(terminals)
        self.parsing_table.setVerticalHeaderLabels(parsing_table_dict.keys())

        for i, nt in enumerate(parsing_table_dict):
            for j, t in enumerate(terminals):
                if parsing_table_dict[nt].get(t):
                    item = QTableWidgetItem(' '.join(parsing_table_dict[nt][t]))
                    self.parsing_table.setItem(i, j, item)
        
    def clear_parsing_table(self) -> None:
        self.parsing_table.clearContents()        
        self.parsing_table.setRowCount(0)
        self.parsing_table.setColumnCount(0)

    def show_parsing_table(self) -> None:
        self.parsing_table_ui.exec()

    def init_parsing_table_UI(self, size) -> None:
        layout = QVBoxLayout()
        layout.addWidget(self.parsing_table)
        self.parsing_table_ui.setLayout(layout)
        self.parsing_table_ui.setWindowTitle("Tabela de Parsing")
        self.parsing_table_ui.resize(QSize(size[0] + 250, size[1]))
        self.center_parsing_table_window()

    def center_parsing_table_window(self) -> None:
        fg = self.parsing_table_ui.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(center)
        self.parsing_table_ui.move(fg.topLeft()) 