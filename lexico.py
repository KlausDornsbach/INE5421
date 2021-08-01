# definimos classe de automatos, podem ser
# deterministicos ou não, epsilon transicoes
# sao representadas como &
class Automata():
    # um automato possui um dicionario de
    # simbolos (alfabeto), lista de estados, 
    # um estado inicial, uma lista de transicoes
    # representada por um dicionario que mapeia
    # tuplas de estado + simbolo para um estado:
    # transicao[(q1, a)] = q3
    # q1, q3 \in states, a \in alphabet
    def __init__(self, alphabet={}, states=[], init_state=None, transitions={}, final_states={}):
        self.alphabet = alphabet
        self.states = states
        self.transitions = transitions
        self.init_state = init_state
        self.final_states = final_states

class SyntaxTree():
    # a arvore de sintaxe possui um dicionario
    # que mapeia definicoes regulares para 
    # alfabetos, esses alfabetos podem ser
    # definicoes regulares com alfabetos internos
    def __init__(self, expression, dictionaries):
        # alfabeto-> digit : [0, 1, ..., 9]
        # regular definition-> id : letter(letter|digit)*
        dict_entry = self.parse_expression(expression)
        dictionaries.append(dict_entry)
        # self.automata = Automata() 
    
    # parseio a expressao, coloco nome associado
    # a uma lista de simbolos usados na definicao
    # através de dicionario
    def parse_regex(self, expression):
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
                print('parse error! please input regex in correct format')
        return {key : alphabet}
    
    # usado na definicao de tokens, ex.: 
    # id : letter(letter|digit) 
    def parse_token_definition(self, token):
        pass

class Lexico():
    # transformar gramatica livre de contexto
    # em um autômato que nos permita reconhecer
    # a classe de um lexema
    def regex_to_afd(self, file):
        pass
    
    # juntar afd's 
    def afd_union(self, afd):
        pass
    
    # determinizacao de automato
    def det_automata():
        pass
    
    # ler um texto e dar output em uma lista:
    # padrao, lexema, indice no arquivo
    def create_symbol_table(self, file):
        pass



def main():
    st = SyntaxTree('letter_ : [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o]')


if __name__ == '__main__':
    main()