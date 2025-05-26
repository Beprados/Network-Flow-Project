from net_represent import *

def label_node_search(graph, s, t=None, search="breadth"):

    """
    _________________
    --- Descrição ---
    _________________

    Função que implementa algortimo de busca dos Nós Marcados. A ideia geral do
    algoritmo é a seguinte: inicialmente, todos os nós do grafo são desmarcados;
    então marca-se o nó de partida s; daí, são varridos os arcos admissíveis (s, j)
    - nó s marcado, e j desmarcado -, marcando-se os nós j; Repete-se o processo 
    para todos os nós marcados, até que não haja nenhum nó marcado com arcos
    admissíveis. Outra opção para o encerramento da função é alcançar nó objetivo t.

    __________________
    --- Argumentos ---
    __________________

    - graph : objeto da classe adj_list() representando grafo a ser percorrido;

    - s : nó (número do nó) de partida;

    - t : nó (número do nó) de destino. Por padrão, None;

    - search : string que delimita a ordem de prioridade na ordem de busca. Caso "breadth",
    realiza busca em profundidade. Caso contrário, busca em largura.

    ______________
    --- Saídas ---
    ______________

    - pred : lista de predecessores de cada nó do grafo ao longo do caminho encontrado.
    
    """

    mark = set([s])
    List = [s]
    pred = [None for _ in range(graph.N)]

    if search == "breadth":
        search_order = 0
    else: # == "depth search"
        search_order = -1

    while len(List) != 0:

        node = List[search_order]
        flag = False

        for edge in graph.adj[node]:

            trial_node = edge[0]

            if trial_node in mark:
                continue
            else:
                flag = True
                break
       
        if flag:

            mark.add(trial_node)
            List.append(trial_node)
            pred[trial_node] = node

            if trial_node == t:
                return pred
        else:
            List.pop(search_order)

    return pred

def descend_search(adj, pred, curr_node, descend, centroid=None):

    """
    _________________
    --- Descrição ---
    _________________

    Função recursiva para calcular o número de descendentes dos nós integrantes
    de uma árvore. 
    
    O algoritmo pode ser descrito da seguinte maneira: dado um nó,
    são varridos todos os nós a quem é ligado; à cada nó filho encontrado, a 
    busca por descendente é recursivamente chamada; cada chamada da função finaliza 
    apenas quando se alcança um nó que possui apenas ligação com seu antecessor,
    então seu número de descendentes é igual a 1; o nó original tem
    (número de descendentes) = (número de descendentes de seus filhos) + 1, logo
    à cada "volta" das chamadas recursivas atualiza-se o número de descentendes do
    nó atual como (número de descendentes de seus filhos) + 1.

    Ao longo da busca, mantém-se controle sobre os nós para checar se o centroide
    - primeiro nó o qual atinge um número de descendentes maior ou igual à metade
    do número de nós da árvore - já foi encontrado. Em caso afirmativo, não são
    aceitos nós que superam essa condição.

    __________________
    --- Argumentos ---
    __________________

    - adj : lista de adjacência da árvore;

    - pred : lista de predecessor para cada nó;

    - curr_node : nó (número do nó) em análise;

    - descend : lista do número de descendentes para cada nó;

    - centroid : nó (número do nó) centroide. Caso não tenha sido encontrado
    centroid = None.

    ______________
    --- Saídas ---
    ______________

    - centroid : nó (número do nó) centroide. Caso não tenha sido encontrado
    centroid = None.

    """

    for edge in adj[curr_node]:
        
        next_node = edge[0]
        
        if next_node == pred[curr_node]:
            if len(adj[curr_node]) > 1:
                continue
            else:
                
                descend[curr_node] += 1
                return centroid
        pred[next_node] = curr_node
        
        centroid = descend_search(adj, pred, next_node, descend, centroid)

        descend[curr_node] += descend[next_node]
    
    descend[curr_node] += 1

    if (descend[curr_node] >= len(adj)/2) and (centroid is None):
        centroid = curr_node

    return centroid

def centroid_search(adj, s=0):

    """
    _________________
    --- Descrição ---
    _________________

    Função auxiliar para iniciar a busca por descendentes dado um nó de
    partida em uma árvore. A função busca definir o centróde da árvore.

    ___________________
    --- Argummentos ---
    ___________________

    - adj : lista de adjacência da árvore;

    - s : nó (número do nó) de partida.

    ______________
    --- Saídas ---
    ______________

    - centroid : nó (número do nó) centroide.
    
    """

    n = len(adj)
    descend = [0 for _ in range(n)]
    pred = [0 for _ in range(n)]
    pred[0] = None
    centroid = descend_search(adj, pred, s, descend)

    return centroid

##########################################################
### Exemplo da aplicação do algoritmo dos Nós Marcados ###
##########################################################

# nodes = list(range(6))
# edges = [[0, 1, 0],
#          [0, 2, 0],
#          [1, 2, 0],
#          [1, 3, 0],
#          [1, 4, 0],
#          [2, 4, 0],
#          [3, 4, 0],
#          [3, 5, 0],
#          [4, 5, 0]]
# G = adj_list(nodes, edges)
# G.construct_adj_list()
# G.display()

# path = label_node_search(G, 0, 5)
# print(path)

###################################################
### Exemplo do algoritmo de busca por centróide ###
####################################################

# nodes = list(range(5))
# edges = [[0, 1, 0],
#          [0, 2, 0],
#          [0, 3, 0]
#          [1, 4, 0]]
# G = adj_list(nodes, edges, directed=False)
# G.construct_adj_list()
# G.display()

# centroid = centroid_search(G.adj, 0)
# print(f"Graph centroid: {centroid}")