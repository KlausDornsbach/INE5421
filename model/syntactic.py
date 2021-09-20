from pprint import pprint
from typing import Tuple, List
# from grammar import Grammar
from model.grammar import Grammar

class Syntactic():
    def __init__(self):
        self.grammar = None
        self.parsing_table = dict()

    def clear(self) -> None:
        self.grammar = None
        self.parsing_table = dict()

    def make(self, nonterminals: List[str], terminals: List[str], productions: dict) -> str:
        """
        método que inicializa o analizador sintático, 
        primeiro criando a gramática a partir dos NT's
        terminais (tokens), e das produções da gramática,
        e depois chama o método para gerar a tabela de 
        análise.
        param return: string contendo msg de erro se
                    tiver algum problema na gramática (não
                    ser fatorável, ou não ser tipo LL(1)),
                    ou na geração da tabela de análise.
                    retorna uma string vazia em caso de sucesso.
        """
        # OBS: se assume que o simbolo inicial é sempre o primeiro NT listado
        g = Grammar(set(terminals), set(nonterminals), nonterminals[0], productions)
        error = g.is_LL1()
        if error:
            return error

        self.grammar = g
        self.generate_parsing_table(g)
        return error

    # método que aplica o algoritmo de gerar 
    # a tabela de análise mostrado em aula.
    def generate_parsing_table(self, grammar: Grammar):
        parsing_table = {nt: dict() for nt in grammar.productions.keys()}
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

    def validate_sentence(self, sentence: List[str]) -> Tuple[bool, str]:
        # variaveis de controle, para evidenciar casos de erro
        result, description = False, ''
        # inicia a pilha
        stack = ['$', self.grammar.initial_symbol]
        # insere '$'no fim da sentença (lista de tokens da analise léxica):
        sentence.append('$')
        i = 0
        print('sentence: ', sentence, '\n')
        print('stack: ', stack)
        while(1):
            # item na sentenca
            if i >= len(sentence):
                description = 'Sentença atingiu o fim mas não foi aceita.'
                break
            sentence_item = sentence[i]
            if stack[-1] in self.grammar.terminal | {'$'}:
                if stack[-1] == '$' and sentence_item == '$':
                    description = 'GREAT SUCCESS! A sentença é válida!'
                    result = True
                    break
                elif stack[-1] != sentence_item:
                    description = f'Não aceitou: (topo da pilha {stack[-1]} != {sentence[i]})'
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
                        description = 'Não aceitou. Atingiu um campo vazio na tabela de parsing.'
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
                    description = 'Não aceitou. Entrada da tabela de parsing inválida.'
                    break
        
        return result, description