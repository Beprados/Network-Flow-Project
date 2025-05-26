import numpy as np
import time
import os
import matplotlib.pyplot as plt
from net_represent import *
from min_span_tree import *
from search import *
from tree_plot import *
from str_reduc import *


if __name__ == "__main__":

    n_var = 50
    time_exec = []
    size_mat = list(range(100, 1000, n_var))
    str_reduc = []
    sigma_coeff = []


    rng = np.random.default_rng(seed=0)
    for i in size_mat:

        print(f"\rOptimizing matrix of size {i}", end="")

        beg = time.time()

        matrix = rng.choice([0, 1], (i, 10), p=[1/2, 1/2]).tolist()

        nodes = list(range(len(matrix)))
        edges = edges_constructor_numba(np.array(matrix))

        G = adj_list(nodes, edges, directed=False)
        G.construct_adj_list()

        aux_edges, cost = prim_heap(nodes, G.adj, s=0, shallow=True)
        # aux_edges, cost = kruskal(nodes, edges)
        aux_T = adj_list(nodes, aux_edges, directed=False)
        aux_T.construct_adj_list()

        centroid = centroid_search(aux_T.adj, s=0) # np.random.randint(low=0, high=G.N))
        tree_edges, pred_list = direct_out_tree(nodes, aux_T.adj, s=centroid)
        T = adj_list(nodes, tree_edges, directed=True)
        T.construct_adj_list()

        opt_matrix = opt_matrix_constructor(matrix, pred_list, centroid)

        fin = time.time()

        opt_matrix = opt_matrix_constructor(matrix, pred_list, centroid)
        time_exec.append(fin-beg)
        str_reduc.append(1 - (size(opt_matrix)/size(matrix)))

        aux0 = cost/(i-1)
        aux1 = aux0/(0.5 * (n_var - 1))
        sigma_coeff.append(aux1)

    path = os.path.expanduser('~/net_flow')
    np.save(os.path.join(path, "k_time"), time_exec)
    np.save(os.path.join(path, "k_reduc"), str_reduc)

    print(f"\nTotal time spent: {sum(time_exec)} s\n")

    fig, ax = plt.subplots(3, figsize=(12, 12))
    ax[0].plot(size_mat, time_exec, ls="--", marker="o", label="Collected data")
    ax[0].set_xlabel("Data samples")
    ax[0].set_ylabel("Execution time")
    ax[0].legend()
    ax[0].grid()

    ax[1].plot(size_mat, str_reduc, ls="--", marker="o", label="Collected data")
    ax[1].set_xlabel("Data samples")
    ax[1].set_ylabel("Storage reduction [ % ]")
    ax[1].legend()
    ax[1].grid()

    ax[2].plot(size_mat, sigma_coeff, ls="--", marker="o", label="Collected data")
    ax[2].set_xlabel("Data samples")
    ax[2].set_ylabel("Sigma coefficient")
    ax[2].legend()
    ax[2].grid()

    plt.show()