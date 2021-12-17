
from pulp import *
import time

import plotly.express as px  # --> data visualisation
import pandas as pd


def instance_creation(N,a,d,q) :
  _N = []
  _a = {}
  _d = {}
  _q = {}

  k = 0

  for i in N :

    _N.append(i)
    _a[i] = a[k]
    _q[i] = q[k]
    _d[i] = d[k]

    k+=1

  return _N , _a, _d , _q



### definition of the model ###

def pulp_model(N,a,d,q):
  '''
  input  : N,a,d,q --> values of the one machine sequencing problem.

  output : model   --> pulp model of the problem.
  '''



  # definition of the problem --> minimization 
  model = LpProblem("one_machine",LpMinimize)


  up_b = sum([a[i]+d[i]+q[i] for i in N])

  # variables défnition
  x = LpVariable.dicts("x", (N,N), 0, 1, LpInteger)
  t = LpVariable.dicts("t" , N ,0,up_b, LpInteger)
  z = LpVariable("z" ,0,up_b,LpInteger)

  # objective
  model += z

  # constraints definition


  # --> constraint about the objectif (linearization of a maximum)
  for i in N :
    model += z >= t[i]+d[i]+q[i]      

  # --> constraints about the order
  for i in N :

    for j in N :

      if (i<j) :
        # total order constraint
        model += x[i][j] + x[j][i] == 1  
      
      for k in N :
        # transitivity constraint
        model += x[i][k] + x[k][j] <= x[i][j] + 1
      
  

  # --> constraints about the machine
  M = 1000000

  for i in N :
    model += t[i]>= a[i]                          # note starting before the start time
    for j in N :
      model += t[j] >= d[i]+t[i] - M*(1-x[i][j])   # constraints between the jobs (i before j)
      model += t[j]-t[i] <= d[i] - 1 + M*(x[i][j])

  return model



#######################
### solve the model ###
#######################

def solve_pulp_model(N,a,d,q , show_output = True):

  N,a,d,q = instance_creation(N,a,d,q)

  start = time.time()
  model = pulp_model(N,a,d,q)                    # the model
  end_time = time.time()-start
  model.solve(COIN_CMD(msg=0 , mip=1)) # solve the model

  if (LpStatus[model.status]=="Optimal"):

    # the solution :
    varsdict = {} # contain the variables

    for v in model.variables():
      if("t_" in v.name) :
        varsdict[v.name] = v.varValue
    
    t = {k: v for k, v in sorted(varsdict.items(), key=lambda item: item[1])} # sort of the dictionnary (by values)

    schedule = [int(k.replace('t_', '')) for k in t]

    if show_output :

      print("Running time : ",end_time)
      print("Solution value : ",value(model.objective))
      print("MIP schedule : ",schedule)

    return {"SCHD" : schedule , "OBJ" : value(model.objective)}

  else :
    # problem not solved
    print("error : problem not solved")



if __name__ == "__main__" :


    N = list(range(1,8))
    a = [10,13,11,20,30,0,30]
    d = [5,6,7,4,3,6,2]
    q = [7,26,24,21,8,17,0]