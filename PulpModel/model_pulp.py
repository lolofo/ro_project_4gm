
from pulp import *


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
  # Input :



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



if __name__ == "__main__" :


    N = list(range(1,8))
    a = [10,13,11,20,30,0,30]
    d = [5,6,7,4,3,6,2]
    q = [7,26,24,21,8,17,0]


    N,a,d,q = instance_creation(N,a,d,q)

    model1 = pulp_model(N,a,d,q)

    model1.solve(COIN_CMD(msg=0 , mip=1))
    print("Status of the solution = ", LpStatus[model1.status]) 
    print("Result : ", value(model1.objective))
