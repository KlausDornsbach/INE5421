
from print_tree import print_tree
import automaton

## por enquanto a arvore consiste apenas de nodos ligados
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.father = None
        self.nullable = False
        self.last_pos = set()
        self.first_pos = set()
        self.follow_pos = set()

## TODO: modificar regra para identificar os simbolos
#        de um alfabeto proveniente das definições regulares(?)
def is_operand(c: str, alphabet=None) -> bool:
	return c.isalnum() or c in {'#', '&'}

def is_operator(c: str) -> bool:
	return c in {'*', '|', '.', '?'}

def parse_regex(re: str) -> str:
    """
    Adequa o regex de entrada para o construtor da árvore sintática 
    Obs: não leva em consideração erros
    Obs2: considera-se que operandos em sequencia representam uma
         concatenação implícita. Exemplo 'abb' = 'a.b.b'
    Obs3: caso encontre operador '?' substitui por '| &' 
        incluindo na expressão os parenteses que respeitem
        as precedencias anteriores
    :param re: expressão regular qualquer (input)
    :return: expressão regular 'parseada'
    """

    # regex
    re = '(' + re + ')#.'
    # parsed regex 
    pre = re[0]

    # primeiro simbolo não é analisado
    # (supõe-se que a regex é valida)
    """
    obs: a lógica aqui é basicamente tomar as decisões com base
        no caractere atual da regex de entrada ( re[i] ) com o último
        da regex parseada ( pre[-1] )
    """
    for i in range(1, len(re)):

        # adiciona operador concat explicito na regex
        # cobre os casos:  
        #   ')(' -> ') . (' 
        #   'aaa' -> 'a . a . a'
        #   'a*b' -> 'a* . b'
        if (is_operand(re[i]) or re[i] == '(') and (is_operand(pre[-1]) or pre[-1] in {'*', ')'} ):
            pre += '.' + re[i]

        # copiar diretamente (exceto para '?')
        elif re[i] in {'(', ')'} or is_operator(re[i]) or is_operand(re[i]):
            
            # substituir operador '?' por ' ( _subexpressão_ |&) . '
            # obs: a inclusão dos parenteses é necessaria para
            #   garantir a formação da arvore de forma correta
            #   a partir do algoritmo utilizado para a arvore
            if re[i] == '?':
                
                # ajustar precedencia da operação |& com parenteses já existentes
                j = len(pre) - 1
                # buffer para restaurar a regex
                buf = ''
                # contador de parenteses
                parenteses = 0
                
                # a leitura da expressao obtida até então em 'pre' é feita 
                # de trás para frente, para poder identificar as aberturas
                # e fechamentos dos parenteses na expressão (se existirem)
                while j > -1:

                    if not is_operand(pre[j]) or parenteses:
                        buf = pre[j] + buf

                        # contagem de parenteses existentes
                        if pre[j] == ')':
                            parenteses += 1
                        elif pre[j] == '(':
                            parenteses -= 1

                            # se fechar todos parenteses encontrados
                            # então foi encontrada a posição para abrir
                            # o novo '('
                            if parenteses == 0:
                                j = -1
                                break
                        
                        j -= 1

                    # caso em que encontra uma posição para 
                    # abrir o parenteses, e não se encontrou
                    # nenhum ()'s no caminho
                    else:
                        pre = pre[0 : j-1] + '(' + buf
                        break

                # indica que foram encontrados parenteses teve que ser 
                # e haviam outros parenteses no meio
                if j == -1:

                    # se nao pegou toda a expressao em 'buf',
                    # restaura a parte anterior ao que tiver em 'buf'
                    if len(pre) > len(buf):
                        pre = pre[:(len(pre) - len(buf))] + '(' + buf
                    else:
                        pre = '(' + buf

                pre += '|&).'
                # aqui termina o tratamento da substituição de '?'

            # caso re[i] válido e != '?'  
            else:
                pre += re[i]

        # caso re[i] inválido. ignorar caractere.
        # exemplo: espaços em branco
        else:
            continue
    
    return pre


"""
Algoritmo adaptado de:
https://www.geeksforgeeks.org/program-to-convert-infix-notation-to-expression-tree/?ref=rp
"""
def build_ST(re: str) -> Node:
    """
    Retorna a árvore sintática de uma dada expressão 
    regular parseada (por parse_regex()) na forma infixa.
    Obs: não trata caso de expressão mal formada 
        (parenteses fora de ordem, etc)
    :param re: expressão regular em notação infixa(operadores entre operandos)
    :return: nodo raiz da árvore sintatica
    """
    # node stack
    ns = [] 
    # char stack
    cs = []
    # precedences
    pcd = {')': 0, '|': 1, '.': 2, '*': 3}

    for i in range(len(re)):

        # Push '(' in char stack
        if re[i] == '(':
            cs.append(re[i])
        
        # Push the operands in node stack
        elif is_operand(re[i]):
            new = Node(re[i])
            ns.append(new)

        # If an operator with lower or
        # same associativity appears
        elif pcd[re[i]] > 0:

            while cs and cs[-1] != '(' and pcd[cs[-1]] >= pcd[re[i]]: 

                # Get and remove the top element
                # from the character stack
                father = Node(cs.pop())

                # Get and remove the top element
                # from the node stack;
                # Update the tree

                ## Treat unary operator case: single child (left)
                if father.value == '*':
                    father.right = None
                else:
                    father.right = ns.pop()
 
                father.left = ns.pop()

                # Push the node to the node stack
                ns.append(father)

            # Push re[i] to char stack
            cs.append(re[i])
        
        elif re[i] == ')':

            while cs and cs[-1] != '(':
            
                father = Node(cs.pop())

                if father.value == '*':
                    father.right = None
                else:
                    father.right = ns.pop()

                father.left = ns.pop()
                ns.append(father)
            
            cs.pop()
    
    father = ns[-1]
    return father


