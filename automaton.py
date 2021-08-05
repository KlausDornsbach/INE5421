import syntax_tree

class Automaton():
    '''
    :attr alphabet: conjunto de simbolos aceitos pelo automato
    :attr initial_state: estado inicial
    :attr states: conjunto de estados (inclui finais e inicial)
    :attr final_states: conjunto de estados finais
    :attr transitions: dicionario de transicoes no formato:
        (simbolo, estado.label) : (estado1, estado2, ...)

    '''
    def __init__(self, syntax_tree: syntax_tree.Node, leaf_list: list, alphabet: set = {'a', 'b'}):
        initial, states, finals, transitions = self.build_automaton(syntax_tree, leaf_list, alphabet)
        self.initial_state = initial
        self.states = states
        self.final_states = finals
        self.transitions = transitions
        self.alphabet = alphabet

    '''
    usado em: build_automaton
    :param states: estados do automato
    :return: um estado não marcado, caso todos 
        estejam marcados, retorna qualquer
    '''
    def find_unmarked(self, states):
        for s in states:
            if not s.marked:
                return s
        return next(iter(states))
    
    '''
    usado em: build_automaton
    :param d_states: estados de um automato
    :param state: estado cuja existencia eh 
        verificada no método
    :return: booleano se existe ou nao
    '''
    def is_in_d_states(self, d_states, state):
        for s in d_states:
            if s.state == state:
                return True
        return False


    '''
    constroi automato a partir de arvore de sintaxe
    e lista de folhas, é o algoritmo Dstates do
    slide
    '''
    def build_automaton(self, sa_root: syntax_tree.Node, leaf_list: list, alphabet: set):
        # estados que farão parte do automato
        d_states = set()
        transitions = dict()

        # estado inicial
        initial_D = State(sa_root.first_pos)
        d_states.add(initial_D)
        
        # conjunto de estados finais
        final_states = set()

        # loop marca 
        s = initial_D
        while s.marked == False:
            s.marked = True
    
            for a in alphabet:
                transitions[(a, s.label)] = set()
                u = set()
                
                for state_index in s.state:
                    if leaf_list[state_index].value == a:
                        u = u | leaf_list[state_index].follow_pos
                
                if not self.is_in_d_states(d_states, u):
                    # new state
                    new_state = State(u)
                    d_states.add(new_state)

                    # se novo estado tem # ele eh final
                    if (len(leaf_list) - 1) in u:
                        final_states.add(new_state)
                
                # define transicao
                transitions[(a, s.label)] = transitions[(a, s.label)] | u

            s = self.find_unmarked(d_states)

        # só pra validacao, se quiser ver, uncomment
        # for st in d_states:
        #     for a in alphabet:
        #         print(f'symbol: {a}, state: {st.label}, transitions to: {transitions[(a, st.label)]}')
        

        # print(f'initial {initial_D.label}')

        # print('finals')
        # for st in final_states:
        #     print(st.label)
        
        return (initial_D, d_states, final_states, transitions)


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
    def __init__(self, state: set, marked: bool=False):
        self.state = state
        self.label = str(state)
        self.marked = marked
    
