#!/usr/bin/env python

#########################################################################
#   This code finds communities of a given graph. According to papge:   #
#   "Searching overlapping communities for group query", by Shan et al. #
#   Author: Mojtaba (Omid) Rezvani                                      #
#########################################################################

import sys
import random
from os.path import isfile, join
import copy



#########################################################################
#   Vertex class; We consider a dictionary to store the neighbours of   #
#   each vertex. It gives us the chance to access each neighbor in      #
#   constant amount of time, as required in this application.           #
#########################################################################
class Vertex:

    #########################################################################
    #   Initialize by an empty dictionry. Here, we also store an array      #
    #   that contains the list of vertices that have been contracted to     #
    #   this vertex. We also distinguish between number of neighbors and    #
    #   sum of weights of neighbors.                                        #
    #########################################################################
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        self.contracted = [node]
        self.num_neighbors = 0
        self.sum_weights = 0


    #########################################################################
    #   Let it print the neighbors of this vertex                           #
    #########################################################################
    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])


    #########################################################################
    #   Add a neighbor to this vertex                                       #
    #########################################################################
    def add_neighbor(self, neighbor, weight=1):
        if not self.adjacent.has_key(neighbor):
            self.num_neighbors += 1
            self.sum_weights += weight
        self.adjacent[neighbor] = weight


    #########################################################################
    #   Check if this vertex has a given neighbor                           #
    #########################################################################
    def has_neighbor(self, neighbor):
        return self.adjacent.has_key(neighbor)


    #########################################################################
    #   Remove a particular neighbor from this list                         #
    #########################################################################
    def remove_neighbor(self, neighbor):
        if self.adjacent.has_key(neighbor):
            self.num_neighbors -= 1
            self.sum_weights -= self.adjacent[neighbor]
            del self.adjacent[neighbor]


    #########################################################################
    #   Get the list of neighbors of this vertex                            #
    #########################################################################
    def get_connections(self):
        return self.adjacent.keys()  


    #########################################################################
    #   Get a neighbor (the Vertex object of the neighbor)                  #
    #########################################################################
    def get_neighbor(self, i):
        return self.adjacent.keys()[i]


    #########################################################################
    #   Getting the num of neighbors the hard way -- used for testing       #
    #########################################################################
    def get_num_neighbors_h(self):
        return len(self.adjacent)


    #########################################################################
    #   Getting the number of neighbors using our defined attribute         #
    #########################################################################
    def get_num_neighbors(self):
        # Testing script; It will be commented out
        #if self.num_neighbors != self.get_num_neighbors_h():
        #    print "Error in updating num neighbors"
        return self.num_neighbors


    #########################################################################
    #   Get the id of this vertex                                           #
    #########################################################################
    def get_id(self):
        return self.id


    #########################################################################
    #   Get the weight of edge between this vertex and a given neighbor     #
    #########################################################################
    def get_weight(self, neighbor):
        return self.adjacent[neighbor]


    #########################################################################
    #   Update the weihgt of a an edge. We do not add/remove edges here     #
    #   Be careful, this is dangrouse. We check whether the connection      #
    #   exists in the graph class                                           #
    #########################################################################
    def update_weight(self, neighbor, new_weight):
        if self.has_neighbor(neighbor):
            self.sum_weights -= self.adjacent[neighbor]
            self.adjacent[neighbor] = new_weight
        else:
            print "Shout: The edge does not exit"


    #########################################################################
    #   Increment the weight of an edge by a certain amount.                #
    #   If the edge does not exist, it means that its weight is zero, so    #
    #   we add an edge in this case                                         #
    #########################################################################
    def increment_weight(self, neighbor, inc_value):
        if self.has_neighbor(neighbor):
            self.adjacent[neighbor] += inc_value
        else:
            self.adjacent[neighbor] = inc_value
            self.num_neighbors += 1
        self.sum_weights += inc_value


    #########################################################################
    #   Getting the sum of weights the hard way -- used for testing         #
    #########################################################################
    def get_sum_weights_h(self):
        return sum(self.adjacent.values())


    #########################################################################
    #   Getting the sum of weights using our attribute                      #
    #########################################################################
    def get_sum_weights(self):
        # Testing script; It will be commented out
        #if self.sum_weights != self.get_sum_weights_h():
        #    print "Error in updating num neighbors"
        return self.sum_weights


    #########################################################################
    #   When contraction happened, we add the poor contracted vertex to     #
    #   our list of contracted vertices                                     #
    #########################################################################
    def add_contracted(self, neighbor):
        self.contracted += neighbor.get_contracted()


    #########################################################################
    #   Get the list of vertices that have been contracted to this vertex   #
    #   This is usefull when the vertex is removed from graph and we want   #
    #   to output the community                                             #
    #########################################################################
    def get_contracted(self):
        return self.contracted




