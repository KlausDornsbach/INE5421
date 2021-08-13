# Trabalho 1 de Linguagens Formais e Compiladores - Analisador Léxico

## Resumo:
Aplicação utilizada para construir e simular um analisador léxico, a partir de definições regulares arbitrárias, e realizar execução do mesmo sobre textos fonte. 
Desenvolvido por Bernardo Pasa Ribeiro, Klaus de Freitas Dornsbach e Eduardo Vicente Petry, como trabalho 1 da disciplina EMC5421 - Linguagens Formais e Compiladores, do Curso      de Ciências da Computação da Universidade Federal de Santa Catarina.  

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
    
    ![interface_de_projeto](https://user-images.githubusercontent.com/48719874/129360768-715d13f8-25eb-4ceb-8703-86750d74e8df.png)

   Em 1, há um campo onde são inseridas as definições regulares. A notação adotada para que a aplicação reconheça uma definição regular tem as seguintes formas:
   - Explícita:
        - identificador : [lista de símbolos separados por vírgulas]. Esse formato pode ser visto na definição 'letter' na imagem acima.
   - Abreviada:
        - identificador : [a-z]. Formato que irá gerar a lista de caracteres de 'a' até 'z'. Também permite os seguintes casos [a-zA-Z], para todas letras maiúsculas e minúsculas e [0-9] para algarismos de 0 a 9. Outros padrões abreviados, não são aceitos.


    Em 2, há o campo para inserção de padrões de tokens utilizando as definições regulares descritas em 1. A notação tem a seguinte forma:
    
    - identificador : {identificador de uma definição regular}
    
    Nota-se que operação de concatenação é implícita, quando houverem definições regulares seguidas, como por exemplo {letter}{digit}, e as demais operações devem ser explicitadas       ('|', '*', '?' '+'), conforme pode ser visto no exemplo de 'id', em 2 na figura acima.
    
    Em 3, foi feito um campo separado para listagem de todos as palavras reservadas para os padrões de tokens definidos em 2. A notação convencionada é a seguinte:
     
    - identificador do token da palavra reservada = identificador do token a qual a define : "lexema da palavra reservada".
    
    Nota-se, no entanto, que como não há validação dos campos de texto, cabe ao usuário inserir o identificador do token "pai" corretamente.

    Em 4, temos o botão 'Simulador', que irá gerar o automato analisador léxico, a partir das definições inseridas em 1, 2 e 3. Ao ser acionado, o programa abre uma nova janela, a qual corresponde a Interface de Execução, onde é feita a simulação do analisador gerado.&nbsp;
    
&nbsp;
- Interface de Execução:
    
    Ao iniciar a simulação, a seguinte interface será mostrada:
    
    ![interface_de_execução](https://user-images.githubusercontent.com/48719874/129368385-abb89164-f0ca-423d-b605-e0309c06c6ec.png)

    Em 1, temos o campo para entrada do texto fonte sobre o qual será realizada a análise léxica.
    
    Em 2, é mostrada a tabela de símbolos, contendo os pares, token - lexema. Esta sempre é inicializada com todas as palavras reservadas definidas anteriormente na Interface de Projeto, e será consultada e atualizada toda vez que um novo padrão não listado for identificado ao se realizar a análise de um texto fonte.
    
    Em 3, é ilustrada a lista de tokens em forma de tabela, a qual é preenchida anotando-se todas as referencias de um tokens, seu lexema e sua posição no texto fonte, conforme forem sendo encontrados na varredura do texto fonte.
    
    Em 4, temos o botão 'Analisar Léxico', que serve para executar a análise léxica do texto fonte que estiver inserido em 1, preenchendo e consultando a tabela de símbolos em 2, e anotando as referências dos tokens em 3. Toda vez que este botão é acionado, o resultado da análise léxica anterior é automaticamente apagado, antes de realizar a nova análise.
    
    Em 5, há o botão 'Resetar Simulação', que serve apenas para limpar as entradas da tabela de símbolos em 2 e da lista de tokens em 3. O texto fonte inserido em 1, não será apagado.
    
    E por fim, em 6, há o botão 'Encerrar', serve para finalizar a simulação do analisador léxico corrente, e retornar a aplicação para a janela principal, da Interface de Projeto, onde poderão ser feitas alterações nas definições regulares, e posteriormente voltar a realizar uma nova simulação com um novo analisador léxico gerado.

    A figura abaixo, mostra um exemplo de resultado da execução do analisador léxico definido na primeira imagem, sobre o texto fonte fonte mostrado na imagem anterior:
    
    ![exemplo_execução](https://user-images.githubusercontent.com/48719874/129371099-09477109-69f4-46b5-8dda-98fde9d76530.png)


