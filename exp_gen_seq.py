import numpy as np
from net_represent import *
from min_span_tree import *
from search import *
from tree_plot import *
from str_reduc import *

###################################################################
### Experimento númerico: armazenamento de sequências genéticas ### 
###################################################################

## Geração do conjunto de pesos ##

rng = np.random.default_rng(seed=0)
m = 10
n = 1000
matrix = rng.choice([-2, -1, 1, 2], (n, m), p=[0.25, 0.25, 0.25, 0.25]).tolist()

## Construção do grafo de diferenças ##

nodes = list(range(len(matrix)))
edges = edges_constructor_numba(np.array(matrix))
G = adj_list(nodes, edges, directed=False)
G.construct_adj_list()

## Busca por Árvore Geradora Mínima (AGM) não orientada ##

aux_edges, cost = prim_heap(nodes, G.adj, s=0, shallow=True)
aux_T = adj_list(nodes, aux_edges, directed=False)
aux_T.construct_adj_list()

## Localização do centróide e direcionamento da AGM ## 

centroid = centroid_search(aux_T.adj, s=np.random.randint(low=0, high=G.N))
tree_edges, pred_list = direct_out_tree(nodes, aux_T.adj, s=centroid)
T = adj_list(nodes, tree_edges, directed=True)
T.construct_adj_list()

## Construção da matriz de armazenamento ótimo ##

opt_matrix = opt_matrix_constructor(matrix, pred_list, centroid)

print(f"Original matrix size: {size(matrix)}\
      \nOpt. matrix size: {size(opt_matrix)}\
      \nStorage reduction: {(1 - (size(opt_matrix)/size(matrix)))*100}%\
      \nMST average cost: {cost/(len(matrix) - 1)}\
      \nMST average cost upper limit: {0.5*(len(matrix[0]) - 2)}")
