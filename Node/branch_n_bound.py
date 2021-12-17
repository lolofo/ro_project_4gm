import networkx as nx               # network graph manipulation


from networkx.drawing.nx_pydot import graphviz_layout


import pandas as pd                 # data mnipulation
import numpy as np                  # ----------------

import matplotlib.pyplot as plt     # show graphics

import math                         # mathematics tools

import time                         # evaluate the the performance of the algorithms

import os

from Node import *

#from inst_gen import *









###############################
    ### The algorithm ###
###############################


def search_current_index(Queue,Tree) :
    '''
    objectiv : search of the node not treated with the highest lower bound

    input : Queue --> list of index (index of the nodes not treated in the Tree)
            Tree  --> list of nodes

    output : index of the node with the highest lower bound in the tree (not treated)
    '''

    res = Queue[0]
    LB = Tree[res]._LB

    for idx in Queue :

        if Tree[idx]._LB>LB :

            res = idx
            LB = Tree[res]._LB

    return res



def branch_n_bound(N , a , d , q , msg = 0) :

    Tree = []       # list of all nodes created (a list of Node objects)
    Queue = []      # list of nodes to process (a list of integers with the index of nodes to process in the Tree)
    UB = math.inf   # set the upper bound to a sufficiently large number
                    
    incumbent = []  # initialize the incumbent solution

    root = Node(N , a , d , q)      # at the root node no variables are fixed

    Tree.append(root)               # start the tree with the root node
    Queue.append(0)

    LB = root._lower_bound(N)

    
    order = 0

    while (Queue!=[] and np.abs(UB-LB)>=1) :                     #   while there is nodes to treat :
        
        currentindex = Queue[0]             # note that we follow a first-in-first-out node processing strategy
        currentnode = Tree[currentindex]

        #   evaluation step :
        shr_schedule = currentnode._schrage_schedule()
        output = currentnode._critical_search(shr_schedule)
        currentUB = output['makespan']
        currentLB = currentnode._LB

        # order of the nodes in th branch and bound --> construction of the tree
        currentnode._order = order
        order += 1


        #   --> update of the upper bound
        #   --> update of the current solution

        if currentUB < UB :
            UB = currentUB
            incumbent = shr_schedule
            currentnode._update_sol = True  # this node made the current solution better


        if (output['status']=='not_optimal') :
            #   creation of the nodes
            e1 , e2 = currentnode._nodes_creation(output['J'],output['jc'])

            # update of the relationships
            e1._parent = currentnode
            e2._parent = currentnode
            currentnode._children = [e1,e2]

            e1._level = currentnode._level +1
            e2._level = currentnode._level +1

            

            # update of the tree and the queue

            Queue.append(len(Tree))
            Queue.append(len(Tree)+1)

            Tree.append(e1)
            Tree.append(e2)

            #   update of the local lower bound
            e1._LB = max(currentLB , e1._lower_bound(output['J']) , e1._lower_bound(output['J']+[output['jc']] ))
            e2._LB = max(currentLB , e2._lower_bound(output['J']) , e2._lower_bound(output['J']+[output['jc']] ))
        
        LB = min([Tree[n]._LB for n in Queue]) # global lower
        Queue.remove(currentindex)

        
        

    return {'UB' : UB , 'LB' : LB , 'SCHD': incumbent , 'Tree' : Tree}


###############################
  ### Tree construction ###
###############################

