from pprint import pprint
from grammar import Grammar

class Syntactic():
    def __init__(self, grammar: Grammar):
        self.grammar =  grammar
        self.parsing_table = dict()

    # inicializa a tabela de análise (dicionário)
    # sendo cada entrada formada por um conjunto contendo
    # um não terminal e um terminal (ou '$') da gramática
    def init_parsing_table(self, grammar: Grammar):
        parsing_table = dict()
        for nt in grammar.nonterminal:
            for t in grammar.terminal | {'$'}:
                parsing_table[frozenset({nt, t})] = []

        return parsing_table

    # método que aplica o algoritmo de gerar 
    # a tabela de análise mostrado em aula.
    def generate_parsing_table(self, grammar: Grammar):
        parsing_table = self.init_parsing_table(grammar)
        for head, prods in grammar.productions.items():
            for p in prods:
                if p[0] in grammar.terminal:
                    parsing_table[ frozenset( {head, p[0]} ) ] = p

                elif p[0] in grammar.nonterminal:
                    length = len(p)
                    # percorrer a sequência da produção
                    for i in range(length):
                        # incluir a produção na tabela para
                        # todo símbolo em first do NT (p[i])  
                        for a in grammar.first[ p[i] ] - {'&'}:
                            parsing_table[ frozenset( {head, a} ) ] = p

                        # condição para não continuar verificando 
                        # os próximos símbolos da produção
                        if '&' not in grammar.first[p[i]]:
                            break
                    
                    # condição para incluir a produção em
                    # nos terminais de follow da cabeça da produção
                    # (caso toda a sequência da produção seja anulável)
                    if i + 1 == length:
                        for a in grammar.follow[head]:
                            parsing_table[ frozenset( {head, a} ) ] = p

                elif p[0] == '&':
                    for a in grammar.follow[head]:
                        parsing_table[ frozenset( {head, a} ) ] = p

        self.parsing_table = parsing_table


def main():
    # gramática do miniteste 09
    terminal = {'b','c','e','f','v','com',';'}
    nonterminal = {'P','K','V','F','C'}
    initial_symbol = 'P'
    productions = {
        'P': [['K','V','C']],
        'K': [['c','K'],['&']],
        'V': [['v','V'],['F']],
        'F': [['f','P',';','F'],['&']],
        'C': [['b','V','C','e'],['com',';','C'],['&']]
    }
    g = Grammar(terminal, nonterminal, initial_symbol, productions)
    g.generate_first()
    g.generate_follow()

    s = Syntactic(g)
    s.generate_parsing_table(g)
    pprint(s.parsing_table)

if __name__ == '__main__':
    main()