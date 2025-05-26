import math
import networkx as nx
import matplotlib.pyplot as plt
from net_represent import *
from heap_graph import *
from disjoint_set import *

def kruskal(nodes, edges, sorted=False, shallow=False):

    """
    _________________
    --- Descrição ---
    _________________

    A função aplica o algoritmo de Kruskal para encontrar a árvore geradora mínima (AGM)
    de um grafo não direcionado. O algoritmo se desenvolve assim: inicialmente, ordenam-se 
    as arestas do grafo em ordem não decrescente de custo; insere-se cada uma delas à lista 
    de arestas da AGM, à medida que ciclos não são formados; caso o sejam, descarta-se a 
    aresta. O algoritmo encerra quando (número de arestas da AGM) = (número de nós do grafo) - 1 .

    __________________
    --- Argumentos ---
    __________________

    - nodes : lista de nós (enumerados);

    - edges : lista de arestas do grafo;

    - sorted : variável booleana que indica se edges já foi previamente ordenada.
    Por padrão, False.

    ______________
    --- Saídas ---
    ______________

    - tree_edges : lista de arestas da AGM;

    - cost : custo total da AGM.

    """

    if not sorted:
        heapsort_graph(edges, len(edges))
        edges.reverse()
        # edges.sort(key=aux_sort)

    boss, height = initialize(nodes)
    tree_edges = []
    cost = 0
    
    for edge in edges:

        node0 = edge[0]
        node1 = edge[1]

        direc0 = find(node0, boss)
        direc1 = find(node1, boss)

        if direc0 != direc1:
            tree_edges.append(edge)
            cost += edge[2]
            union_rank(direc0, direc1, boss, height)

    return tree_edges, cost 

def find_min_prim(visited, unvisited, adj, shallow=False):

    """
    _________________
    --- Descrição ---
    _________________

    Função auxiliar ao algortimo de Prim, é responsável por encontrar o arco (i, j)
    de menor custo, com i pertencente à primeira partição, e j à segunda.

    Ademais, aplica-se uma pequena modificação a qual prioriza, quando possível, a
    busca por AGM's rasas. Ao selecionar o arco mais barato (i, j), analisa-se se há mais
    de uma arco com o mesmo custo: em caso positivo, toma-se o arco cujo nó j possui mais 
    graus de saída; caso contrário, toma-se (i, j).

    __________________
    --- Argumentos ---
    __________________

    - visited : lista de nós representando a primeira partição;

    - unvisited : conjunto de nós representando a segunda partição;

    - adj : lista de adjacência representando o grafo;

    - shallow : valor booleano que condiciona o algoritmo de Prim a priorizar a AGM mais
    rasa. Por padrão, False.

    ______________
    --- Saídas ---
    ______________
    
    - node0 : nó (número do nó) i do arco mais barato (i, j);

    - node1 : nó (número do nó) j do arco mais barato (i, j);

    - minim : custo do arco mais barato (i, j). 

    """

    minim = math.inf
    node0, node1 = 0, 0

    if shallow:
        descend = 0

    for start_node in visited:
        for end_node, weight in adj[start_node]:
            if (end_node in unvisited):

                if shallow:
                    if (weight < minim):
                        node0 = start_node
                        node1 = end_node
                        descend = len(adj[end_node])
                        minim = weight
                        
                    elif (weight == minim) and (len(adj[end_node]) > descend):
                        node0 = start_node
                        node1 = end_node
                        descend = len(adj[end_node])
                        minim = weight
                    
                else:
                    if (weight < minim):
                        node0 = start_node
                        node1 = end_node
                        minim = weight

    return node0, node1, minim

