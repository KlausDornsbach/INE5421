class Automaton():
    '''
    um automato possui um dicionario de
    simbolos (alfabeto), lista de estados, cada
    estado representado por uma string, um 
    estado inicial.
    obs: as transicoes de estados estao em cada
        estado
    '''
    def __init__(self, syntax_tree, leaf_list):
        self.build_automaton(syntax_tree, leaf_list, ['a', 'b'])
    # def __init__(self, alphabet={}, states=[], init_state=None, final_states=[]):
    #     self.alphabet = alphabet
    #     self.states = states
    #     # self.transitions = transitions
    #     self.init_state = init_state
    #     self.final_states = final_states

    def find_unmarked(self, states):
        for s in states:
            if not s.marked:
                return s
        return next(iter(states))
    
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
    def build_automaton(self, sa_root, leaf_list, alphabet):
        # estados que farão parte do automato
        d_states = set()

        # estado inicial
        initial_D = State(sa_root.first_pos)
        d_states.add(initial_D)
        
        # loop 
        s = initial_D
        while s.marked == False:
            s.marked = True
            
            # for g in d_states:
                # print('once again: ')
                # print(f'from state {g.state}, transitions: {g.transitions}')
            for a in alphabet:
                s.transitions[a] = set()
                u = set()
                
                for state_index in s.state:
                    if leaf_list[state_index].value == a:
                        u = u | leaf_list[state_index].follow_pos
                
                if not self.is_in_d_states(d_states, u):
                    # new state
                    new_state = State(u)
                    d_states.add(new_state)
                    # s = new_state
                
                s.transitions[a] = s.transitions[a] | u
                print(s)
                # print(f'from state {s.state}, transitions: {s.transitions}')
            # print(d_states)
            s = self.find_unmarked(d_states)

        # print(d_states)
        
        for g in d_states:
            print(f'from state {g.state}, transitions: {g.transitions}')

    

class State():
    '''
    um estado possui um conjunto indices de
    folha da arvore de sintaxe e uma lista 
    de transicoes, representada por um dicionario 
    cuja key = elemento do alfabeto e
    value = conjunto de estados (labels)
    estados vem com uma marca, pra ajudar na
    hora de implementar o build_automaton
    '''
    def __init__(self, state: set, transitions: dict = {}, marked=False):
        self.state = state
        self.transitions = transitions
        self.marked = marked
        print(transitions)
    
