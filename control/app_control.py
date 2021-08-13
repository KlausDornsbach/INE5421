from view.main_ui import MainUI
from model.lexico import Lexico

class AppControl():

    def __init__(self):
        self.main_ui = MainUI(self, (700, 500))
        self.simulator_ui = self.main_ui.simulator_ui
        self.lex = Lexico()

    def start_simulator(self, input_reg_defs: str, input_tokens: str, keywords: str) -> None:
        reg_defs_list = input_reg_defs.splitlines()
        tokens_list = input_tokens.splitlines()
        self.create_symbols_table(keywords)
        self.lex.make(reg_defs_list, tokens_list)

    def create_symbols_table(self, keywords: str) -> None:
        keywords_list = self.parse_keywords(keywords.splitlines())
        self.lex.create_symbol_table(keywords_list)
        self.simulator_ui.insert_symbols_table(self.lex.symbols_table)

    # faz o parsing do texto das palavras reservadas
    # retorna uma lista de triplas contendo:
    # [0] token da palavra chave 
    # [1] token "pai" para verificar se faz parte de alguma def reg
    # [1] lexema da palavra chave
    def parse_keywords(self, keywords: list) -> None:
        keywords_list = []
        for kw in keywords:
            list = kw.split()
            keyword = list[0]
            token_id = list[2]
            lexeme = list[4].strip('""')
            keywords_list.append( [keyword, token_id, lexeme] )

        return keywords_list


    def exec_lexical_analysis(self, source_text: str) -> None:
        self.lex.analyze(source_text)
        self.simulator_ui.insert_token_list(self.lex.tokens)
        self.simulator_ui.insert_symbols_table(self.lex.symbols_table)

    def reset_simulation(self, keywords: str) -> None:
        self.lex.reset()
        self.create_symbols_table(keywords)

    def end_simulation(self) -> None:
        self.lex.clear()