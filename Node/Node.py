import networkx as nx               # network graph manipulation


from networkx.drawing.nx_pydot import graphviz_layout


import pandas as pd                 # data mnipulation
import numpy as np                  # ----------------

import matplotlib.pyplot as plt     # show graphics

import math                         # mathematics tools

import time                         # evaluate the the performance of the algorithms



############ Node class programmation ############

class Node :

    def __init__ (self , N , a , d , q) :

        #   attributs to stock the data

        self._N = []
        self._a = {}
        self._d = {}
        self._q = {}

        k = 0

        for i in N :

            self._N.append(i)
            self._a[i] = a[k]
            self._q[i] = q[k]
            self._d[i] = d[k]

            k+=1


        # lower bound of the problem
        self._LB = -math.inf

        #   attribut to link the nodes in a tree.
        self._parent = None
        self._children = []

        # attributs to construct the branch and bound tree
        self._update_sol = False
        self._order = -1             
        self._edge = 0
        self._level = 1


#############################
### The conjunctive graph ###
#############################


def _construct_conjonctive (self , schedule):
    ''' 
    output : the conjonctive graph for a given schedule
    '''

    # construction of a directed graph :
    G = nx.DiGraph() 

    # construction of the submit :

    sbm = ['s','t']+schedule
    G.add_nodes_from(sbm)

    # construction of the edges.
    # shcedule --> permutation of element of self._N


    for i in range(len(schedule)) :

        curr = schedule[i]
        
        e1 = ("s",curr , self._a[curr])
        e2 = (curr,"t",self._q[curr]+self._d[curr])
        # we check if we are at the last task of the schedule
        if i != len(schedule)-1 :
            next = schedule[i+1]
            e3 = (curr,next,self._d[curr]) # creation of the last edges.
            G.add_weighted_edges_from([e1,e2,e3])
        else :
            G.add_weighted_edges_from([e1,e2])
    
    # we return the conjunctive graph.
    return(G)

setattr(Node , "_construct_conjonctive" , _construct_conjonctive)




def _graph_ready_to_print(self , schedule , path ) :
    '''
    same function but return a matplotlib object ready to print.
    '''
    
    G = self._construct_conjonctive(schedule)

    # color of the edges
    for (u,v) in G.edges():
        G[u][v]['color'] = 'grey'

    for k in range(len(path)) :
        curr = path[k] # current note
        if k==0 and len(path)>1:
            next = path[k+1]
            G['s'][curr]['color'] = 'red'
            G[curr][next]['color'] = 'red'

        elif k == len(path)-1 :
            if len(path)==1 :
                
                G['s'][path[0]]['color'] = 'red'
                G[path[0]]['t']['color'] = 'red'
            else :
                G[curr]['t']['color'] = 'red'

        else :

            next = path[k+1]
            G[curr][next]['color'] = 'red'

    colors = [G[u][v]['color'] for u,v in G.edges()]
    weights = [G[u][v]['weight'] for u,v in G.edges()]

    # color of the nodes
    couleurs_sommets = ["yellow"] * G.number_of_nodes()   


    pos = {} # positions of the node.
    
    set_x = 0
    set_y = len(schedule)/2
    dy = -1

    
    for t in schedule : 
        pos[t] = [set_x , set_y]
        set_y += dy

    # position of the sources nodes.
    pos['s'] = [-1 , 0]
    pos['t'] = [1, 0]


    options = {
    'node_color' : couleurs_sommets,
    'node_size'  : 550,
    'pos' : pos,
    'edge_color' : colors,
    'with_labels': True,
    }

    
    labels = nx.get_edge_attributes(G,'weight')

    return G , options , labels , pos

setattr(Node , "_graph_ready_to_print" , _graph_ready_to_print)


#############################
### The longest path ###
#############################


def _longest_path(self, schedule):
    
    '''
    output : python dictionnary
        - value : the length of the longest past
        - path : the tasks of N in the path.
    '''

    L = {}      # dictionnary that will contain the distances
    pred = {}   # dictionnary that will contain the predecessors


    # 1 : initiation of the values

    L['s'] = 0
    pred['s'] = 's'

    L['t'] = -math.inf

    
    for k in schedule :
        L[k] = self._a[k]
        pred[k] = 's'

    # 2 : propagation of the solution :

    for i in range(len(schedule)) :

        curr = schedule[i]                  #    current node to treat.
                                            #    we'll check the succesors of curr 
        if i != len(schedule)-1 :

            next = schedule[i+1]            # next node in the order.
            new_L = L[curr]+self._d[curr]
            
            if (new_L >= L[next]) :
                L[next] = new_L
                pred[next] = curr
        
                                            # we'll change the value of the path to t
                                            # from the current node.
                                            
        new_t = L[curr]+self._d[curr]+self._q[curr]

        if new_t >= L['t'] :
            pred['t'] = curr
            L['t'] = new_t

    
    # backpropagation to find the path
    temp = 't'
    makespan = L['t']
    path = ['t']


    while temp !='s':

        path.insert(0,pred[temp]) # add to the begining
        temp = pred[temp]

    path.pop()
    path.pop(0)
    

    res = {'value' : makespan , 'path' : path}


    
    return(res)


