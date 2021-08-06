from collections import deque
from pprint import pprint  # para printar os atributos

from print_tree import print_tree
import automaton
import syntax_tree

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
    
    # simula a execucao de um afd sobre uma dada palavra e
    # determina se a palavra foi reconhecida pelo automato
    # obs.: nao serve para simular um afnd, e portanto
    # deve-se determinizar primeiro
    def run(self, word):
        current_state = self.init_state
        for c in word:
            next_state = self.transitions.get((current_state,c))
            if next_state is None: return False
            current_state = next_state
        return current_state in self.final_states
    
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

    # renomeia estados de um afd
    # com numeros comecando por "i"
    # em todas as estruturas e atributos,
    # util para legibilidade e para
    # evitar colisoes durante a uniao
    def rename_states(self, afd, i=0):
        # determina novos nomes dos estados
        # e checa se a renomeacao eh necessaria
        new_names = range(i,i+len(afd.states))
        set_new_names = set(new_names)
        if afd.states == set_new_names: return

        # varre os estados do automato por niveis (BFS)
        # partindo do estado inicial e armazena
        # os novos nomes para cada estado
        names = {afd.init_state: i}
        i += 1
        queue = deque([afd.init_state])
        while queue:
            s = queue.popleft()
            for a in afd.alphabet:
                x = afd.transitions.get((s,a), {})
                if isinstance(x,frozenset):
                    x = {x}
                for t in x:
                    if t not in names:
                        names[t] = i
                        i += 1
                        queue.append(t)

        # renomeia os estados em todas as estruturas do afd
        afd.states = set_new_names
        afd.init_state = names.get(afd.init_state)
        afd.final_states = {names.get(fs) for fs in afd.final_states}
        new_trans = {}
        for (s,a),t in afd.transitions.items():
            new_trans[(names.get(s),a)] = names.get(t) if isinstance(t,frozenset) \
                                    else {names.get(u) for u in t}
        afd.transitions = new_trans

    # uniao de afds
    # recebe uma quantidade arbitraria de afds
    # e retorna afnd equivalente a uniao deles
    def afd_union(self, *afds):
        n_init = 0  # novo estado inicial
        n_states = {n_init}  # novos estados
        n_final = set()  # novos estados finais
        n_trans = {(n_init,'&'): set()}  # novas transicoes
        n_alphabet = set()  # novo alfabeto

        i = 1
        for afd in afds:
            # renomeia os estados de modo a evitar
            # que haja colisoes entre os nomes
            # dos estados dos diferentes afds
            self.rename_states(afd, i)
            i += len(afd.states)
            # atualiza as estruturas do novo automato
            # com as aquelas de cada um dos afds
            n_states.update(afd.states)
            n_final.update(afd.final_states)
            n_trans.update(afd.transitions)
            n_alphabet.update(afd.alphabet)
            # insere a epsilon transicao partindo do novo
            # estado inicial para os antigos estados iniciais
            n_trans[(n_init,'&')].add(afd.init_state)

        return Automaton(n_alphabet, n_states, n_init, n_trans, n_final)

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

        d_init = epsilon_closure(afnd.init_state)  # novo estado inicial
        d_states = {d_init}  # novos estados
        d_final = set()  # novos estados finais
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
        for s in d_states:
            if s & afnd.final_states:
                d_final.add(s)

        # afd obtido apos a determinizacao
        afd = Automaton(afnd.alphabet, d_states, d_init, d_trans, d_final)
        # renomeia os estados para melhor legibilidade
        self.rename_states(afd)
        return afd
    
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

    # teste ERs -> AFDs -> uniao -> determinizacao
    # com as expressoes regulares equivalentes
    # aos afds da figura 3.35 no livro do Aho

    # parse das ERs
    re1 = syntax_tree.parse_regex('a')
    re2 = syntax_tree.parse_regex('abb')
    re3 = syntax_tree.parse_regex('a*b+')

    # construcao das arvores sintaticas para cada ER
    st1 = syntax_tree.build_ST(re1)
    st2 = syntax_tree.build_ST(re2)
    st3 = syntax_tree.build_ST(re3)

    # print das arvores, uncomment para ver
    print_tree(st1)
    print_tree(st2)
    print_tree(st3)

    # computa nullable, firstpos, lastpos, followpos
    (st1, leaf_list1) = syntax_tree.specify_nodes(st1)
    (st2, leaf_list2) = syntax_tree.specify_nodes(st2)
    (st3, leaf_list3) = syntax_tree.specify_nodes(st3)

    # gera os afds para cada ER
    afd1 = automaton.Automaton(st1, leaf_list1, {'a'} )
    afd2 = automaton.Automaton(st2, leaf_list2, {'a', 'b'} )
    afd3 = automaton.Automaton(st3, leaf_list3, {'a', 'b'} )

    # printa as estruturas dos afds, uncomment pra ver
    print('afd1:')
    pprint(afd1.__dict__)

    print('\nafd2:')
    pprint(afd2.__dict__)

    print('\nafd3:')
    pprint(afd3.__dict__)

    # print('\n===================================================\n')

    # teste de uniao com os afds da figura 3.35 no livro do Aho
    # alphabet = {'a','b'}
    # states = {1, 2}
    # init_state = 1
    # transitions = {(1,'a'): {2}}
    # final_states = {2}
    # afd1 = Automaton(alphabet, states, init_state, transitions, final_states)

    # states = {3, 4, 5, 6}
    # init_state = 3
    # transitions = {
    #     (3,'a'): {4},
    #     (4,'b'): {5},
    #     (5,'b'): {6}
    # }
    # final_states = {6}
    # afd2 = Automaton(alphabet, states, init_state, transitions, final_states)

    # states = {7, 8}
    # init_state = 7
    # transitions = {
    #     (7,'a'): {7},
    #     (7,'b'): {8},
    #     (8,'b'): {8}
    # }
    # final_states = {8}
    # afd3 = Automaton(alphabet, states, init_state, transitions, final_states)

    # # faz a uniao e printa os atributos do afnd resultante
    # afnd_uniao = lex.afd_union(afd1, afd2, afd3)
    # print('União dos AFDs antes da determinização:\n')
    # pprint(afnd_uniao.__dict__)

    # print('\n===================================================\n')

    # determiniza o afnd resultante da uniao e printa seus atributos
    # afd_uniao = lex.det_automaton(afnd_uniao)
    # print('União dos AFDs após determinização:\n')
    # pprint(afd_uniao.__dict__)

    # print('\nTeste da execução sobre algumas palavras...')
    # words = ('a','aa','aaa','ab','aaab','abbbb','aaabbbb')
    # for word in words:
    #     print(f'run({word}) = {afd_uniao.run(word)}')
    

if __name__ == '__main__':
    main()