def prim(nodes, adj, s=0, shallow=False):

    """
    _________________
    --- Descrição ---
    _________________

    A função aplica o algoritmo de Prim para encontrar árvore geradora mínima (AGM) de 
    um grafo não direcionado. O algoritmo funciona da seguinte maneira: particiona-se o
    grafo em dois, uma parte contendo o nó de partida s, e outra contendo os demais nós; 
    em seguida, procura-se o arco (s, j) de menor custo tal que j pertença à segunda 
    partição; adiciona-se j à primeira partição e exclui-se da segunda. Repete-se o 
    processo para os nós da primeira partição, até que a segunda se esvazie.

    Ademais, aplica-se uma pequena modificação a qual prioriza, quando possível, a
    busca por AGM's rasas. Ao selecionar o arco mais barato (i, j), analisa-se se há mais
    de uma arco com o mesmo custo: em caso positivo, toma-se o arco cujo nó j possui mais 
    graus de saída; caso contrário, toma-se (i, j).

    __________________
    --- Argumentos ---
    __________________

    - nodes : lista de nós (enumerados);

    - adj : lista de adjacência representando o grafo;

    - s : nó de partida. Como padrão, s = 0, isto é, o primeiro nó de nodes;

    - shallow : valor booleano que condiciona o algoritmo de Prim a encontrar a AGM mais
    rasa. Por padrão, False.

    ______________
    --- Saídas ---
    ______________

    - tree_edges : lista de arestas da AGM;

    - cost : custo total da AGM.

    """

    cost = 0
    visited = [s]
    unvisited = set(nodes)
    unvisited.remove(s)
    tree_edges = []

    while(len(unvisited) != 0):
        
        start_node, end_node, local_cost = find_min_prim(visited, unvisited, adj, shallow)
        start_node, end_node = int(start_node), int(end_node)

        tree_edges.append([start_node, end_node, local_cost])
        
        visited.append(end_node)
        unvisited.remove(end_node)
                
        cost += local_cost 
    
    return tree_edges, cost 

def prim_heap(nodes, adj, s=0, shallow=False):

    """
    _________________
    --- Descrição ---
    _________________

    A função aplica o algoritmo de Prim para encontrar a árvore geradora mínima (AGM) do
    grafo. Diferente da versão anterior, esta implementa estrutura heap na etapa de busca
    por menor custo - sob o intuito de otimizar o custo computacional.

    Ademais, aplica-se uma pequena modificação a qual prioriza, quando possível, a
    busca por AGM's rasas. Ao selecionar o arco mais barato (i, j), analisa-se se há mais
    de uma arco com o mesmo custo: em caso positivo, toma-se o arco cujo nó j possui mais 
    graus de saída; caso contrário, toma-se (i, j).

    __________________
    --- Argumentos ---
    __________________

    - nodes : lista de nós (enumerados);

    - adj : lista de adjacência representando o grafo;

    - s : nó de partida. Como padrão, s = 0, isto é, o primeiro nó de nodes;

    - shallow : valor booleano que condiciona o algoritmo de Prim a encontrar a AGM mais
    rasa. Por padrão, False.

    ______________
    --- Saídas ---
    ______________

    - tree_edges : lista de arestas da AGM;

    - cost : custo total da AGM.

    """

    cost = 0
    visited = set([s])
    unvisited = set(nodes)
    unvisited.remove(s)
    tree_edges = []
    
    fringe = []
    for edge in adj[s]:
        add_to_heap_graph(fringe, [s, edge[0], edge[1]])
    
    while(len(unvisited) != 0):
        
        while (len(fringe) != 0) and (fringe[0][1] in visited):
            extract_min_graph(fringe)

        if shallow:

            i = 1
            while i < len(fringe) and (fringe[0][2] == fringe[i][2]) and len(adj[fringe[i][1]]) > len(adj[fringe[i-1][1]]):
                i += 1
            start_node, end_node, local_cost = fringe[i-1]
            delete_elem_graph(fringe, i-1)
            
        else:
            start_node, end_node, local_cost = extract_min_graph(fringe)
        
        start_node, end_node = int(start_node), int(end_node)
        tree_edges.append([start_node, end_node, local_cost])
        
        visited.add(end_node)
        unvisited.remove(end_node)
        
        cost += local_cost

        for edge in adj[end_node]:
            if edge[0] not in visited:
                add_to_heap_graph(fringe, [end_node, edge[0], edge[1]])

    return tree_edges, cost 
    
def find_min_dijkstra(unmark, dist):

    minim = math.inf

    for i in range(len(unmark)):
        node = unmark[i]
        if dist[node] <= minim:
            minim = dist[node]
            minim_index = i
            minim_node = node

    return minim_index, minim_node

