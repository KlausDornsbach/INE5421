from pprint import pprint  # para printar os atributos
from string import whitespace

## tive que trocar aqui pra funcionar os imports
from model.print_tree import print_tree
import model.automaton as automaton
import model.syntax_tree as syntax_tree

# import print_tree
# import automaton
# import syntax_tree

class Lexico():
    def __init__(self):
        self.reg_defs = dict()
        self.alphabet = set()
        self.analyzer = None
        self.symbols_table = dict()
        self.tokens = []


    # reinicializa lexico, para repetir uma
    # nova analise lexica, sobre um diferente
    # texto fonte
    def reset(self) -> None:
        self.symbols_table.clear()
        self.tokens.clear()

    # método para reinicializar os atributos
    # para evitar ter de criar uma nova instancia
    # toda vez que iniciar uma nova simulação
    def clear(self) -> None:
        self.reg_defs = dict()
        self.alphabet = set()
        self.analyzer = None
        self.symbols_table = dict()
        self.tokens = []

    '''
    parametro expression é uma lista de strings que são
    definicoes regulares
    :attr reg_def: dicionario[key] -> {set de simbolos}
    :attr alphabet: set da uniao de simbolos definidos
    '''
    def create_regdefs_alphabet(self, expressions):
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
    
    
    '''
    método para inicializar a tabela de simbolos, a
    partir das palavras reservadas de entrada.
    para fazer uma validaçao previa, testa se o ID
    da keyword existe no dicionario das definiçoes regulares
    :param keywords: lista de tuplas contendo
    # [0] token da palavra chave 
    # [1] token "pai" para verificar se faz parte de alguma def reg
    # [1] lexema da palavra chaveER da definicao regular 
    :return: lista contendo os simbolos da def regular
    '''
    def create_symbol_table(self, keywords: list):
        for k in keywords:
            # if k[1] in self.reg_defs.keys():
            #     self.symbols_table[k[0]] = k[2]
            self.symbols_table[k[0]] = {k[2]}

    # encontra o indice do proximo caractere
    # no texto que nao seja de espacamento,
    # a partir do indice i
    def get_next_idx(self, text, i):
        while i < len(text) and text[i] in whitespace:
            i += 1
        return i
    
    # checa se o lexema ja esta na TS
    # se estiver, retorna True e seu(s) token(s)
    # senao, executa o AFD sobre o lexema
    def check(self, lexeme):
        if lexeme in self.symbols_table:
            return True, self.symbols_table.get(lexeme)
        return self.analyzer.run(lexeme)

    # faz a analise lexica
    def analyze(self, text):
        # inicializa os ponteiros
        begin = self.get_next_idx(text, 0)
        forward = begin + 1
        while begin < len(text):
            lexeme = text[begin]
            was_valid, tokens = self.check(lexeme)
            if tokens is None:
                self.tokens.append(('ERRO LÉXICO', f'Caracter não esperado: {lexeme[0]}', begin))
                break
            while forward < len(text):
                lexeme += text[forward]
                is_valid, tokens = self.check(lexeme)
                if was_valid and not is_valid: break
                was_valid = is_valid
                forward += 1
            # lexema valido encontrado
            # pega o(s) token(s) e atualiza as estruturas
            if forward < len(text): # se for a ultima palavra, nao precisa cortar
                lexeme = lexeme[:-1]
            is_valid, tokens = self.check(lexeme)
            self.symbols_table[lexeme] = tokens
            self.tokens.append((','.join(tokens), lexeme, begin))
            # atualiza os ponteiros
            begin = self.get_next_idx(text, forward) # se o forward era espaco, pular o espaco para nao iniciar de um espaco
            forward = begin + 1
    
    # Identificar as tokens pelo seu identificador,
    # em um dicionario.
    # vai servir para indicar na hora de criar cada
    # automato a qual padrao de token ele "traduz"
    # para depois no automato unido, saber quais
    # estados representam qual token!
    # mapeamento é bem simples:
    # raw_token -> 'nome_do_token' : expressao q define o token
    def identify_tokens(self, raw_tokens) -> dict:
        tokens = dict()
        for rt in raw_tokens:
            split = rt.split(":")
            key = split[0].strip()
            val = split[1].strip()
            tokens[key] = val

        return tokens

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
        if len(part) > 1 and part[1] == '-':
            alphabet = self.process_abreviated_reg_def(part)
        else:
            alphabet = part.split(',')
        if alphabet == None:
            alphabet = part.split('|')
            if alphabet == None:
                raise Exception('parse error! please input regular definition in correct format')
        return (key, set(alphabet))

    '''
    método para gerar lista de simbolos para definicoes regulares
    no formato abreviado (ex: 'a-z') a iterando sobre o codigo ASC
    dos caracteres. utilizado em parse_regular_definitions.
    :param expression: ER da definicao regular 
    :return: lista contendo os simbolos da def regular
    '''
    def process_abreviated_reg_def(self, expression: str):
        if expression == '0-9':
            return [chr(i) for i in range(ord('0'), ord('9') + 1)]

        elif expression == 'a-z':
            return [chr(i) for i in range(ord('a'), ord('z') + 1)]
    
        elif expression in {'a-zA-Z', 'A-Za-z'}:
            return [chr(i) for i in range(ord('a'), ord('z') + 1)] + [chr(i) for i in range(ord('A'), ord('Z') + 1)]

        else:
            raise Exception('parse error! please input regular definition in correct format')


    '''
    funcao make automatiza transformacao ER->AFD->Uniao->Determinizacao
    :param reg_defs: lista de str com definicoes regulares 
    :param tokens: lista de str com definicoes de tokens
    :param verbose: printar ou nao as informacoes ao longo do processo
    :return automato_completo: Automato pronto para ler entradas de texto
    '''
    def make(self, reg_defs: list, raw_tokens: list, verbose: bool=False):
        # lex = Lexico(reg_defs)
        self.create_regdefs_alphabet(reg_defs)
        tokens = self.identify_tokens(raw_tokens)

        automata = []
        regexes = []

        # for rt in range(len(raw_tokens)):
            # regexes.append(syntax_tree.parse_regex(raw_tokens[rt], self.reg_defs, self.alphabet))
            # st = syntax_tree.build_ST(regexes[rt], self.alphabet)
            
        for id, rtk in tokens.items():
            regex = syntax_tree.parse_regex(rtk, self.reg_defs, self.alphabet)
            st = syntax_tree.build_ST(regex, self.alphabet)

            (st, leaf_list) = syntax_tree.specify_nodes(st, self.alphabet)
            afd = automaton.build_automaton(st, leaf_list, id) # passa o identificador da exp regular
            
            # afd = automaton.build_automaton(st, leaf_list)
            # print(afd.init_state)
            # print(afd.states)
            # print(afd.final_states)
            # print(afd.transitions)
            # print(afd.alphabet)
            if verbose:
                print('\n============================\n')
                print(f'raw token: {rtk}')
                print(f'derived regex: {regex}')
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
