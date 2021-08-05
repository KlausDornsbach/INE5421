# definimos classe de automatos, podem ser
# deterministicos ou não, epsilon transicoes
# sao representadas como &
class Automaton():
    # um automato possui um dicionario de
    # simbolos (alfabeto), lista de estados, cada
    # estado representado por uma string, 
    # um estado inicial, uma lista de transicoes
    # representada por um dicionario que mapeia
    # tuplas de estado + simbolo para 
    # um estado: transicao[(q1, a)] = q3
    # q1, q3 \in states, a \in alphabet
    def __init__(self, alphabet=set(), states=set(), init_state=None, transitions={}, final_states=set()):
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
        # self.automaton = Automaton()
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

    # uniao de afd's
    # recebe uma quantidade arbitraria de afd's como parametro
    def afd_union(self, *afds):
        for afd in afds:
            pass

    # determinizacao de afnd (algoritmo 3.2 no livro do Aho)
    # recebe afnd e retorna afd equivalente
    def det_automaton(self, afnd):
        # computa o epsilon fecho
        def epsilon_closure(T):
            if isinstance(T, int):  # fechamento-&(s)
                stack = [T]
                eps_closure = {T}
            else:  # fechamento-&(T)
                stack = list(T)
                eps_closure = T
            while stack:
                t = stack.pop()  # desempilha um estado t
                # itera pelos estados u alcancaveis por t atraves de &
                for u in afnd.transitions.get((t,'&'), {}):
                    if u not in eps_closure:
                        eps_closure.add(u)
                        stack.append(u)
            # retorna um frozenset (conjunto imutavel)
            # possibilita ser adicionado a outros sets
            return frozenset(eps_closure)

        # computa o conjunto de estados do afnd que
        # possuem transicoes partindo de estados de
        # T pelo simbolo a e chegando a si
        def movement(T, a):
            mov = set()
            if isinstance(T, int):
                T = {T}
            for t in T:
                u = afnd.transitions.get((t,a), {})
                if u:  # se a transicao existir
                    mov.update(u)
            return mov

        init_state = epsilon_closure(afnd.init_state)  # novo estado inicial
        d_states = {init_state}  # novos estados
        d_trans = dict()  # novas transicoes

        # computa todos os novos estados e transicoes
        marked = set()  # conjunto de estados marcados
        while marked != d_states:  # se houver estados nao marcados
            T = (d_states-marked).pop()  # pega um estado nao marcado
            marked.add(T)  # marca o estado
            for a in afnd.alphabet:
                u = epsilon_closure(movement(T,a))
                d_states.add(u)
                d_trans[(T,a)] = u
        
        # computa os novos estados finais
        final_states = set()
        for s in afnd.final_states:
            for t in d_states:
                if s in t:
                    final_states.add(t)

        return Automaton(afnd.alphabet, d_states, init_state, d_trans, final_states)

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

    # teste de determinizacao com o afnd
    # da figura 3.27 no livro do Aho
    alphabet = {'a','b'}
    states = set(range(11))
    init_state = 0
    transitions = {
        (0,'&'): {1,7},
        (1,'&'): {2,4},
        (2,'a'): {3},
        (3,'&'): {6},
        (4,'b'): {5},
        (5,'&'): {6},
        (6,'&'): {1,7},
        (7,'a'): {8},
        (8,'b'): {9},
        (9,'b'): {10},
    }
    final_states = {10}
    afnd = Automaton(alphabet, states, init_state, transitions, final_states)
    
    # determiniza o afnd e printa os atributos do afd
    afd = lex.det_automaton(afnd)
    __import__('pprint').pprint(afd.__dict__)
    

if __name__ == '__main__':
    main()
