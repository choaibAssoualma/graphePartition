import sys

def read_graph(graph_file):
	file = open(graph_file)

	nb_vertices, nb_edges = [int(x) for x in next(file).split()]
	graph = []

	for line in file:
		graph.append([int(x) for x in line.split()])

	return graph 

print(read_graph("exemple.graphe"))
