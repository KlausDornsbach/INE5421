# Trabalho de Linguagens Formais e Compiladores - Analisador Léxico e Sintático

## Resumo:
Aplicação utilizada para construir e simular um analisador léxico e um analisador sintático (preditivo LL1), a partir de definições regulares e gramática arbitrárias, e realizar execução dos mesmos sobre textos fonte.

Desenvolvido por Bernardo Pasa Ribeiro, Klaus de Freitas Dornsbach e Eduardo Vicente Petry, como trabalho da disciplina EMC5421 - Linguagens Formais e Compiladores, do Curso      de Ciências da Computação da Universidade Federal de Santa Catarina.  

- Requisitos:
    - Python 3.5 ou mais recente

- Dependências:
    - se encontram no arquivo requirements.txt
    - para instalação, utilizar o comando (aconselha-se antes criar um ambiente virtual, mas não é requisito):
      - pip install -r requirements.txt

- Executar a aplicação:
    - python main.py (Windows)
    - python3 main.py (Linux)
  

## Execução e Funcionalidades:

- Interface de Projeto:

   Ao iniciar a aplicação, o usuário irá se deparar com a interface de projeto, cuja janela se dispõe na seguinte forma:
    
    ![interface_projeto](https://user-images.githubusercontent.com/48719874/134091436-a38f7aff-827b-410d-9959-5913ea149cb0.png)

   A parte 1, se refere as definições para o analisador léxico.
   
   Em 1a, há um campo onde são inseridas as definições regulares. A notação adotada para que a aplicação reconheça uma definição regular tem as seguintes formas:
   - Explícita:
        - identificador : [lista de símbolos separados por vírgulas]. Esse formato pode ser visto na definição 'S' na imagem acima.
   - Abreviada:
        - identificador : [a-z]. Formato que irá gerar a lista de caracteres de 'a' até 'z'. Também permite os seguintes casos [a-zA-Z], para todas letras maiúsculas e minúsculas e [0-9] para algarismos de 0 a 9. Outros padrões abreviados, não são aceitos.


    Em 1b, há o campo para inserção de padrões de tokens utilizando as definições regulares descritas em 1a. A notação tem a seguinte forma:
    
    - identificador : {identificador de uma definição regular}.
    
    Nota-se que operação de concatenação pode ser implícita, se definições regulares forem dispostas em sequência, como por exemplo '{S}{D}{S}'. As demais operações ('|', '*', '?' '+') devem ser explicitas.
    
    Em 1c, foi feito um campo separado para listagem de todos as palavras reservadas para os padrões de tokens definidos em 1b. A notação convencionada é a seguinte:
     
    - identificador do token da palavra reservada = identificador do token a qual a define : "lexema da palavra reservada".
    
    Nota-se, no entanto, que como não há validação dos campos de texto, cabe ao usuário inserir o identificador do token "pai" corretamente.

    A parte 2, se refere as definições para a gramática do analisador sintático.
    
    Em 2a, há o campo para inserção dos terminais da gramática, onde em cada linha deve-se colocar apenas um não terminal, entre chaves.
    
    Em 2b, temos o campo para definição da gramática. Em cada linha, deve-se inserir as produções de um não terminal no seguinte formato:
    - {cabeça_da_produção} -> produção_1 | produção_2 | ...... | produção_n
    
    Sendo que as produções irão contemplar tudo o que estiver entre |, e todos terminais e não terminais devem estar espaçados por um espaço em branco, sendo os não terminais caracterizados por estarem entre chaves, e o que não estiver entre chaves, será considerado como um terminal, como por exemplo na produção:
    - "{E} + {T}", onde 'E' e 'T' são não terminais e '+' é um terminal.

    O botão 'Simulador', gera o automato analisador léxico, a partir das definições inseridas em 1a, 1b e 1c, assim como a tabela de análise para um analisador sintático preditivo LL1, a partir da gramática definida em 2a, considerando os não terminais de 2b, e os terminais serão provenientes dos tokens definidos em 1b e 1c. 
    Caso seja possível eliminar recursões à esquerda, não determinismos diretos e indiretos, e a gramática cumpra as 3 condições para ser LL1, o programa irá prosseguir abrindo uma nova janela, a qual corresponde a Interface de Execução, onde são executadas as simulações dos analisadores gerados.&nbsp;
    
&nbsp;
- Interface de Execução:
    
    Ao iniciar a simulação, a seguinte interface será mostrada:
    
    ![interface_exec](https://user-images.githubusercontent.com/48719874/134095283-72104f35-e02e-4df6-a5bd-f9285522a910.png)

    Em relação ao campos, em 1 temos um campo para entrada do texto fonte sobre o qual serão realizadas as análises.
    
    Em 2, é mostrada a tabela de símbolos, contendo os pares, token - lexema. Esta sempre é inicializada com todas as palavras reservadas definidas anteriormente na Interface de Projeto, e será consultada e atualizada toda vez que um novo padrão não listado for identificado ao se realizar a análise de um texto fonte.
    
    Em 3, é ilustrada a lista de tokens em forma de tabela, a qual é preenchida anotando-se todas as referencias de um tokens, seu lexema e sua posição no texto fonte, conforme forem sendo encontrados na varredura do texto fonte.
    
    Em relação ao botões, o botão 'Analisar Léxico', serve para executar a análise léxica do texto fonte que estiver inserido em 1, preenchendo e consultando a tabela de símbolos em 2, e anotando as referências dos tokens em 3. Toda vez que este botão é acionado, o resultado da análise léxica anterior é automaticamente apagado, antes de realizar a nova análise.
    
    O botão 'Exibir tabela de parsing' irá abrir uma nova janela contendo a tabela de parsing do analisador preditivo LL1 gerada a partir da gramática definida na Interface de Projeto. A primeira coluna é preenchida com os não terminais e a primeira linha, com os terminais. As demais células, irão conter as produções, caso exista uma transição pelo par [terminal,não terminal] das respectivas linha e coluna que a célula pertença, ou estarão vazias caso não haja transição, representando uma entrada de erro. 
    
    O botão 'Analisar Sintático' executa a análise sintática sobre a lista de tokens produzida a partir da análise léxica sobre o texto fonte, e ao ser acionado irá abrir uma pequena janela informando caso o texto seja válido ou em caso de erro irá notificar qual foi o erro ocorrido.
    
    O botão 'Resetar Simulação' serve apenas para limpar as entradas da tabela de símbolos em 2 e da lista de tokens em 3. O texto fonte inserido em 1 não é apagado, e a tabela de parsing também não é afetada.
    
    Por fim, o botão 'Encerrar', serve para finalizar a simulação dos analisadores correntes, e retornar a aplicação para a janela principal, da Interface de Projeto, onde poderão ser feitas alterações nas definições léxicas e sintáticas, e posteriormente voltar a realizar outras simulação com possíveis novos analisadores léxico e/ou sintático gerados.