def construct_tree(Tree) :
    '''
    Construction of the branch and bound tree and print of it
    '''
    bb_tree = nx.DiGraph()
    colors = [0]*len(Tree)
    nx.set_node_attributes(bb_tree, 'colors', colors)

    nd_not_treated = len(Tree)-1

    Queue = [Tree[0]]
    bb_tree.add_node(Tree[0]._order)
    marked = [Tree[0]]                  # Nodes of the bb_tree treated

    colors = []
    while (Queue != []) :

        buff = Queue.pop(0)             # we take the first

        # order = -1 the node wasn't treated.
        if (buff not in marked):
            bb_tree.add_node(buff._order)
            marked.append(buff)

        if (len(buff._children) != 0) :
            Queue += buff._children     # we add the children

            for n in buff._children :
                if (n not in marked) :
                    if n._order == -1 :
                        bb_tree.add_node(nd_not_treated)
                        bb_tree.add_weighted_edges_from([(buff._order , nd_not_treated , n._edge)])
                        marked.append(n)
                        nd_not_treated+=1
                    else :
                        bb_tree.add_node(n._order)
                        bb_tree.add_weighted_edges_from([(buff._order , n._order , n._edge)])
                        marked.append(n)

    return bb_tree

###############################
### tools to print the tree ###
###############################

def bb_tree_ready_to_print(Tree , Larg = 7 , Haut = 7):

    G = construct_tree(Tree)
    pos = graphviz_layout(G, prog="dot")
    nds = G.nodes()
    colors = []


    nd_max = len(Tree)-1

    node_not_treated = []

    for t in Tree :
        if t._order == -1 :
            node_not_treated.append(nd_max)
            nd_max += 1

    for n in nds :
        if n in node_not_treated :
            colors.append('red')
        else :
            for t in Tree :
                if n==t._order :
                    if t._update_sol :
                        colors.append('green')
                    else :
                        colors.append('grey')

    options = {
    'node_color' :  colors,
    'node_size'  : 550,
    'pos' : pos,
    'with_labels': True,
    }

    return G , options


###############################
### Solve the problem ###
###############################

def solve_schrage_heuristic(N,a,d,q , show_output = True ,graphics = True , larg = 7 , haut = 7):

    r = Node(N,a,d,q)

    # solve the problem with the schrage heuristic

    start = time.time()
    solution = branch_n_bound(N , a , d , q)
    end = time.time()-start

    if show_output :
        
        print("--- Solution of the one machine sequencing problem ---")
        print()
        print("optimal value : ",solution['UB'])
        print("schedule : ",solution['SCHD'])
        print("running time : ",end)
        print()
    

    G=nx.grid_2d_graph(1,2)  #1x2 grid
    
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(4*larg,2*haut))

    # the conjunctive graph
    lg_path = r._longest_path(solution['SCHD'])['path']
    G , options , labels , pos = r._graph_ready_to_print(solution['SCHD'] , lg_path )
    labels = nx.get_edge_attributes(G,'weight')        

    plt.subplot(121)
    nx.draw(G,**options)
    nx.draw_networkx_edge_labels(G,edge_labels = labels,pos = pos)
    plt.title("the solution")
    
    
    G , options = bb_tree_ready_to_print(solution['Tree'])
    lvl = max([t._level for t in solution['Tree']])
    pos = options['pos']
    labels = nx.get_edge_attributes(G,'weight')
    
    plt.subplot(122)
    nx.draw(G,**options)
    nx.draw_networkx_edge_labels(G,edge_labels = labels,pos = pos)
    plt.title('the branching tree of level : {}'.format(lvl))


    solution['time'] = end

    if graphics :
        plt.show()
        return solution
    else :
        return solution,fig
        

    

if __name__ == "__main__":

    # first test with the example of the subject
 
    N = list(range(1,8))
    a = [10,13,11,20,30,0,30]
    d = [5,6,7,4,3,6,2]
    q = [7,26,24,21,8,17,0]

    #N,a,d,q = instance_in_circle(700 , radius = 15 , origin = [100,100,100])
    solution , fig1 = solve_schrage_heuristic(N,a,d,q , graphics = False)
    print(solution)

    plt.savefig("test.png")

    '''

    fig = plt.figure(figsize = (10, 7))
    ax = plt.axes(projection ="3d")
    
    # Creating plot
    ax.scatter3D(a, d, q, color = "green")
    plt.title("Task simulated")
    
    # show plot
    plt.show()

    '''

    


    