def dijkstra(nodes, adj, s=0):

    mark = []
    unmark = nodes.copy()

    dist = [math.inf for _ in range(len(nodes))]
    dist[s] = 0

    pred = [[] for _ in range(len(nodes))]
    pred[s].append(0)

    while len(mark) < len(nodes):

        minim_index, minim_node = find_min_dijkstra(unmark, dist) 
        mark.append(minim_node)
        unmark.pop(minim_index)

        for edge in adj[minim_node]:
            end_node, edge_weight = edge
            if end_node in unmark:
                if dist[end_node] > dist[minim_node] + edge_weight:
                    dist[end_node] = dist[minim_node]
                    pred[end_node].append(minim_node)
            else:
                continue
    
    tree_edges = []
    for i in range(1, len(pred)):
        beg_node = pred[i][0]
        end_node = i
        j = 0
        while adj[beg_node][j][0] != end_node:
            j += 1        
        tree_edges.append([beg_node]+adj[beg_node][j])


    return tree_edges

def direct_out_tree(nodes, adj, s=0):

    """
    _________________
    --- Descrição ---
    _________________

    Função para gerar, a partir de uma árvore não direcionada e um nó raiz, árvore 
    direcionada para fora.

    __________________
    --- Argumentos ---
    __________________

    - nodes : lista de nós (enumerados);

    - adj : lista de adjacência representando o grafo;

    - s : nó (número do nó) raiz da árvore direcionada;

    ______________
    --- Saídas ---
    ______________

    - new_edges : lista de arestas da árvore direcionada para fora;

    - pred : lista de predecessores de cada nó.

    """

    mark = set([s])
    List = [s]
    pred = [0 for _ in range(len(nodes))]
    new_edges = []

    while len(List) != 0:
        node=List.pop(0)
        for trial_node, weitgh in adj[node]:
            if trial_node not in mark:
                mark.add(trial_node)
                List.append(trial_node)
                pred[trial_node] = node
                new_edges.append([node, trial_node, weitgh])

    return new_edges, pred

#######################################################################
### Exemplo de aplicação dos algoritmos de AGM com exibição gráfica ###
#######################################################################

# nodes = [0, 1, 2, 3, 4, 5]
# edges = [[0, 1, 5], 
#          [0, 2, 6], 
#          [1, 2, 2],
#          [1, 4, 3],
#          [1, 3, 4],
#          [2, 4, 4],
#          [3, 4, 2],
#          [3, 5, 6],
#          [4, 5, 5]]
# G = adj_list(nodes, edges, directed=False)
# G.construct_adj_list()
# # tree_edges, cost = prim_heap(nodes, G.adj, True)
# # tree_edges, cost = prim(nodes, G.adj, True)
# tree_edges, cost = kruskal(nodes, edges)

# T = adj_list(nodes, tree_edges, directed=False)
# T.construct_adj_list()

# graph = nx.Graph()
# for edge in edges:
#     graph.add_edge(edge[0], edge[1], weight=edge[2])
# edge_labels1 = nx.get_edge_attributes(graph, 'weight')
# pos1 = {
#     0: (0, 0),
#     1: (2, 1),
#     2: (2, -1),
#     3: (4, 1),
#     4: (4, -1),
#     5: (6, 0),
# }


# tree = nx.Graph()
# for edge in tree_edges:
#     tree.add_edge(edge[0], edge[1], weight=edge[2])
# edge_labels2 = nx.get_edge_attributes(tree, 'weight')
# pos2 = {
#     0: (0, 0),
#     1: (2, 1),
#     2: (2, -1),
#     3: (4, 1),
#     4: (4, -1),
#     5: (6, 0),
# }

## Módulo de visualização ##
 
# fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# axs[0].set_title("Grafo original")
# nx.draw(graph, pos1, with_labels=True, node_color='lightsteelblue', node_size=1000, font_size=14,  ax=axs[0])
# nx.draw_networkx_edge_labels(graph, pos1, edge_labels=edge_labels1, ax=axs[0])

# axs[1].set_title("Árvore geradora mínima")
# nx.draw(tree, pos2, with_labels=True, node_color='lightsteelblue', node_size=1000, font_size=14, ax=axs[1])
# nx.draw_networkx_edge_labels(tree, pos2, edge_labels=edge_labels2, ax=axs[1])

# plt.tight_layout()
# plt.draw()
# plt.show()