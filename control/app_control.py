from PyQt5.QtWidgets import QMessageBox
from model.syntactic import Syntactic
from view.main_ui import MainUI
from model.lexico import Lexico

class AppControl():

    def __init__(self):
        self.main_ui = MainUI(self, (700, 500))
        self.simulator_ui = self.main_ui.simulator_ui
        self.lex = Lexico()
        self.syn = Syntactic()
        self.msg_dialog = QMessageBox()

    def start_simulator(self, reg_defs: str, tokens: str, keywords: str, nonterminals: str, grammar: str) -> None:
        reg_defs_list = reg_defs.splitlines()
        tokens_list = tokens.splitlines()
        keywords_list = self.parse_keywords(keywords.splitlines())
        self.create_symbols_table(keywords_list)
        self.lex.make(reg_defs_list, tokens_list)
        
        # terminais da gramática são os tokens (e palavras reservadas)
        terminals_list = [k[0] for k in keywords_list] + [tk.split()[0] for tk in tokens_list]
        nonterminals_list = [nt.strip('{}') for nt in nonterminals.splitlines()]
        productions = self.split_grammar(grammar.splitlines())

        error = self.syn.make(nonterminals_list, terminals_list, productions)
        if error:
            self.show_message_dialog(error)
        else:
            self.create_parsing_table(terminals_list + ['$'])
            self.simulator_ui.exec()

    def create_symbols_table(self, keywords_list: list) -> None:
        self.lex.create_symbol_table(keywords_list)
        self.simulator_ui.insert_symbols_table(self.lex.symbols_table)

    def create_parsing_table(self, terminals: list) -> None:
        self.simulator_ui.init_parsing_table(self.syn.parsing_table, terminals)

    # faz o parsing do texto das palavras reservadas
    # retorna uma lista de triplas contendo:
    # [0] token da palavra chave 
    # [1] token "pai" para verificar se faz parte de alguma def reg
    # [1] lexema da palavra chave
    def parse_keywords(self, keywords: list) -> list:
        keywords_list = []
        for kw in keywords:
            list = kw.split()
            keyword = list[0]
            token_id = list[2]
            lexeme = list[4].strip('""')
            keywords_list.append( [keyword, token_id, lexeme] )

        return keywords_list

    # transforma a gramática de entrada em forma de 
    # strings num dicionário, conforme modelagem adotada
    # (ver construtor da classe Grammar) 
    def split_grammar(self, grammar_list: list[str]) -> dict:
        grammar = dict()
        for line in grammar_list:
            line = line.split(' -> ')
            head = line[0].strip('{}')
            grammar[head] = []
            productions = line[1].split('|')
            for prod in productions:
                grammar[head].append([symb.strip('{}') for symb in prod.split()])

        return grammar

    def exec_lexical_analysis(self, source_text: str) -> None:
        self.lex.analyze(source_text)
        self.simulator_ui.insert_token_list(self.lex.tokens)
        self.simulator_ui.insert_symbols_table(self.lex.symbols_table)

    def exec_syntactic_analysis(self, source_text: str) -> None:
        result, description = self.syn.validate_sentence(source_text)
        self.show_message_dialog(description, result)

    def reset_simulation(self, keywords: str) -> None:
        self.lex.reset()
        self.create_symbols_table(self.parse_keywords(keywords.splitlines()))

    def end_simulation(self) -> None:
        self.lex.clear()
        self.syn.clear()

    def show_message_dialog(self, description: str, result=False) -> None:
        self.msg_dialog = QMessageBox()
        if result:
            self.msg_dialog.setIcon(QMessageBox.Information)
            self.msg_dialog.setWindowTitle("Sucesso!")
            self.msg_dialog.setText(description)
        else:
            self.msg_dialog.setWindowTitle("Erro")
            self.msg_dialog.setIcon(QMessageBox.Warning)
            self.msg_dialog.setText("Ocorreu um erro:")
            self.msg_dialog.setInformativeText(description)
        self.msg_dialog.setStandardButtons(QMessageBox.Ok)
        self.msg_dialog.exec_()