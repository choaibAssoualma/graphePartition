from gurobipy import *
import parser as p

def poids(s1,s2,graph):
    try:
        v = graph.get_edge_data(s1,s2,0)['weight']
    except (TypeError):
        v = 0
    return v


def matricePoids(graph):
    n = graph.number_of_nodes()
    cij = [[0 for x in range (n)] for x in range (n)]
    for i in range (n):
        for j in range (i+1, n):
            cij[i][j] = poids(i+1,j+1,graph)
    return cij


def funcobj(cij, graph):
    n = graph.number_of_nodes()
    global X
    X = {}
    global Y
    Y = {}

    global Z
    Z = {}

    global model
    model = Model()

    # Ajout de la variable Xi au modèle
    for i in range(1, n+1):
        X[i] = model.addVar(vtype=GRB.BINARY, name="X_"+str(i), obj=0)

    # Ajout de la variable Yij au modèle
    for i in range(1, n):
        for j in range(i+1, n+1):
            Y[i,j] = model.addVar(vtype=GRB.BINARY, name="Y_"+str(i)+"_"+str(j), obj=-cij[i-1][j-1])
            Y[j,i] = Y[i,j]

    # Ajout de la variable Zij au modèle
    for j in range(1,n+1):
        for i in range(1,j):
            Z[i,j] = model.addVar(vtype=GRB.BINARY, name="Z_"+str(i)+"_"+str(j), obj=0)

    # Problème de minimisation
    model.modelSense = GRB.MINIMIZE
    model.update()



def contraintes(cij, graph, k):

    n = graph.number_of_nodes()

    # Le nombre de partitions est égal au nombre de représentants
    model.addConstr(quicksum(X[i] for i in range (1,n+1)) == k)

    #  Inégalité triangulaire
    # Si i est dans une partition avec j et k,
    # alors j et k sont aussi dans une même partition
    for i in range(1,n+1):
        for j in range (1,n+1):
            if j != i:
                for k in range (1,n+1):
                    if k!=j and k!=i:
                        L3a = LinExpr([1,1], [Y[i,j], Y[i,k]])
                        L3a.addConstant(-1)
                        L3b = LinExpr([1],[Y[j,k]])
                        model.addConstr(L3a, "<=", L3b)

    # Choix des représentants
    # Un sommet i connait soit des voisins déjà représentants,
    # soit il devient représentant
    for j in range(1,n+1):
        model.addConstr(X[j] + quicksum(Z[i,j] for i in range (1,j) ) == 1)

    for j in range(1,n+1):
        for i in range(1,j):
            model.addConstr(Z[i,j], "<=", X[i])
            model.addConstr(Z[i,j], "<=", Y[i,j])
            model.addConstr(Z[i,j], ">=", X[i] + Y[i,j] -1)

    # Relaxation linéaire sur les Yij
    for i in range(1,n+1):
        for j in range (1,i):
            model.addConstr(Y[i,j], "<=", 1)
            model.addConstr(Y[i,j], ">=", 0)



def printSol(n):
    for i in range(1,n+1):
        if model.getVarByName("X_"+str(i)).getAttr('X') == 1:
            print ("Partiton avec representant",i,":")
            for j in range(i+1,n+1):
                if model.getVarByName("Y_"+str(i)+"_"+str(j)).getAttr('X') > 0:
                    print (j)



def solve(graph,k):
    cij = matricePoids(graph)
    funcobj(cij, graph)
    contraintes(cij,graph,k)
    model.optimize()
    s = model.status
    if s == GRB.Status.UNBOUNDED:
        print ("Modele non borné")
    if s == GRB.Status.OPTIMAL:
        print ("la solution optimale est %g" % model.objVal)
        n = graph.number_of_nodes()
        printSol(n)
    if s == GRB.Status.INF_OR_UNBD and s != GRB.Status.INFEASIBLE:
        print ("programme arreté;status: %d" % s)
