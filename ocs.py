#!/usr/bin/env python

#################################################
#   This code finds communities of a given      #
#   graph. According to papge: "Searching       #
#   overlapping communities for group query"    #
#   by Shan et al.                              #
#   Author: Mojtaba (Omid) Rezvani              #
#################################################

import sys
import random
from os.path import isfile, join
import copy

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        self.contracted = [node]
        self.num_neighbors = 0
        self.sum_weights = 0


    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])


    def add_neighbor(self, neighbor, weight=1):
        if not self.adjacent.has_key(neighbor):
            self.num_neighbors += 1
            self.sum_weights += weight
        self.adjacent[neighbor] = weight


    def has_neighbor(self, neighbor):
        return self.adjacent.has_key(neighbor)


    def remove_neighbor(self, neighbor):
        if self.adjacent.has_key(neighbor):
            self.num_neighbors -= 1
            self.sum_weights -= self.adjacent[neighbor]
            del self.adjacent[neighbor]


    def get_connections(self):
        return self.adjacent.keys()  


    def get_neighbor(self, i):
        return self.adjacent.keys()[i]


    # getting the num of neighbors the hard way -- used for testing
    def get_num_neighbors_h(self):
        return len(self.adjacent)


    def get_num_neighbors(self):
        # Testing script; It will be commented out
        #if self.num_neighbors != self.get_num_neighbors_h():
        #    print "Error in updating num neighbors"
        return self.num_neighbors


    def get_id(self):
        return self.id


    def get_weight(self, neighbor):
        return self.adjacent[neighbor]


    # be careful, this is dangrouse. We check whether the connection exists in the graph class
    def update_weight(self, neighbor, new_weight):
        if self.has_neighbor(neighbor):
            self.sum_weights -= self.adjacent[neighbor]
            self.adjacent[neighbor] = new_weight
        else:
            print "Shout: The edge does not exit"


    # if the edge does not exist, it means that its weight is zero
    def increment_weight(self, neighbor, inc_value):
        if self.has_neighbor(neighbor):
            self.adjacent[neighbor] += inc_value
        else:
            self.adjacent[neighbor] = inc_value
            self.num_neighbors += 1
        self.sum_weights += inc_value


    # getting the sum of weights the hard way -- used for testing
    def get_sum_weights_h(self):
        return sum(self.adjacent.values())


    def get_sum_weights(self):
        # Testing script; It will be commented out
        #if self.sum_weights != self.get_sum_weights_h():
        #    print "Error in updating num neighbors"
        return self.sum_weights


    def add_contracted(self, neighbor):
        self.contracted += neighbor.get_contracted()


    def get_contracted(self):
        return self.contracted




class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.vert_num = {}
        self.num_vertices = 0


    def read_graph(self, graph_file):
        """ Add connections (list of tuple pairs) to graph """

        with open(graph_file) as gf:
            for line in gf:
                e = [int(v) for v in line.split()]
                self.add_edge(e[0], e[1])
        gf.close()


    def __iter__(self):
        return iter(self.vert_dict.values())


    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        self.vert_num[node] = self.num_vertices - 1
        return new_vertex


    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None


    def add_edge(self, frm, to, cap = 1):
        """ Add connection between frm and to """

        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cap)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cap)


    def remove_edge(self, frm, to):
        """ Remove connection between frm and to """

        if self.is_connected(frm, to):
            self.vert_dict[frm].remove_neighbor(self.vert_dict[to])
            self.vert_dict[to].remove_neighbor(self.vert_dict[frm])


    def print_edges(self):
        for v in self:
            for w in v.get_connections():
                vid = v.get_id()
                wid = w.get_id()
                print '( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w))


    def print_graph(self):
        for v in self:
            print 'g.vert_dict[%s]=%s' %(v.get_id(), self.vert_dict[v.get_id()])


    def is_connected(self, node1, node2):
        if node1 in self.vert_dict and node2 in self.vert_dict:
            return self.vert_dict[node1].has_neighbor(self.vert_dict[node2])
        else:
            return False


    def get_weight(self, node1, node2):
        if node1 in self.vert_dict and node2 in self.vert_dict:
            return self.vert_dict[node1].get_weight(self.vert_dict[node2])
        else:
            return -1


    def update_weight(self, node1, node2, new_weight):
        if self.is_connected(node1, node2):
            #self.vert_dict[node1].adjacent[self.vert_dict[node2]] = new_weight
            self.vert_dict[node1].update_weight(self.vert_dict[node2], new_weight)
            return self.vert_dict[node1].get_weight(self.vert_dict[node2])
        else:
            return -1


    def increment_weight(self, node1, node2, inc_by = 1):
        self.vert_dict[node1].increment_weight(self.vert_dict[node2], inc_by)
        #if self.is_connected(node1, node2):
        #    self.vert_dict[node1].adjacent[self.vert_dict[node2]] += inc_by
        #    return self.vert_dict[node1].adjacent.get(self.vert_dict[node2])
        #else:
        #    self.add_edge(node1, node2, inc_by)
        #    return inc_by


    def get_vertices(self):
        return self.vert_dict.keys()


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


    # This is finding kECC for different values of k until there is not a connected component that contains all query vertices
    def query_gamma_quasi_k_clique(self, gamma, k, query):
        community = []
        while len(query) > 0:
            v0 = query.pop()
            # Let's decompose the graph into kECC

        return community







g = Graph()
gamma = 0.9
k = 10
# Test for large networks
#g.read_graph("edges.txt")
#g.decompose_kecc(5)

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
g.query_gamma_quasi_k_clique(gamma, k, 'a')

# Test for removing edges
#g.print_edges()
#g.print_graph()
#print ""
#g.remove_edge('a', 'b')
#g.print_graph()
#g.print_edges()


# Test for ktruss with edge removals
#g.print_edges()
#print ""
#g.decompose_ktruss(2)
#g.print_edges()

# Test for connected components
#g.print_graph()
#g.decompose_kecc(2)
#g.print_graph()
#components = g.detect_connected_components()
#print components

# Test for community search 
#g.print_graph()
#components = g.query_kecc(['a', 'b'])
##components = g.query_kecc(['i', 'j'])
#print components


