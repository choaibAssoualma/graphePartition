from random import randint
import networkx as nx
import matplotlib.pyplot as plt


def parse(fichier):
    g=nx.Graph()
    f = open(fichier, 'r')
    n = 0
    for l in f:
        if n != 0:
            t = str.rsplit(l)
            i = 0
            j = 1
            while j < len(t):
                if not g.has_edge(n,int(t[j])):
                    g.add_edge(n,int(t[j]),weight=int(t[i]))
                i = i + 2
                j = j + 2
        n = n+1
    f.close()
    return g
