from collections import deque

## tive que trocar aqui pra funcionar os imports
import model.syntax_tree as syntax_tree
# import syntax_tree

# definimos classe de automatos, podem ser
# deterministicos ou não, epsilon transicoes
# sao representadas como &
class Automaton():
    '''
    :attr alphabet: conjunto de simbolos aceitos pelo automato
    :attr states: conjunto de estados (inclui finais e inicial)
    :attr init_state: estado inicial
    :attr transitions: dicionario de transicoes no formato:
        (estado, simbolo) : {estado1, estado2, ...}
    :attr final_states: conjunto de estados finais
    '''
    def __init__(self, alphabet=set(), states=set(), init_state=None, transitions={}, final_states=set()):
        self.alphabet = alphabet
        self.states = states
        self.transitions = transitions
        self.init_state = init_state
        self.final_states = final_states

    # determina se o automato eh afnd
    def isAFND(self):
        return any(a=='&' or len(t)>1 for (_,a),t in self.transitions.items())

    # simula a execucao de um afd sobre uma dada palavra e
    # determina se a palavra foi reconhecida pelo automato
    # obs.: nao serve para simular um afnd, e portanto
    # deve-se determinizar primeiro
    def run(self, word):
        # checa se eh AFD antes de simular
        if self.isAFND(): return
        # realiza a simulacao
        current_state = self.init_state
        for c in word:
            next_state = self.transitions.get((current_state,c))
            if next_state is None: return False
            current_state = next_state
        return current_state in self.final_states

    # renomeia os estados com numeros comecando por "i"
    # em todas as estruturas e atributos,
    # util para legibilidade e para
    # evitar colisoes durante a uniao
    def rename_states(self, i=0):
        # determina novos nomes dos estados
        # e checa se a renomeacao eh necessaria
        new_names = range(i,i+len(self.states))
        set_new_names = set(new_names)
        if self.states == set_new_names: return

        # varre os estados do automato por niveis (BFS)
        # partindo do estado inicial e armazena
        # os novos nomes para cada estado
        names = {self.init_state: i}
        i += 1
        queue = deque([self.init_state])
        while queue:
            s = queue.popleft()
            for a in self.alphabet:
                x = self.transitions.get((s,a), {})
                if isinstance(x,frozenset):
                    x = {x}
                for t in x:
                    if t not in names:
                        names[t] = i
                        i += 1
                        queue.append(t)

        # renomeia os estados em todas as estruturas
        self.states = set_new_names
        self.init_state = names.get(self.init_state)
        self.final_states = {names.get(fs) for fs in self.final_states}
        new_trans = {}
        for (s,a),t in self.transitions.items():
            new_trans[(names.get(s),a)] = names.get(t) if isinstance(t,frozenset) \
                                    else {names.get(u) for u in t}
        self.transitions = new_trans

    # mostra tabela de transicoes
    def print_automaton(self):       
        print('\ntransitions table:', end = '\n\n  | ')
        for a in sorted(self.alphabet):
            print(f'{a}', end = ' | ')
        for st in self.states:
            print(f'\n{st}', end = ' | ')
            for a in sorted(self.alphabet):
                if (st, a) in self.transitions.keys():
                    print(f'{self.transitions[(st, a)]}', end = ' | ')
                else:
                    print('-', end = ' | ') # sem transição            
        
        print(f'\n\ninitial: {self.init_state}')
        print('finals:', self.final_states)


# uniao de afds
# recebe uma quantidade arbitraria de afds
# e retorna afnd equivalente a uniao deles
def union(*afds):
    n_init = 0  # novo estado inicial
    n_states = {n_init}  # novos estados
    n_final = set()  # novos estados finais
    n_trans = {(n_init,'&'): set()}  # novas transicoes
    n_alphabet = set()  # novo alfabeto

    i = n_init + 1
    for afd in afds:
        # renomeia os estados de modo a evitar
        # que haja colisoes entre os nomes
        # dos estados dos diferentes afds
        afd.rename_states(i)
        i += len(afd.states)
        # atualiza as estruturas do novo automato
        # com aquelas de cada um dos afds
        n_states.update(afd.states)
        n_final.update(afd.final_states)
        n_trans.update(afd.transitions)
        n_alphabet.update(afd.alphabet)
        # insere a epsilon transicao partindo do novo
        # estado inicial para os antigos estados iniciais
        n_trans[(n_init,'&')].add(afd.init_state)

    return Automaton(n_alphabet, n_states, n_init, n_trans, n_final)