setattr(Node , "_longest_path" , _longest_path)


#############################
### The shrage schedule ###
#############################


def _schrage_schedule(self) :
        #       Step 1
        n = len(self._N)
        U = []
        b_U = self._N.copy() #  Copy of all the tasks
        t = min([self._a[i] for i in b_U])

        #       step 2 and 3
        while (len(U) != n) :
                arg_set = []                        # set where we search for the argmax
                for j in b_U :
                        if self._a[j] <= t :
                                arg_set.append(j)

                buff = [self._q[j] for j in arg_set]

                idx_arg_max = np.argmax(buff)
                i = arg_set[idx_arg_max]

                b_U.remove(i)
                U.append(i)

                ti = t
                buff = [self._a[j] for j in b_U]


                '''
                two cases : --> b_U is empty
                            --> still got one element (at least)
                '''
                
                if len(b_U)==0 :
                        t = ti + self._d[i]
                else :
                        t = max(ti + self._d[i] , min([self._a[i] for i in b_U]))

        return U

setattr(Node , "_schrage_schedule" , _schrage_schedule)

############################
### Critical search ###
############################

def _critical_search(self,schedule) :

    '''
    input : python array
        - the array is a permutation of the set self._N

    output : python dictionnary
        - makespan : time of the schedule
        - J : critical set (if it exists)
        - jc : critical task (if it exists)
        - status : status of the schrage schedule
    '''
    
    output = self._longest_path(schedule) # search for the longest path
    path = output['path']                 # get the path
    makespan = output['value']            # time that the schedule will take


    jp = path[-1]           # last task to worry about
    target = self._q[jp]
    J = [jp]                # critical set
    jc = -1                 # critical task
    status = ''             # status of the schedule.

    # search of a potential critical task  --> we search from the end to the begining of the path.
    # the critical set will grow wathever happens.

    for i in range(len(path)-2 , -1 , -1) :

        jk = path[i]
        buff = self._q[jk]

        if (buff<target) :
            # critical set found, we stop.
            jc = jk
            break
        else :
            J.append(jk)

    
    if(jc == -1):
        # critical task not found --> schedule is optimal
        #                         --> the critical set doesn't exists
        J = []
        status = 'optimal'
    else :
        status = 'not_optimal'

    
    # dictionnary to return
    res = {'makespan' : makespan , 'J' : J , 'jc' : jc , 'status' : status}

    return(res)

setattr(Node,"_critical_search",_critical_search)



def _lower_bound(self , I) :

    a = min([self._a[i] for i in I])
    d = sum([self._d[i] for i in I])

    q = min([self._q[i] for i in I])

    return(a+d+q)

setattr(Node,"_lower_bound",_lower_bound)



################################
### Nodes creation / branching rule ###
################################


def _nodes_creation(self , J , jc):

    ''' 
    output : python array
        - the first node is the node where we changed the value of q
        - the second node is the node where we changed the value of a
    '''
    jp = J[0]

    q_jc = sum([self._d[r] for r in J]) + self._q[jp]
    a_jc = min([self._a[r] for r in J]) + sum([self._d[r] for r in J])

    N = self._N.copy()

    a1 = []
    a2 = []

    d1 = []
    d2 = []

    q1 = []
    q2 = []

    for i in N :
        a1.append(self._a[i])
        a2.append(self._a[i])
        d1.append(self._d[i])
        d2.append(self._d[i])
        q1.append(self._q[i])
        q2.append(self._q[i])

    e1 = Node(N , a1 , d1 , q1)
    e2 = Node(N , a2 , d2 , q2)


    e1._q[jc] = q_jc
    e1._edge = q_jc


    e2._a[jc] = a_jc
    e2._edge = a_jc

    return([e1,e2])
    
setattr(Node,"_nodes_creation",_nodes_creation)