def specify_nodes(as_root: Node) -> (Node, list):
    '''
    gera valores nullable, firstpos, lastpos e followpos
    percorrendo a ST em pós ordem: filho esquerda, filho 
    direita e pai. 
    :param as: arvore sintática gerada no passo anterior
    :return Node: arvore modificada
    :return list: lista de folhas
    '''
    stack = []
    leaf_counter = 0

    stack.append(as_root)

    # essa lista serve pra armazenar nodos folha
    # é usada na definicao de followpos
    leaf_list = []
    # 
    while(stack):
        curr_node = stack.pop()
        # caso seja folha
        if is_operand(curr_node.value):
            if curr_node == '&':
                curr_node.nullable = True
            else:
                curr_node.nullable = False
                curr_node.last_pos.add(leaf_counter)
                curr_node.first_pos.add(leaf_counter)
                leaf_counter += 1
                leaf_list.append(curr_node)

        # caso seja operacao
        else:
            # checo se filhos já tem fpos definido 
            # entao sei que posso definir lpos e fpos do
            # nodo de operacao
            if curr_node.left.first_pos != set():
                # faz testes pra cada tipo de operacao
                cn = curr_node
                r = cn.right
                l = cn.left
                if cn.value == '|':
                    cn.nullable = l.nullable or r.nullable
                    cn.first_pos = l.first_pos | r.first_pos
                    cn.last_pos = l.last_pos | r.last_pos

                if cn.value == '*':
                    cn.nullable = True
                    cn.first_pos = l.first_pos
                    cn.last_pos = l.last_pos
                for i in cn.first_pos:                      # followpos
                    for j in cn.last_pos:
                        leaf_list[i].follow_pos.add(j)
                    
                if cn.value == '.':
                    cn.nullable = l.nullable and r.nullable
                    if l.nullable:
                        cn.first_pos = l.first_pos | r.first_pos
                    else:
                        cn.first_pos = l.first_pos
                    if r.nullable:
                        cn.last_pos = l.last_pos | r.last_pos
                    else:
                        cn.last_pos = r.last_pos
                    for r_node_index in r.first_pos:        # followpos
                        for l_node_index in l.last_pos:
                            leaf_list[l_node_index].follow_pos.add(r_node_index)

            else:
                stack.append(curr_node)
                if curr_node.right != None:
                    stack.append(curr_node.right)
                stack.append(curr_node.left)
    
    return (as_root, leaf_list)


def print_recursively(root: Node):
    if(root.left != None):
        print_recursively(root.left)
    if(root.right != None):
        print_recursively(root.right)
    print('########\n', root.value)
    # print(root.follow_pos)
    print(root.nullable)
    print(root.first_pos)
    print(root.last_pos)

# Teste
def main():
    # regexes testados (agaora todos OK!)
    regex = '(a | b)*abb'
    # regex = '(a | b) ? (a| b)?aa'
    # regex = 'a|b* a'
    # regex = 'a|b|c'
    # regex = 'a|b|(c|d)'
    # regex = 'abba|cd'

    # exemplos da verificaçao de apredizagem 09
    # regex = '(& | b)(ab)*(& | a)'
    # regex = 'a(a | b)* a'
    # regex = 'a a *(bb*aa*b)*'

    # miniteste 06
    # regex = '(a | b)? (a| b)* aa'

    print('Input regex: ', regex, '\n')

    regex = parse_regex(regex)
    print('Parsed regex: ', regex, '\n')

    syntax_tree = build_ST(regex)
    print_tree(syntax_tree)
    
    # buildo nullable, lpos, fpos, followpos
    (syntax_tree, leaf_list) = specify_nodes(syntax_tree)
    
    # VALIDACAO, se quiser ver, uncomment
    # print_recursively(syntax_tree)
    # print('----------------------------')
    # testando followpos
    # for i in leaf_list:
    #     print(i.value)
    #     print(i.follow_pos) 

    # buildo automato
    auto = automaton.Automaton(syntax_tree, leaf_list)

if __name__ == '__main__':
    main()