# determinizacao de afnd (algoritmo 3.2 no livro do Aho)
def determinization(afnd):
    # checa se a determinizacao eh necessaria
    if not afnd.isAFND(): return

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
    afd.rename_states()
    return afd

'''
constroi automato a partir de arvore de sintaxe
e lista de folhas, é o algoritmo Dstates do
slide
'''
def build_automaton(sa_root: syntax_tree.Node, leaf_list: list):
    '''
    :param states: estados do automato
    :return: um estado não marcado, caso todos 
        estejam marcados, retorna qualquer
    '''
    def find_unmarked(states):
        for s in states:
            if not s.marked:
                return s
        return next(iter(states))

    '''
    :param d_states: estados de um automato
    :param state: estado cuja existencia eh 
        verificada no método
    :return: booleano se existe ou nao
    '''
    def is_in_d_states(d_states, state):
        for s in d_states:
            if s.state == state:
                return True
        return False

    '''
    função que converte as d_transitions do algoritmo
    ER -> AFD para transições com os estados pelo nº do estado
    '''
    def convert_transitions(states_map, d_transitions):
        transitions = dict()
        for k, v in d_transitions.items():
            transitions[k] = states_map[frozenset(v)]

        return transitions

    # determina o conjunto de simbolos do alfabeto
    alphabet = {s.value for s in leaf_list}
    alphabet.discard('#')

    init_state = 0 # estado inicial
    # state_id (contador para identificar os estados)
    sid = init_state
    
    # estados que farão parte do automato
    d_states = set()
    d_transitions = dict()
    states = set() # conjunto de estados pelo seu numero
    states_map = dict() # dicionario que mapeia d_state -> sid

    # estado inicial
    initial_D = State(sa_root.first_pos, sid)
    d_states.add(initial_D)
    
    states_map[frozenset(initial_D.state)] = {sid}
    states.add(sid)
    sid += 1
    
    # conjunto de estados finais
    final_states = set()

    # loop marca 
    s = initial_D
    while s.marked == False:
        s.marked = True

        for a in alphabet:
            u = set()
            
            for state_index in s.state:
                if leaf_list[state_index].value == a:
                    u = u | leaf_list[state_index].follow_pos
            
            # AQUIII KLAUS, mudei a logica, caso u seja vazio
            # tratar caso de transição que nao vai 
            # para lugar nenhum (u vazio) (???)
            if u:
                d_transitions[(s.label, a)] = set()

                if not is_in_d_states(d_states, u):
                    # new state
                    new_state = State(u, sid)
                    d_states.add(new_state)
                    
                    states.add(sid)
                    states_map[frozenset(u)] = {sid}
                    sid += 1

                    # se novo estado tem # ele eh final
                    if (len(leaf_list) - 1) in u:
                        final_states.add(new_state.label)
                
                # define transicao
                d_transitions[(s.label, a)] = d_transitions[(s.label, a)] | u

        s = find_unmarked(d_states)

    ## converter as 'd_transiçoes' do algoritmo ER->AFD
    # para transiçoes com os indices numericos dos estados
    transitions = convert_transitions(states_map, d_transitions)        
    
    # gera o automato
    automaton = Automaton(alphabet, states, init_state, transitions, final_states)

    # só pra validacao, se quiser ver, uncomment
    # automaton.print_automaton()

    return automaton


class State():
    '''
    :attr state: conjunto de inteiros indicando
        que nós folha aquele estado representa
        (tirados da arvore sintatica)
    :attr marked: usado só pra facilitar o método
        build_automaton
    :attr label: nome do estado, usado pra acessar
        o dicionario de transicoes do automato
    '''
    def __init__(self, state: set, sid: int, marked: bool=False):
        self.state = state
        self.label = sid
        self.marked = marked
