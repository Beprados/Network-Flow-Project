import numpy as np
import networkx as nx
from numba import njit
import matplotlib.pyplot as plt
from net_represent import *
from min_span_tree import *
from search import *
from tree_plot import *


def size(data):

    """
    _________________
    --- Descrição ---
    _________________

    Função para calcular tamanho de vetores e matrizes.

    __________________
    --- Argumentos ---
    __________________

    - data : lista ou lista de listas.

    ______________
    --- Saídas ---
    ______________

    - sum_size : número de elementos em data.

    """

    if type(data[0]) != list:
        sum_size = len(data)
            
    else:
        sum_size = 0
        for elem in (data):
            sum_size += len(elem)
    
    return sum_size
 
def diff(vec_0, vec_1):

    """
    _________________
    --- Descrição ---
    _________________

    Função para gerar vetor sinlaizador de diferenças dado dois vetores de mesmo 
    tamanho. Caso haja difença na entrada j, a entrada j do vetor de diferença será 1,
    senão, 0.

    __________________
    --- Argumentos ---
    __________________

    - vec_0 : primeira lista da comparação.

    - vec_1 : segunda lista da comparação.

    ______________
    --- Saídas ---
    ______________

    - diff_vec : lista de diferença nas entradas.

    """

    cols = len(vec_0)
    diff_vec = []

    for i in range(cols):
        diff_vec.append(int(vec_0[i]!=vec_1[i]))

    return diff_vec

def find_diff(vec_0, vec_1):

    """
    _________________
    --- Descrição ---
    _________________

    Função para definir, em um vetor 1, a localização de entradas destoantes e o 
    valor destoante, tomando um vetor 0 como referência.

    __________________
    --- Argumentos ---
    __________________

    - vec_0 : lista representando o vetor referência.

    - vec_1 : lista representando o vetor destoante.

    ______________
    --- Saídas ---
    ______________

    - opt_vec : lista contendo localização de entradas destoantes e o valor 
    destoante.

    """

    cols = len(vec_0)
    opt_vec = []

    for i in range(cols):
        if vec_0[i]-vec_1[i]:
            opt_vec += [i, vec_1[i]]

    return opt_vec

def find_fix(opt_matrix, centroid, node):

    """
    _________________
    --- Descrição ---
    _________________

    Função para definir os consertos necessários para reconstruir um vetor da 
    matriz original.

    __________________
    --- Argumentos ---
    __________________

    - opt_matrix : lista de listas representando matriz de armazenamento ótima;
    
    - centroid : nó (número do nó) centroide da árvore geradora mínima (AGM) 
    de similaridade, representando o vetor referência;

    - node : nó (número do nó) representando vetor que se almeja reconstruir.

    ______________
    --- Saídas ---
    ______________

    - fix : lista indicando os consertos necessários para a reconstrução.

    """

    vec = opt_matrix[node]
    pred_node = vec[0]

    fix = tuple([])
    while(pred_node != centroid):
        if len(vec) > 1:
            fix = tuple(vec[1:]) + fix
        vec = opt_matrix[pred_node]
        pred_node = vec[0]

    fix = tuple(vec[1:]) + fix

    return fix

def edges_constructor(matrix):

    """
    _________________
    --- Descrição ---
    _________________

    Função para construir os arcos do grafo de similaridade. São calculadas todas
    as possíveis diferenças entre vetores (linhas) da matriz, dadas pelas combinações dois 
    a dois.

    __________________
    --- Argumentos ---
    __________________

    - matriz : lista de listas, em que cada linha corresponde a um dado.

    ______________
    --- Saídas ---
    ______________

    - edges : lista de arestas.

    """

    rows = len(matrix)
    edges = []
    
    for i in range(rows):
        for j in range(i+1, rows):
            diff_vec = diff(matrix[i], matrix[j])
            local_cost = sum(diff_vec)
            edges.append([i, j, local_cost])

    return edges

def aux_edges_constructor_numba(matrix):

    rows = len(matrix)
    cols = len(matrix[0])
    edges = []
    
    for i in range(rows):
        for j in range(i+1, rows):

            diff_vec = np.empty(len(matrix[0]), dtype=np.int64)

            for k in range(cols):
                diff_vec[k] = matrix[i][k]!=matrix[j][k]

            local_cost = sum(diff_vec)
            edges.append([i, j, local_cost])

    return edges

edges_constructor_numba = njit(aux_edges_constructor_numba)

