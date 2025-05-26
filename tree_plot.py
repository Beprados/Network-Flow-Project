import networkx as nx
import random

import numpy as np

def radial_pos(G, root=None, radius_step=1.0):
    '''
    Retorna um dicionário com posições (x, y) dos nós em layout radial.
    root: nó central (raiz)
    radius_step: distância entre "níveis"
    '''
    if root is None:
        root = list(nx.topological_sort(G))[0]

    layers = {}  # nível de profundidade de cada nó
    def assign_layers(node, depth=0):
        if node in layers:
            return
        layers[node] = depth
        for child in G.successors(node):
            assign_layers(child, depth + 1)

    assign_layers(root)

    max_layer = max(layers.values())
    positions = {}
    for layer in range(max_layer + 1):
        nodes_at_layer = [n for n in G.nodes if layers[n] == layer]
        angle_step = 2 * np.pi / len(nodes_at_layer)
        radius = layer * radius_step
        for i, node in enumerate(nodes_at_layer):
            theta = i * angle_step
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            positions[node] = (x, y)

    return positions
    
def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.  
    Licensed under Creative Commons Attribution-Share Alike 
    
    If the graph is a tree this will return the positions to plot this in a 
    hierarchical layout.
    
    G: the graph (must be a tree)
    
    root: the root node of current branch 
    - if the tree is directed and this is not given, 
      the root will be found and used
    - if the tree is directed and this is given, then 
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given, 
      then a random choice will be used.
    
    width: horizontal space allocated for this branch - avoids overlap with other branches
    
    vert_gap: gap between levels of hierarchy
    
    vert_loc: vertical location of root
    
    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''
    
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos

            
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)