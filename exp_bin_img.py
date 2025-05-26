import numpy as np
import time as time
from net_represent import *
from min_span_tree import *
from search import *
from tree_plot import *
from str_reduc import *

###############################################################
### Experimento númerico: armazenamento de imagens binárias ### 
###############################################################


## Geração do conjunto de imagens ##

rng = np.random.default_rng(seed=0)
matrix = rng.choice([0, 1], (28, 28), p=[0.5, 0.5])
num_matrix = 100
list_row = [[matrix[i].copy().tolist() for j in range(num_matrix)] for i in range(matrix.shape[0])]
p_factor = 3/28
for h in range(matrix.shape[0]) :
    for i in range(1, num_matrix):
        num_chg = rng.integers(low=1, high=int(matrix.shape[1]*p_factor))
        pos_chg = rng.integers(low=0, high=(matrix.shape[1] - 1), size=num_chg)
        for j in range(num_chg):
            list_row[h][i][pos_chg[j]] = int(not(list_row[h][i][pos_chg[j]]))
opt_list_row = [[] for i in range(matrix.shape[0])]

print("\n")
beg = time.time()
for row in range(matrix.shape[0]):

    print(f"\rOptimizing row {row+1}/{matrix.shape[0]} storage", end="")

    samples = list_row[row]

    ## Construção do grafo de diferenças ##

    nodes = list(range(len(samples)))
    edges = edges_constructor_numba(np.array(samples))
    G = adj_list(nodes, edges, directed=False)
    G.construct_adj_list()

    ## Busca por Árvore Geradora Mínima (AGM) não orientada ##

    aux_edges, cost = prim_heap(nodes, G.adj, s=0, shallow=True)
    aux_T = adj_list(nodes, aux_edges, directed=False)
    aux_T.construct_adj_list()

    ## Localização do centróide e direcionamento da AGM ## 

    centroid = centroid_search(aux_T.adj, s=0)
    tree_edges, pred_list = direct_out_tree(nodes, aux_T.adj, s=centroid)
    T = adj_list(nodes, tree_edges, directed=True)

    ## Construção da matriz de armazenamento ótimo ##

    opt_list_row[row] = opt_matrix_constructor(samples, pred_list, centroid)
end = time.time()

size_matrix = num_matrix*(matrix.shape[0]*matrix.shape[1])
size_opt_list_row = 0
for i in range(matrix.shape[0]):
    size_opt_list_row += size(opt_list_row[i])

print(f"\n-------------------------------------\
    \nOriginal matrix size: {size_matrix}\
    \nOpt. matrix size: {size_opt_list_row}\
    \nStorage reduction: {(1 - (size_opt_list_row)/size_matrix)*100}%\
    \nExecution time: {end-beg} s\
    \n-------------------------------------")
