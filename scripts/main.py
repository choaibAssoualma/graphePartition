from gurobipy import *
import parser as p
import solve as so


graph =p.parse("../graphs/exemple.graph")
so.solve(graph,2)
