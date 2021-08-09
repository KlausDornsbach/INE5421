from pprint import pprint  # para printar os atributos

## tive que trocar aqui pra funcionar os imports
from model.print_tree import print_tree
import model.automaton as automaton
import model.syntax_tree as syntax_tree

# import print_tree
# import automaton
# import syntax_tree

class Lexico():
    # modificação desse construtor, para poder 
    # inicializar o Lexico no controlador da aplicação
    def __init__(self):
        self.reg_defs = dict()
        self.alphabet = set()
        self.analyzer = None # vai ser o afd final apos todo o processo


    '''
    parametro expression é uma lista de strings que são
    definicoes regulares
    :attr reg_def: dicionario[key] -> {set de simbolos}
    :attr alphabet: set da uniao de simbolos definidos
    '''
    def generate_regdefs_alphabet(self, expressions):
        reg_defs = dict()
        alphabet = set()
        for i in expressions:
            (key, value) = self.parse_regular_definition(i)
            alphabet = alphabet | value
            reg_defs[key] = value
        self.reg_defs = reg_defs
        self.alphabet = alphabet
        
    # transformar gramatica livre de contexto
    # em um autômato que nos permita reconhecer
    # a classe de um lexema
    def regex_to_afd(self, file):
        pass
    
    # ler um texto e dar output em uma lista:
    # padrao, lexema, indice no arquivo
    def create_symbol_table(self, file):
        pass

    # parseio a expressao, coloco nome associado
    # a uma lista de simbolos usados na definicao
    # através de dicionario
    # regular definition-> digit : [0, 1, ..., 9]
    def parse_regular_definition(self, expression):
        end_key = expression.find(' :')
        if end_key == -1:
            end_key = expression.find(':')
        key = expression[0:end_key]
        # string.find(value, start, end)
        index = expression.find('[', end_key) + 1   
        part = expression[index:-1]
        alphabet = part.split(',')
        if alphabet == None:
            alphabet = part.split('|')
            if alphabet == None:
                print('parse error! please input regular definition in correct format')
        return (key, set(alphabet))
    
    '''
    funcao make automatiza transformacao ER->AFD->Uniao->Determinizacao
    :param reg_defs: lista de str com definicoes regulares 
    :param tokens: lista de str com definicoes de tokens
    :param verbose: printar ou nao as informacoes ao longo do processo
    :return automato_completo: Automato pronto para ler entradas de texto
    '''
    def make(self, reg_defs: list, raw_tokens: list, verbose: bool=True):
        # lex = Lexico(reg_defs)
        self.generate_regdefs_alphabet(reg_defs)

        automata = []
        regexes = []

        for rt in range(len(raw_tokens)):
            regexes.append(syntax_tree.parse_regex(raw_tokens[rt], self.reg_defs, self.alphabet))
            st = syntax_tree.build_ST(regexes[rt], self.alphabet)
            (st, leaf_list) = syntax_tree.specify_nodes(st, self.alphabet)
            # print(st)
            # print(leaf_list)
            # print(lex.alphabet)
            afd = automaton.build_automaton(st, leaf_list)
            # print(afd.init_state)
            # print(afd.states)
            # print(afd.final_states)
            # print(afd.transitions)
            # print(afd.alphabet)
            if verbose:
                print('\n============================\n')
                print(f'raw token: {raw_tokens[rt]}')
                print(f'derived regex: {regexes[rt]}')
                print(f'generated tree:')
                print_tree(st)
                print('automaton:')
                pprint(afd.__dict__)
                # afd.print_automaton()
            
            automata.append(afd)
        
        # union
        afnd_uniao = automaton.union(*automata)
        
        # determinization
        afd_uniao = automaton.determinization(afnd_uniao)
        if verbose:
            print('\n====================================\nunion\n====================================\n')
            pprint(afnd_uniao.__dict__)
            print('\n====================================\ndeterminizado\n====================================\n')
            pprint(afd_uniao.__dict__)

        self.analyzer = afd_uniao

    

def main():
    '''
    AQUI ->  parte pra automatizar fazer o automato
    definicao regulares e tokens
    call pra make
    '''
    reg_def1 = 'a : [a]'
    reg_def2 = 'b : [b]'
    # tenho que definir cada simbolo dos tokens entre chaves  
    lex = Lexico()
    lex.make([reg_def1, reg_def2], ['{a}', '{a}{b}{b}', '{a}*{b}+'])
    
    print('\n___________________/\/\/\/\/\/\/\/\/\/\/\/\/\______________________\n')
    

if __name__ == '__main__':
    main()
