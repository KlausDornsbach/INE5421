from copy import deepcopy
from pprint import pprint
from typing import List, Set, Dict

class Grammar:
    def __init__(self, terminal : Set[str], nonterminal : Set[str], initial_symbol : str, productions : Dict[str,List[List[str]]]):
        self.terminal = terminal
        self.nonterminal = nonterminal
        self.initial_symbol = initial_symbol
        self.productions = productions
        self.first : Dict[str,Set[str]] = {x:set() for x in terminal | nonterminal}
        self.follow : Dict[str,Set[str]] = {x:set() for x in nonterminal}

    def refactor(self):
        pass

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


def main():
    # terminal = {'a','b','c','d'}
    # nonterminal = {'S','A','B'}
    # initial_symbol = 'S'
    # productions = {
    #     'S': [['A','b'],['A','B','c']],
    #     'A': [['a','A'],['&']],
    #     'B': [['b','B'],['A','d'],['&']]
    # }
    terminal = {'a','b'}
    nonterminal = {'S','A'}
    initial_symbol = 'S'
    productions = {
        'S': [['S','a'],['A','b']],
        'A': [['S','b'],['b']]
    }
    g = Grammar(terminal, nonterminal, initial_symbol, productions)
    g.generate_first()
    g.generate_follow()
    g.remove_left_recursion()
    pprint(g.first)
    pprint(g.follow)
    g.print()

if __name__ == '__main__':
    main()
