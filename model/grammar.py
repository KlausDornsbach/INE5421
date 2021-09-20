from copy import deepcopy
from pprint import pprint
from typing import List, Set, Dict

class Grammar():
    def __init__(self, terminal : Set[str], nonterminal : Set[str], initial_symbol : str, productions : Dict[str,List[List[str]]]):
        self.terminal = terminal
        self.nonterminal = nonterminal
        self.initial_symbol = initial_symbol
        self.productions = productions
        self.first : Dict[str,Set[str]] = {x:set() for x in terminal | nonterminal}
        self.follow : Dict[str,Set[str]] = {x:set() for x in nonterminal}

    # aplica fatoracao a esquerda
    # retorna msg de erro, caso não seja 
    # possível fatorar (entrar em loop)
    def left_factoring(self) -> str:
        threshold = 10 * len(self.nonterminal) # limite arbitrario para interromper em caso de loop
        ordering = tuple(self.nonterminal)
        while threshold:
            threshold -= 1
            productions_copy = deepcopy(self.productions)
            for i,n in enumerate(ordering):
                # derivacoes sucessivas
                repeated = set() # guarda os simbolos da cabeça das produçoes que causam ND indireto
                prefixes = set()
                for p in self.productions[n]:
                    if p[0] in self.nonterminal:
                        for q in self.productions[p[0]]:
                            if q[0] in prefixes:
                                repeated.add(q[0])
                            else:
                                prefixes.add(q[0])

                # elimina ND's indiretos 
                # (substituindo os NT's por suas produções)
                if repeated:
                    new_productions = []
                    for r in repeated:
                        for p in self.productions[n]:
                            if p[0] in self.nonterminal:
                                # 'search' serve para filtrar apenas as produções que contem
                                # ND indireto, e que portanto devem ser modificadas.
                                search = set( [ q[0] for q in self.productions[p[0]] ] )
                                if r in search:
                                    # para cada produção 'q' do NT 'p[0]'
                                    # que gerou o ND indireto, inclui uma nova
                                    # produção em p, substituindo 'p[0]' por 'q'
                                    for q in self.productions[p[0]]:
                                        new = q + p[1:]
                                        new_productions.append(new)
                
                    self.productions[n] = new_productions
                
                # elimina nao determinismos diretos
                d = {x:[] for x in self.terminal}
                for p in self.productions[n]:
                    if p[0] in d:
                        d[p[0]].append(p)
                for x, prods in d.items():
                    if len(prods) > 1:
                        new_symbol = str(n) + "'"
                        self.nonterminal.add(new_symbol)
                        self.productions[new_symbol] = []
                        self.productions[n].append([x,new_symbol])
                        for p in prods:
                            self.productions[n].remove(p)
                            self.productions[new_symbol].append(p[1:])
            ordering = tuple(self.nonterminal)
            if self.productions == productions_copy: break

        if not threshold:
            return "FACTORING PANIC! (fatoração da gramática entrou em loop)"
        return ''

    # remove recursao a esquerda
    def remove_left_recursion(self):
        ordering = tuple(self.nonterminal)
        while True:
            productions_copy = deepcopy(self.productions)
            for i,n in enumerate(ordering):
                # derivacoes sucessivas
                for j in range(i):
                    for p in self.productions[n]:
                        if p[0] == ordering[j]:
                            self.productions[n].remove(p)
                            for q in self.productions[p[0]]:
                                self.productions[n].append(q+p[1:]) 
                # elimina recursoes diretas
                involved, not_involved = set(), set()
                for p in self.productions[n]:
                    if p[0] == n:
                        involved.add(tuple(p[1:]))
                    else:
                        not_involved.add(tuple(p))
                if involved:
                    new_symbol = str(n) + "'"
                    self.nonterminal.add(new_symbol)
                    self.productions[n] = [[*x,new_symbol] for x in not_involved]
                    self.productions[new_symbol] = [[*x,new_symbol] for x in involved]+[['&']]
            if self.productions == productions_copy: break

    # gera o conjunto first
    def generate_first(self):
        for x in self.terminal:
            self.first[x].add(x)
        while True:
            first_copy = deepcopy(self.first)
            for x in self.nonterminal:
                for p in self.productions[x]:
                    if p[0] in self.terminal | {'&'}:
                        self.first[x].add(p[0])
                    else:
                        for i in range(len(p)):
                            self.first[x].update(self.first[p[i]]-{'&'})
                            if '&' not in self.first[p[i]]: break
                        else:
                            self.first[x].add('&')
            if self.first == first_copy: break

    # gera o conjunto follow
    def generate_follow(self):
        self.follow[self.initial_symbol].add('$')
        while True:
            follow_copy = deepcopy(self.follow)
            for x in self.nonterminal:
                for p in self.productions[x]:
                    for i in range(len(p)-1):
                        if p[i] in self.nonterminal:
                            self.follow[p[i]].update(self.first[p[i+1]]-{'&'})
                            for j in range(i+1,len(p)-1):
                                if '&' in self.first[p[j]]:
                                    self.follow[p[i]].update(self.first[p[j+1]]-{'&'})
                    for i in range(len(p)-1,-1,-1):
                        if p[i] not in self.nonterminal: break
                        self.follow[p[i]].update(self.follow[x])
                        if '&' not in self.first[p[i]]: break
            if self.follow == follow_copy: break

    def print(self):
        for head, body in self.productions.items():
            print(f'{head} ::= {" | ".join(map("".join,body))}')


    # teste 3 (LL1) intersecção de firsts e follows
    def first_follow_intersection(self) -> str:
        derives_epsilon = [nt for nt in self.nonterminal if '&' in self.first[nt]]
        for nt in derives_epsilon:
            if self.first[nt].intersection(self.follow[nt]):
                return f'Gramática não é LL1! Intersecção de first e follow do não terminal {{nt}} não vazia!'

        return ''

    # aplica os 3 testes de verificação LL(1):
    # 1) remover recursao a esquerda
    # 2) fatorar 
    # 3) p/ todo NT que derive &: 
    #    First(NT) interseccçao Follow(NT) = []
    def is_LL1(self) -> str:
        # teste 1
        self.remove_left_recursion()
        
        # teste 2
        error = self.left_factoring()
        if error:
            return error
        
        # teste 3
        self.generate_first()
        self.generate_follow()
        error = self.first_follow_intersection()
        return error
  