from net_represent import *

#####################################################################
### Estrutura de dado min-heap (árvore binária) aplicada à grafos ###
#####################################################################
#
# Sua implementação visa ao suporte do algoritmo de Prim, mais especificamente,
# na etapa de busca por arcos de custo mínimo. O suporte ao algoritmo de Krukal 
# durante a ordenação das arestas também não pode ser esquecido. A implementação 
# seguiu os passos esclarecedores do professor Paulo Feofiloff (https://www.ime.usp.br/~pf/), 
# cujas notas de aula sobre o assunto (https://www.ime.usp.br/~pf/mac0122-2002/aulas/heapsort.html)
# em muito contribuíram para a minha compreensão dos algoritmos.
#

def exch (A, B):

    """
    _________________
    --- Descrição ---
    _________________

    Função responsável por trocar a posição de dois elementos em uma lista.

    __________________
    --- Argumentos ---
    __________________

    - A : primeiro elemento a ser trocado;

    - B : segundo elemento a ser trocado.

    ______________
    --- Saídas ---
    ______________

    - A : primeiro elemento já trocado;

    - B : segundo elemento já trocado.

    """

    temp = A
    A = B 
    B = temp

    return A, B

def fix_up_graph(vec, k):

    """
    _________________
    --- Descrição ---
    _________________

    Função responsável por rearranjar um vetor de arestas de modo a transfromá-lo em min-heap.
    Supõe-se que o vetor recebido vec[0..k-1] é tal que vec[0..k-2] já é min-heap. A função 
    "arruma para cima" o vetor recebido.

    __________________
    --- Argumentos ---
    __________________

    - vec : lista de arestas a ser rearranjada;

    - k : índice do nó a ser "realocado para cima".

    ______________
    --- Saídas ---
    ______________

    None.
    
    """

    while(k>0 and (vec[((k-1)//2)][2] > vec[k][2])):
        vec[k], vec[(k-1)//2] = exch(vec[k], vec[(k-1)//2])
        k = (k-1)//2

    return 

def fix_down_graph(vec, k, n):

    """
    _________________
    --- Descrição ---
    _________________

    Função responsável por rearranjar vetor vec[0..n-1] de modo que o subvetor cuja
    raiz é k transforme-se em min-heap. Supoõe-se que os subvetores cujas raízes são
    os filhos de k, já são min-heap. A função "arruma para baixo" o vetor recebido.

    __________________
    --- Argumentos ---
    __________________

    - vec : lista de arestas a ser rearranjada;

    - k : índice do nó a ser "realocado para baixo";

    - n : tamanho de vec.

    ______________
    --- Saídas ---
    ______________

    None.
    
    """

    while 2*k + 1 <= n-1:
        j = 2*k + 1
        if j<n-1 and vec[j][2]>vec[j+1][2]:
            j += 1
        if vec[k][2] < vec[j][2]:
            break
        vec[k], vec[j] = exch(vec[k], vec[j])
        k = j

    return

def extract_min_graph(vec):
    
    """
    _________________
    --- Descrição ---
    _________________

    Função responsável por extrair o nó de menor valor da min-heap, a saber, sempre
    o primeiro elemento. Uma vez retirado, a min-heap é "arrumada para baixo" a partir
    do primeiro índice.

    __________________
    --- Argumentos ---
    __________________

    - vec : lista de arestas representando min-heap em relação as custos de arco.

    ______________
    --- Saídas ---
    ______________

    - minim : elemento de maior prioridade, mínimo da heap.
    
    """

    minim = vec[0]
    vec[0], vec[-1] = exch(vec[0], vec[-1])
    vec.pop(-1)
    fix_down_graph(vec, 0, len(vec))

    return minim

def add_to_heap_graph(vec, elem):

    """
    _________________
    --- Descrição ---
    _________________

    Função responsável por adicionar nó à min-heap. Visto que o elemento é concatenado ao
    fim do vetor, subsequentemente a heap é "arrumada para cima" a partir do último 
    elemento. 

    __________________
    --- Argumentos ---
    __________________

    - vec : lista de arestas representando min-heap em relação as custos de arco;

    - elem : elemento a ser adicionado.

    ______________
    --- Saídas ---
    ______________

    None.
    
    """
    
    vec.append(elem)
    fix_up_graph(vec, len(vec)-1)

    return

def delete_elem_graph(vec, i):

    """
    _________________
    --- Descrição ---
    _________________

    Função responsável por retirar nó da min-heap. Uma vez retirado, já que o elemento 
    ocupava índice i no vetor, subsequentemente a heap é "arrumada para baixo" a partir 
    da posição i. 

    __________________
    --- Argumentos ---
    __________________

    - vec : lista de arestas representando min-heap em relação as custos de arco;

    - i : índice do elemento a ser retirado.

    ______________
    --- Saídas ---
    ______________

    None.
    
    """
    
    vec[i], vec[-1] = exch(vec[i], vec[-1])
    vec.pop(-1)
    fix_down_graph(vec, i, len(vec))

    return

def decrease_key_graph(vec, i, val):

    """
    _________________
    --- Descrição ---
    _________________

    Função responsável por diminuir o custo de uma aresta pertencente à min-heap.
    Em seguida, "arruma para cima" o vetor a partir do índice cuja chave foi alterada. 

    __________________
    --- Argumentos ---
    __________________

    - vec : lista de arestas a ser rearranjada;

    - i : índice do nó a ter valor de chave alterado;

    - val : novo valor da chave.

    ______________
    --- Saídas ---
    ______________

    None.
    
    """

    vec[i][2] = val
    fix_up_graph(vec, i)

    return

def turn_to_heap_graph(vec, n):

    """
    _________________
    --- Descrição ---
    _________________

    Função responsável por tornar lista de arestas em min-heap. Iterativamente, os últimos filhos,
    e então seus pais são "arrumados para baixo", até que se alcance o elemento da primeira posição.

    __________________
    --- Argumentos ---
    __________________

    - vec : lista de arestas;

    - n : número de elementos de vec.

    ______________
    --- Saídas ---
    ______________

    None.
    
    """

    for k in range(n//2 - 1, -1, -1):
        fix_down_graph(vec, k, n)

    return

def heapsort_graph(vec, n):

    """
    _________________
    --- Descrição ---
    _________________

    Função responsável ordenar lista de arestas em ordem decrescente.

    __________________
    --- Argumentos ---
    __________________

    - vec : lista de arestas;

    - n : número de elementos de vec.

    ______________
    --- Saídas ---
    ______________

    - vec : lista de arestas ordenada.
    
    """

    turn_to_heap_graph(vec, n)

    for cont in range(n-1, 0, -1):
        vec[0], vec[cont] = exch(vec[0], vec[cont])
        fix_down_graph(vec, 0, cont)

    return vec

###############################################
### Exemplo de heapsort em arestas de grafo ###
###############################################

# nodes = [0, 1, 2, 3, 4, 5]
# edges = [[0, 1, 5], 
#          [0, 2, 6], 
#          [1, 2, 2],
#          [1, 4, -1],
#          [1, 3, 4],
#          [2, 4, 4],
#          [3, 4, 2],
#          [3, 5, 6],
#          [4, 5, 5]]
# G = adj_list(nodes, edges, directed=False)
# G.construct_adj_list()

# heapsort_graph(edges, len(edges))
# print(edges, "\n")