#########################################################################
#   Graph class is designed to handle operations on graph               #
#########################################################################
class Graph:

    #########################################################################
    #   Inisitalize the graph with empty set of vertices                    #
    #   We also store the index of each vertex in vert_num                  #
    #########################################################################
    def __init__(self):
        self.vert_dict = {}
        self.vert_num = {}
        self.num_vertices = 0


    #########################################################################
    #   Read the list of edges of a graph from a file                       #
    #########################################################################
    def read_graph(self, graph_file):
        """ Add connections (list of tuple pairs) to graph """

        with open(graph_file) as gf:
            for line in gf:
                e = [int(v) for v in line.split()]
                self.add_edge(e[0], e[1])
        gf.close()


    #########################################################################
    #   Iterate over vertices of the graph                                  #
    #########################################################################
    def __iter__(self):
        return iter(self.vert_dict.values())


    #########################################################################
    #   Add a vertex to the graph                                           #
    #########################################################################
    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        self.vert_num[node] = self.num_vertices - 1
        return new_vertex


    #########################################################################
    #   It returns a vertex with id n, while checking its existence         #
    #########################################################################
    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None


    #########################################################################
    #   Add an edge to the network with a certain weight                    #
    #########################################################################
    def add_edge(self, frm, to, cap = 1):
        """ Add connection between frm and to """

        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cap)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cap)


    #########################################################################
    #   Remove an edge from network. Usefull in decomposition               #
    #########################################################################
    def remove_edge(self, frm, to):
        """ Remove connection between frm and to """

        if self.is_connected(frm, to):
            self.vert_dict[frm].remove_neighbor(self.vert_dict[to])
            self.vert_dict[to].remove_neighbor(self.vert_dict[frm])


    #########################################################################
    #   Print the list of edges of the network along with their weight      #
    #########################################################################
    def print_edges(self):
        for v in self:
            for w in v.get_connections():
                vid = v.get_id()
                wid = w.get_id()
                print '( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w))


    #########################################################################
    #   Print the edge lists of the network in a form of adjacency list     #
    #########################################################################
    def print_graph(self):
        for v in self:
            print 'g.vert_dict[%s]=%s' %(v.get_id(), self.vert_dict[v.get_id()])


    #########################################################################
    #   Check if two nodes are connected                                    #
    #########################################################################
    def is_connected(self, node1, node2):
        if node1 in self.vert_dict and node2 in self.vert_dict:
            return self.vert_dict[node1].has_neighbor(self.vert_dict[node2])
        else:
            return False


    #########################################################################
    #   Get the weight of an edge between two nodes in the network          #
    #########################################################################
    def get_weight(self, node1, node2):
        if node1 in self.vert_dict and node2 in self.vert_dict:
            return self.vert_dict[node1].get_weight(self.vert_dict[node2])
        else:
            return -1


    #########################################################################
    #   Update the weight of the edge between two nodes in the network      #
    #########################################################################
    def update_weight(self, node1, node2, new_weight):
        if self.is_connected(node1, node2):
            #self.vert_dict[node1].adjacent[self.vert_dict[node2]] = new_weight
            self.vert_dict[node1].update_weight(self.vert_dict[node2], new_weight)
            return self.vert_dict[node1].get_weight(self.vert_dict[node2])
        else:
            return -1


    #########################################################################
    #   Increment the weight of this edge by a certain amount. If the edge  #
    #   is not present, consider the weight to be zero and add it           #
    #########################################################################
    def increment_weight(self, node1, node2, inc_by = 1):
        self.vert_dict[node1].increment_weight(self.vert_dict[node2], inc_by)
        #if self.is_connected(node1, node2):
        #    self.vert_dict[node1].adjacent[self.vert_dict[node2]] += inc_by
        #    return self.vert_dict[node1].adjacent.get(self.vert_dict[node2])
        #else:
        #    self.add_edge(node1, node2, inc_by)
        #    return inc_by


    #########################################################################
    #   Get a list of vertices from dictionary (keys)                       #
    #########################################################################
    def get_vertices(self):
        return self.vert_dict.keys()


    #########################################################################
    #   It decomposes the network into k-cores which is usefull, as we can  #
    #   run a (gamma * k^2)-core decomposition                              #
    #########################################################################
    def decompose_kcore(self, k):
        # Let's decompose the graph into k-cores

        # Find some vertices to be removed
        to_be_removed = []
        for v in self:
            if v.get_sum_weights() < k:
                to_be_removed.append(v.get_id())

        # Iteratively removed edges with support no less than k
        while len(to_be_removed) > 0:
            u = to_be_removed.pop()
            if not self.vert_dict.has_key(u):
                continue
            # mark neighbours of vertex u
            for w in self.vert_dict[u].get_connections():
                self.remove_edge(u, w.get_id())
                self.remove_edge(w.get_id(), u)
                if (w.get_sum_weights() < k):
                    to_be_removed.append(w.get_id())
            del self.vert_dict[u]
            # Do we want to output u as a community?
            #print u


    #########################################################################
    #   Modified DFS used for finding quasi-cliques in the network          #
    #########################################################################
    def modified_dfs(self, gamma, k, v0, C, CC):
        if len(C) == k:
            # check if it is actually a gamma-quasi k-clique
            CC.append(C)
            return 

        # Maximal number of edges that the result clique can have
        gC = 0
        if gC < gamma * k * (k-1) / 2:
            return
        for v in self.vert_dict[v0].get_connections():
            if v.get_num_neighbors(v.get_id()) > xx:
                modified_dfs(gamma, k, v.get_id(), C+[v], CC)


    #########################################################################
    #   Recursively find the quasi-cliques that include vertex v0           #
    #########################################################################
    def next_clique(self, gamma, k, v0, C, CC):
        C = [v0]
        modified_dfs(gamma, k, v, C, CC)


    #########################################################################
    #   Expand the quasi clique of G[C]                                     #
    #########################################################################
    def expand(self, gamma, k, C):
        C = []


    #########################################################################
    #   This is finding gamma-quasi k-cliques for all query vertices, and   #
    #   outputting one such component for each vertex in query              #
    #########################################################################
    def query_gamma_quasi_k_clique(self, gamma, k, query):
        community = []
        while len(query) > 0:
            v0 = query.pop()
            print v0
            while (1):
                C = []
                CC = []
                self.next_clique(gamma, k, v0, C, CC)
                if len(C) == 0:
                    break
                self.expand(gamma, k, C)
                for u in C:
                    if u in query:
                        query.remove(u)
                community += C

        return community







g = Graph()
gamma = 0.9
k = 10
# Test for large networks
#g.read_graph("edges.txt")
#g.query_gamma_quasi_k_clique(self, 10, 0.9, [0])

g.add_vertex('a')
g.add_vertex('b')
g.add_vertex('c')
g.add_vertex('d')
g.add_vertex('e')
g.add_vertex('f')

g.add_vertex('g')
g.add_vertex('h')
g.add_vertex('i')
g.add_vertex('j')

g.add_edge('a', 'b')  
g.add_edge('a', 'c')
g.add_edge('a', 'f')
g.add_edge('b', 'c')
g.add_edge('b', 'd')
g.add_edge('c', 'd')
g.add_edge('c', 'f')
g.add_edge('d', 'e')
g.add_edge('e', 'f')
g.add_edge('e', 'g')
g.add_edge('g', 'h')
g.add_edge('g', 'i')
g.add_edge('g', 'j')
g.add_edge('h', 'i')
g.add_edge('h', 'j')
g.add_edge('i', 'j')

# Test for detecting gamma-quasi-k-clique
g.query_gamma_quasi_k_clique(gamma, k, ['a', 'b'])

