######################################
### Estrutura de dado disjoint-set ###
######################################
#
# Sua implementação visa ao suporte do algoritmo de Kruskal, mais especificamente,
# na etapa de verificação de formação de ciclos. A implementação seguiu os passos 
# esclarecedores do professor Paulo Feofiloff (https://www.ime.usp.br/~pf/), cujas
# notas de aula sobre o assunto (https://www.ime.usp.br/~pf/analise_de_algoritmos/aulas/union-find.html)
# em muito contribuíram para a minha compreensão dos algoritmos.
#

def initialize(nodes):

    """
    _________________
    --- Descrição ---
    _________________

    Função responsável por inicializar lista de representantes e altura de cada nó. A princípio,
    todos os nós são chefes de si mesmo, e a partição das quais fazem parte (todos os nós 
    sendo disjuntos) tem altura zero.

    __________________
    --- Argumentos ---
    __________________

    - nodes : lista de nós (enumeração dos nós).

    ______________
    --- Saídas ---
    ______________

    - boss : lista de chefes de cada nó;

    - height : lista de alturas de cada nó.

    """

    boss = nodes.copy()
    height = [0 for _ in range(len(nodes))]
    
    return boss, height

def find(node, boss):

    """
    _________________
    --- Descrição ---
    _________________

    Função responsável por encontrar representante (nó de partição tal que é chefe de si mesmo) da 
    partição de um dado nó.

    __________________
    --- Argumentos ---
    __________________

    - node : nó (número do nó) de cuja partição se almeja encontrar o representante;

    - boss : lista de chefes de cada nó; 

    ______________
    --- Saídas ---
    ______________

    - represent: nó (número do nó) representante da partição de node;

    """
    
    represent = node
    while represent != boss[represent]:
        represent = boss[represent]
    
    return represent

def find_path_compression(node, boss):

    """
    _________________
    --- Descrição ---
    _________________

    Função responsável por encontrar representante (nó de partição tal que é chefe de si mesmo) da 
    partição de um dado nó, através do encurtamento de caminhos. Com essa heurística, define-se como
    chefe de um nó, o próprio representante da partição.

    __________________
    --- Argumentos ---
    __________________

    - node : nó (número do nó) de cuja partição se almeja encontrar o representante;

    - boss : lista de representantes da partição de cada nó; 

    ______________
    --- Saídas ---
    ______________

    - boss[node]: nó (número do nó) chefe de node;

    """
    
    if node != boss[node]:
        boss[node] = find_path_compression(boss[node], boss)

    return boss[node]

def union_rank(node0, node1, boss, height):

    """
    _________________
    --- Descrição ---
    _________________

    Função responsável pela união das partições de dois nós.

    __________________
    --- Argumentos ---
    __________________

    - node0 : primeiro nó (número do nó);

    - node1 : segundo nó (número do nó);

    - boss : lista de chefes de cada nó; 

    - height : lista de alturas de cada nó.

    ______________
    --- Saídas ---
    ______________

    None.

    """

    if node0 == node1:
        return print("União desnecessária, pois os nós são idênticos.")

    if height[node0] > height[node1]:
        boss[node1] = node0
    else:
        boss[node0] = node1
        if height[node0] == height[node1]:
            height[node1] = height[node0] + 1

    return

def components(nodes, edges):

    """
    _________________
    --- Descrição ---
    _________________

    Função (extra) responsável por definir o número de componentes disjuntas em um grafo.

    __________________
    --- Argumentos ---
    __________________

    - nodes : lista de nós (enumeração dos nós);

    - edges : lista de arcos.

    ______________
    --- Saídas ---
    ______________

    - cont: número de componentes do grafo.

    """

    cont = len(nodes)
    boss, height = initialize(nodes)

    for edge in edges:
        
        represent0 = find_path_compression(edge[0], boss)
        represent1 = find_path_compression(edge[1], boss)
        
        if represent0 != represent1:
            union_rank(represent0, represent1, boss, height)
            cont -= 1

    return cont

#################################################################
### Exemplo  do algoritmo de contagem de componentes em grafo ###
#################################################################

# nodes = list(range(9))
# edges = [[0, 1],
#          [0, 2],
#          [0, 5],
#          [0, 6],
#          [0, 7],
#          [1, 7],
#          [3, 4],
#          [3, 5],
#          [4, 5],
#          [4, 6],
#          [4, 7],
#          [6, 7]]

# print(components(nodes, edges))
