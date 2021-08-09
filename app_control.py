from view.main_ui import MainUI
from model.lexico import Lexico

class AppControl():

    def __init__(self):
        self.main_ui = MainUI(self, (700, 500))
        self.lex = Lexico()

    def start_simulator(self, input_reg_defs: str, input_tokens: str):
        reg_defs_list = input_reg_defs.splitlines()
        tokens_list = input_tokens.splitlines()
        
        # # para ver como ficam as listas cruas
        # # a partir das linhas dos campos de texto:
        # print(reg_defs_list)
        # print(tokens_list)
        self.lex.make(reg_defs_list, tokens_list)

    def exec_lexical_analysis(self) -> None:
        self.lex.create_symbol_table('...') # não esta fazendo nada por enquanto

        ######################## TESTE ########################
        # exemplo de uma lista de entrada
        # para a tabela de simbolos (sugestão)
        st_entry = [
            ('ID', 'begin', '0'),
            ('ID', 'while', '10'),
            ('ID', 'for', '15')
        ]
        self.main_ui.simulator_ui.insert_symbols_table(st_entry)
        ######################## TESTE ########################
    