# definimos classe de automatos, podem ser
# deterministicos ou não, epsilon transicoes
# sao representadas como &
class Automata():
    # um automato possui um dicionario de
    # simbolos (alfabeto), lista de estados, cada
    # estado representado por uma string, 
    # um estado inicial, uma lista de transicoes
    # representada por um dicionario que mapeia
    # tuplas de estado + simbolo para 
    # um estado: transicao[(q1, a)] = q3
    # q1, q3 \in states, a \in alphabet
    def __init__(self, alphabet={}, states=[], init_state=None, transitions={}, final_states=[]):
        self.alphabet = alphabet
        self.states = states
        self.transitions = transitions
        self.init_state = init_state
        self.final_states = final_states
    
    def read_file():
        pass

class SyntaxTree():
    # a arvore tem nodos, cada nodo com 2 nodos filhos
    # um nodo pode ter os seguintes simbolos: 
    # -definicao regular
    # operacao: *?|.
    # quando é encontrado () na entrada, ponteiro para
    # pai é setado 
    class Node():
        def __init__(self, symbol, c1=None, c2=None, father=None):
            self.c1 = c1
            self.c2 = c2
            self.symbol = symbol
        
    # a arvore de sintaxe recebe um dicionario
    # que mapeia o nome de definicoes regulares 
    # para simbolos, esses simbolos podem ser
    # definicoes regulares com simbolos internos
    def __init__(self, expression, dictionaries):
        expression.append('#')
        # cria arvore
        # descobre nullable, lastpos, nextpos e followpos
        # cria automato
        # self.automata = Automata()
        pass
    # usado na definicao de tokens, ex.:
    # token -> id : letter(letter|digit)*
    def parse_token_definition(self, token):
        pass

    def create_tree(self, expression):
        i = len(expression) - 1     # comeco no fim
        end = Node('#')
        root = Node('.', None, end)
        father = root
        while i > -1:
            new = Node(expression[i])
            if expression[i] in {'?', '*', '|', ')', '('}:
                # finds special character
                if expression[i] == '*':
                    pass
                pass
            else: # finds a leaf
                concat_node = Node('.', new, father.c1)
                father.c1 = concat_node
                father = new
            i -= i
        pass


class Lexico():
    # transformar gramatica livre de contexto
    # em um autômato que nos permita reconhecer
    # a classe de um lexema
    def regex_to_afd(self, file):
        pass

    # juntar afd's 
    def afd_union(self, afd):
        pass

    # determinizacao de automato
    def det_automata():
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
        return {key : alphabet}

def main():
    lex = Lexico()
    letter_ = lex.parse_regular_definition('letter_ : [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,x,w,y,z_]')


if __name__ == '__main__':
    main()