class incid_matrix():

    """ 
    _________________
    --- Descrição ---
    _________________

    Classe para representação de grafos por matriz de incidência.

    __________________
    --- Argumentos ---
    __________________

    - nodes : lista de nós (enumerados ou com nome);

    - edges : lista de arcos, em que cada elemento é
    definido segundo o padrão:
        [nó de partida, nó incidente, custo=opcional];

    - directed : valor booleano que indica o direcionamento,
    ou não, do grafo;

    - sort : valor booleano que, quando verdadeiro, ordena
    os arcos com relação aos seus custos;

    _________________
    --- Atributos ---
    _________________

    - nodes : lista de nós (enumerados ou com nome);

    - N : número de nós;

    - edges : lista de arcos, em que cada elemento é
    definido segundo o padrão:
        [nó de partida, nó incidente, custo=opcional];

    - E : número de arcos.

    - directed : valor booleano que indica o direcionamento,
    ou não, do grafo;

    - weight : valor booleano que se o grafo é ponderado;

    - sort : valor booleano que, quando verdadeiro, ordena
    os arcos com relação aos seus custos;

    - cost : lista de custos;

    - mat : matriz de incidência.

    _______________
    --- Métodos ---
    _______________

    - __init___ : inicializa atributos básicos, sendo eles
    nodes, N, edges, E, directed, sort, weight e cost;

    - construct_matrix : constrói matriz de incidência;

    - display : fornce vizualização da matriz de inciência, 
    caso já tenha sido construída, via terminal.

    """

    def __init__(self, nodes, edges, directed=True, sort=True):
        
        self.nodes = nodes
        self.N = len(nodes)
        self.edges = edges
        self.E = len(edges)
        self.directed = directed
        if len(self.edges[0]) == 2:
            self.weight = False
        else:
            self.weight = True
            if sort:
                self.edges.sort(key=aux_sort)
            self.cost = [edge[2] for edge in edges]
        self.mat = None
    
    def construct_matrix(self):
        
        self.mat = [[0 for _ in range(self.E)] for __ in range(self.N)]

        val0 = 1
        if self.directed:
            val1 = -1
        else:
            val1 = 1
        
        for i in range(self.E):
            self.mat[self.edges[i][0]][i] = val0
            self.mat[self.edges[i][1]][i] = val1

        return 

    def display(self):
        
        if self.mat is None:
            return print("Matriz de incidência ainda não foi construída.")
        
        print("\n")
        for lin in self.mat:
            print(lin, "\n")
        print("\n")

        return 

def aux_sort(elem):

    """
    _________________
    --- Descrição ---
    _________________

    Função auxiliar para comparação entre os arcos de um grafo conforme seus pesos.

    __________________
    --- Argumentos ---
    __________________

    - elem : lista representando um arco ponderado, segundo o padrão:
        [nó de partida, nó incidente, custo] .

    
    _____________
    --- Saída ---
    _____________
    
    - elem[2] : custo do arco.

    """
    return elem[2]
    
class adj_list():

    """ 
    _________________
    --- Descrição ---
    _________________

    Classe para representação de grafos por lista de adjacência.

    __________________
    --- Argumentos ---
    __________________

    - nodes : lista de nós (enumerados ou com nome);

    - edges : lista de arcos, em que cada elemento é
    definido segundo o padrão:
        [nó de partida, nó incidente, custo=opcional];

    - directed : valor booleano que indica o direcionamento,
    ou não, do grafo;

    _________________
    --- Atributos ---
    _________________

    - nodes : lista de nós (enumerados ou com nome);

    - N : número de nós;

    - edges : lista de arcos, em que cada elemento é
    definido segundo o padrão:
        [nó de partida, nó incidente, custo=opcional];

    - E : número de arcos.

    - directed : valor booleano que indica o direcionamento,
    ou não, do grafo;

    - weight : valor booleano que se o grafo é ponderado;

    - adj : lista de adjacência.

    _______________
    --- Métodos ---
    _______________

    - __init___ : inicializa atributos básicos, sendo eles
    nodes, N, edges, E, directed e weight;

    - add_edge : adiciona arco à lista de adjacência.

        * Argumentos: 

            - edge : lista do arco a se adicionado.

    - construct_adj_list : constrói lista de adjacência;

    - display : fornce vizualização da lista de adjacência, 
    caso já tenha sido construída, via terminal.

    """

    def __init__(self, nodes, edges, directed=True):

        self.nodes = nodes
        self.N = len(nodes)
        self.edges = edges
        self.E = len(edges)
        self.directed = directed
        if len(self.edges[0]) == 2:
            self.weight = False
        else:
            self.weight = True
        self.adj = None
    
    def add_edge(self, edge):
    
        if not self.weight:
            cost = 0
        else:
            cost = edge[2]
        
        self.adj[edge[0]].append([edge[1], cost])
        
        if not self.directed:
            self.adj[edge[1]].append([edge[0], cost])  # Undirected
    
    def construct_adj_list(self):

        self.adj = [[] for _ in range(self.N)]
        
        for edge in self.edges:
            self.add_edge(edge)

        return

    def display(self):

        if self.adj is None:
            return print("Lista de adjacência ainda não foi construída.")

        print("\n")
        for i in range(len(self.adj)):
            print(f"{i}: ", end="")
            for j in self.adj[i]:
                print(j, end=" ")
            print()
        
        return

############################################
### Exemplo de construção e vizualização ###
############################################

# nodes = [0, 1, 2, 3, 4, 5]
# edges = [[0, 1, 0],
#          [0, 2, 1],
#          [0, 4, 2],
#          [1, 2, 3],
#          [1, 3, 4],
#          [2, 3, 5],
#          [2, 4, 6],
#          [3, 5, 7],
#          [4, 5, 8]]
#
# incid_mat = incid_matrix(nodes, edges)
# incid_mat.construct_matrix()
# incid_mat.display()
#
# adj_lst = adj_list(nodes, edges)
# adj_lst.construct_adj_list()
# adj_lst.display()

