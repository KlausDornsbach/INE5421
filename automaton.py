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
    def __init__(self, syntax_tree: syntax_tree.Node, leaf_list: list):
        self.alphabet = self.get_symbols(leaf_list)
        states, finals, transitions = self.build_automaton(syntax_tree, leaf_list, self.alphabet)
        self.init_state = 1 # id do estado inicial sempre vai ser igual por causa do algoritmo
        self.states = states
        self.final_states = finals
        self.transitions = transitions


    '''
    usado em: __init__
    :param leaf_list: lista de simbolos da ER
    :return: conjunto de simbolos formar o
        alfabeto do automato 
    '''
    def get_symbols(self, leaf_list) -> set:
        alphabet = set()
        for s in leaf_list:
            alphabet.add(s.value)

        alphabet.discard('#')
        return sorted(alphabet)

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
        # state_id (contador para identificar os estados)
        sid = 1
        
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

                    if not self.is_in_d_states(d_states, u):
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

            s = self.find_unmarked(d_states)

        ## converter as 'd_transiçoes' do algoritmo ER->AFD
        # para transiçoes com os indices numericos dos estados
        transitions = self.convert_transitions(states_map, d_transitions)

        # # só pra validacao, se quiser ver, uncomment        
        print('\ntransitions table:', end = '\n\n  |  ')
        for a in alphabet:
            print(f'{a}', end = '  |  ')
        for st in states:
            print(f'\n{st}', end = ' | ')
            for a in alphabet:
                if (st, a) in transitions.keys():
                    print(f'{transitions[(st, a)]}', end = ' | ')
                else:
                    print(' - ', end = ' | ') # sem transição            
        
        print(f'\n\ninitial: {initial_D.label}')
        print('finals:', final_states)
        
        return (states, final_states, transitions)


    '''
    função que converte as d_transitions do algoritmo
    ER -> AFD para transições com os estados pelo nº do estado
    '''
    def convert_transitions(self, states_map, d_transitions):
        transitions = dict()
        for k, v in d_transitions.items():
            transitions[k] = states_map[frozenset(v)]

        return transitions


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
    
