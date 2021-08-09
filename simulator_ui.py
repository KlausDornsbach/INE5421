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
        self.execute_btn = QPushButton("Analisar Léxico")
        self.clear_table_btn = QPushButton("Limpar Tabela")
        self.close_btn = QPushButton("Encerrar")
        self.initUI(size)

    def initUI(self, size) -> None:
        self.setWindowTitle("Testar Analisador Léxico")
        self.resize(QSize(size[0], size[1]))
        self.center_window()
        self.create_simulator_layout()

    def center_window(self) -> None:
        fg = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(center)
        self.move(fg.topLeft())

    def create_simulator_layout(self) -> QLayout:
        s_code = self.main_UI.create_text_area('Código Fonte', self.scode_text)
        s_table = self.create_symbols_table_widget()

        splitter = QSplitter(Qt.Horizontal)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([550, 550])
        splitter.addWidget(s_code)
        splitter.addWidget(s_table)
        
        hbox = QHBoxLayout()
        hbox.addWidget(splitter)

        layout = QVBoxLayout()
        layout.addLayout(hbox, 5)
        layout.addWidget(self.create_buttons_layout())
        self.setLayout(layout)

    def create_buttons_layout(self) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout()

        self.execute_btn.clicked.connect(self.exec_lexical_analysis)
        self.clear_table_btn.clicked.connect(self.clear_symbols_table)
        self.close_btn.clicked.connect(self.close_simulator)

        layout.addWidget(self.execute_btn)
        layout.addWidget(self.clear_table_btn)
        layout.addWidget(self.close_btn)
        widget.setLayout(layout)
        return widget

    def create_symbols_table_widget(self) -> QWidget:
        if self.symbols_table.columnCount() < 3:
            self.symbols_table.setColumnCount(3)

        tokens = QTableWidgetItem('Token')
        self.symbols_table.setHorizontalHeaderItem(0, tokens)
        lexemes = QTableWidgetItem('Lexema')
        self.symbols_table.setHorizontalHeaderItem(1, lexemes)
        position = QTableWidgetItem('Posição')
        self.symbols_table.setHorizontalHeaderItem(2, position)
        
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Tabela de Símbolos'))
        layout.addWidget(self.symbols_table)
        widget.setLayout(layout)
        return widget

    ## recebe uma lista de entradas para a tabela de simbolos
    # sugestão: entries = Tuple/List (ID, lexema, posição)
    def insert_symbols_table(self, entries) -> None:
        self.clear_symbols_table()
        size = len(entries)
        self.symbols_table.setRowCount(size)

        for i in range(size):
            self.symbols_table.setItem(i, 0, QTableWidgetItem(entries[i][0]))
            self.symbols_table.setItem(i, 1, QTableWidgetItem(entries[i][1]))
            self.symbols_table.setItem(i, 2, QTableWidgetItem(entries[i][2]))

    def clear_symbols_table(self) -> None:
        self.symbols_table.setRowCount(0)

    def close_simulator(self) -> None:
        self.clear_symbols_table()
        self.close()

    def exec_lexical_analysis(self) -> None:
        self.control.exec_lexical_analysis()