def opt_matrix_constructor(matrix, pred_list, centroid):

    """
    _________________
    --- Descrição ---
    _________________

    Função para construir matriz de armazenamento ótima.

    __________________
    --- Argumentos ---
    __________________

    - matrix : lista de listas com os dados originais;

    - pred_list : lista de predecessores para cada nó (representando um 
    vetor da matriz original); 

    - centroid : nó (número do nó) centroide da árvore geradora mínima (AGM) 
    de similaridade, representando o vetor referência.

    ______________
    --- Saídas ---
    ______________

    - opt_matrix : lista de lista representando matriz de armazenamento ótima.

    """

    rows = len(matrix)
    opt_matrix = [[] for _ in range(rows)]
    opt_matrix[centroid] = matrix[centroid]

    for i in range(centroid):
        node_pred = pred_list[i]
        pred = matrix[node_pred]
        son = matrix[i]

        opt_matrix[i] += [node_pred] + find_diff(pred, son)

    for i in range(centroid+1, rows):
        node_pred = pred_list[i]
        pred = matrix[node_pred]
        son = matrix[i]

        opt_matrix[i] += [node_pred] + find_diff(pred, son)

    return opt_matrix

def reconstruct_vector(opt_matrix, centroid, node):

    """
    _________________
    --- Descrição ---
    _________________

    Função para reconstruir vetor da matriz original.

    __________________
    --- Argumentos ---
    __________________

    - opt_matrix : lista de listas representando matriz de armazenamento ótima;

    - centroid : nó (número do nó) centroide da árvore geradora mínima (AGM) 
    de similaridade, representando o vetor referência;

    - node : nó (número do nó) representando vetor que se almeja reconstruir.

    ______________
    --- Saídas ---
    ______________

    - real_vec : lista representando vetor reconstruído.

    """

    real_vec = opt_matrix[centroid].copy()

    if node != centroid:

        fix = find_fix(opt_matrix, centroid, node)
        size_fix = len(fix)
        
        if size_fix != 0:
            for i in range(0, size_fix, 2):
                aux_index = fix[i]
                aux_fix = fix[i+1]
                real_vec[aux_index] = aux_fix

    return real_vec

def str_reduction(n, m, k):

    aux0 = (m-2)/m
    aux1 = 2*(k**m) + m - 3
    aux2 = aux1/(m*n)
    aux3 = aux0 - aux2

    return aux3*100


###################################################################
### Exemplo de otimização de armazenamento com exibição gráfica ### 
###################################################################

## Geração do conjunto de vetores ##

# rng = np.random.default_rng(seed=0)
# m = 4
# n = 30
# matrix = rng.choice([0, 1], (n, m), p=[0.5, 0.5]).tolist()

## Construção do grafo de diferenças ##

# nodes = list(range(len(matrix)))
# edges = edges_constructor_numba(np.array(matrix))
# G = adj_list(nodes, edges, directed=False)
# G.construct_adj_list()

## Busca por Árvore Geradora Mínima (AGM) não orientada ##

# aux_edges, cost = prim_heap(nodes, G.adj, s=0, shallow=True)
# aux_T = adj_list(nodes, aux_edges, directed=False)
# aux_T.construct_adj_list()

## Localização do centróide e direcionamento da AGM ## 

# centroid = centroid_search(aux_T.adj, s=np.random.randint(low=0, high=G.N))
# tree_edges, pred_list = direct_out_tree(nodes, aux_T.adj, s=centroid)
# T = adj_list(nodes, tree_edges, directed=True)
# T.construct_adj_list()

## Construção da matriz de armazenamento ótimo ##

# opt_matrix = opt_matrix_constructor(matrix, pred_list, centroid)

# print(f"Original matrix size: {size(matrix)}\
#       \nOpt. matrix size: {size(opt_matrix)}\
#       \nStorage reduction: {(1 - (size(opt_matrix)/size(matrix)))*100}%\
#       \nMST cost: {cost}")

# print("\nOriginal matrix:\n")
# for lin in matrix:
#     print(lin, sep="")
# print("\n\nOpt. matrix:\n")
# for lin in opt_matrix:
#     print(lin, sep="")
# print(f"Centróide da árvore: {centroid}")

## Reconstrução das amostras da matriz original ##

# orig_matrix = []
# for i in range(len(matrix)):
#     orig_matrix.append(reconstruct_vector(opt_matrix, centroid, i))

## Módulo de visualização ## 

# plot = True
# if plot:
    
#     fig, axs = plt.subplots(1, figsize=(20, 40))

#     plot_tree_edges = [(edge[0], edge[1], edge[2]) for edge in tree_edges]
#     plot_tree_graph = nx.Graph()
#     plot_tree_graph.add_weighted_edges_from(plot_tree_edges)
#     pos_tree =  hierarchy_pos(plot_tree_graph, centroid)
#     edge_labels = nx.get_edge_attributes(plot_tree_graph, 'weight')
#     node_color=['lightsteelblue']*len(nodes)
#     nx.draw(plot_tree_graph, pos=pos_tree, with_labels=True, node_color=node_color, node_size=500, 
#             arrows=True, edge_color='gray', font_weight='bold', font_size=12)
#     aux_plot = dict(boxstyle='round', ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0), color="k", alpha=0.3)
#     nx.draw_networkx_edge_labels(plot_tree_graph, pos_tree, edge_labels=edge_labels, font_size=9, bbox=aux_plot)
    
#     plt.show()
