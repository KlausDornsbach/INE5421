from pprint import pprint
from grammar import Grammar

class Syntactic():
    def __init__(self, grammar: Grammar):
        self.grammar =  grammar
        self.parsing_table = dict()

    # método que aplica o algoritmo de gerar 
    # a tabela de análise mostrado em aula.
    def generate_parsing_table(self, grammar: Grammar):
        parsing_table = {nt: dict() for nt in grammar.nonterminal}
        for head, prods in grammar.productions.items():
            for p in prods:
                if p[0] in grammar.terminal:
                    parsing_table[head][p[0]] = p

                elif p[0] in grammar.nonterminal:
                    length = len(p)
                    # percorrer a sequência da produção
                    for i in range(length):
                        # incluir a produção na tabela para
                        # todo símbolo em first do NT (p[i])  
                        for a in grammar.first[ p[i] ] - {'&'}:
                            parsing_table[head][a] = p

                        # condição para não continuar verificando 
                        # os próximos símbolos da produção
                        if '&' not in grammar.first[p[i]]:
                            break
                    
                    # condição para incluir a produção em
                    # nos terminais de follow da cabeça da produção
                    # (caso toda a sequência da produção seja anulável)
                    if i + 1 == length:
                        for a in grammar.follow[head]:
                            parsing_table[head][a] = p

                elif p[0] == '&':
                    for a in grammar.follow[head]:
                        parsing_table[head][a] = p

        self.parsing_table = parsing_table

    def validate_sentence(self, sentence: str):
        # inicia a pilha
        stack = ['$', self.grammar.initial_symbol]
        # parse a sentença (itens vem espaçacos na string):
        sentence = sentence.split()
        sentence.append('$')
        i = 0
        print('sentence: ', sentence, '\n')
        print('stack: ', stack)
        while(1):
            # item na sentenca
            if i >= len(sentence):
                print('not accepted (reach end)')
            sentence_item = sentence[i]
            if stack[-1] in self.grammar.terminal | {'$'}:
                if stack[-1] == '$' and sentence_item == '$':
                    print('GREAT SUCCESS!')
                    break
                elif stack[-1] != sentence_item:
                    print('not accepted (top of stack terminal != sentence[i])')
                    break
                else:
                    i += 1
                    stack.pop()
                    print('sentence: ', sentence[i:], '\n')
                    print('stack: ', stack)
            # eh nonterminal
            else:
                try:
                    parsing_table_list = self.parsing_table[stack[-1]][sentence_item]
                    if parsing_table_list == []:
                        print('not accepted ([])')
                        break
                    else:
                        # desempilha
                        if parsing_table_list[0] == '&':
                            print('stack: ', stack)
                            stack.pop()
                        # add elementos de acordo com tabela em ordem decrescente
                        else:
                            stack.pop()
                            for j in range(len(parsing_table_list)-1, -1, -1):
                                stack.append(parsing_table_list[j])
                            print('stack: ', stack)

                except KeyError:
                    print('not accepted (key error)')
                    break


def main():
    # gramática do miniteste 10
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

    sentence = 'c v f b e ;'
    s.validate_sentence(sentence)

    # gramatica miniteste 09   
    # terminal = {'a', 'b', 'c', 'd'}
    # nonterminal = {'S', 'A', 'B', 'C', 'D'}
    # initial_symbol = 'S'
    # productions = {
    #     'S': [['A', 'B']],
    #     'A': [['a','B','A'],['&']],
    #     'B': [['C','D']],
    #     'C': [['b','D','C'],['&']],
    #     'D': [['c','S','c'],['d']]
    # }
    # g = Grammar(terminal, nonterminal, initial_symbol, productions)
    # g.generate_first()
    # g.generate_follow()

    # s = Syntactic(g)
    # s.generate_parsing_table(g)
    # pprint(s.parsing_table)

    # sentence = ''
    # s.validate_sentence(sentence)

    # gramatica Exemplo construção preditivo LL(1) semana 11
    # terminal = {'+', '*', '(', ')', 'id'}
    # nonterminal = {'E', 'T', 'F'}
    # initial_symbol = 'E'
    # productions = {
    #     'E': [['E', '+', 'T'], ['T']],
    #     'T': [['T', '*', 'F'], ['F']],
    #     'F': [['(', 'E', ')'], ['id']]
    # }
    # g = Grammar(terminal, nonterminal, initial_symbol, productions)
    # # problema nas strings de nomes gerados no remove left recursion
    # # (T -> T')
    # g.remove_left_recursion()
    # g.left_factoring()
    
    # g.generate_first()
    # g.generate_follow()

    # s = Syntactic(g)
    # s.generate_parsing_table(g)
    # pprint(s.parsing_table)

if __name__ == '__main__':
    main()