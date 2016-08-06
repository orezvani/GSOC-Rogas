#!/usr/bin/env python

#################################################
#   This code finds k-edge-connected component  #
#   of a given graph using random contraction.  #
#   It also queries vertices in kECC            #
#   Author: Mojtaba (Omid) Rezvani              #
#################################################

import sys
import random
from os.path import isfile, join

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
        if self.num_neighbors != self.get_num_neighbors_h():
            print "Error in updating num neighbors"
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
        if self.sum_weights != self.get_sum_weights_h():
            print "Error in updating num neighbors"
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
            # mark neighbours of vertex u
            for w in self.vert_dict[u].get_connections():
                self.remove_edge(u, w.get_id())
                self.remove_edge(w.get_id(), u)
                if (w.get_sum_weights() < k):
                    to_be_removed.append(w.get_id())
            del self.vert_dict[u]
            # Do we want to output u as a community?
            #print u


    def decompose_kcore_by_vertex(self, k, v):
        # Let's decompose the graph into k-cores

        # Find some vertices to be removed
        to_be_removed = [v]

        # Iteratively removed edges with support no less than k
        while len(to_be_removed) > 0:
            u = to_be_removed.pop()
            # mark neighbours of vertex u
            for w in self.vert_dict[u].get_connections():
                self.remove_edge(u, w.get_id())
                self.remove_edge(w.get_id(), u)
                if (w.get_sum_weights() < k):
                    to_be_removed.append(w.get_id())
            del self.vert_dict[u]
            # Do we want to output u as a community?
            #print u


    def detect_connected_components(self):
        # Find the connected components of the graph
        inList = [0] * self.num_vertices
        components = [[]]
        for v in self:
            if inList[self.vert_num[v.get_id()]] == 1:
                continue
            components.append([])
            components[len(components) - 1].append(v.get_id())
            inList[self.vert_num[v.get_id()]] = 1
            qq = 0
            while qq < len(components[len(components) - 1]):
                vv = components[len(components) - 1][qq]
                for u in self.vert_dict[vv].get_connections():
                    if inList[self.vert_num[u.get_id()]] == 0:
                        components[len(components) - 1].append(u.get_id())
                        inList[self.vert_num[u.get_id()]] = 1
                qq += 1
        return components


    # Finds connected components of the graph and returns the list of ID of connected component of each vertex
    def detect_connected_components_inversely(self):
        # Find the connected components of the resulting graph
        inList = [0] * self.num_vertices
        connected_component_of_v = [-1] * self.num_vertices
        c = -1
        for v in self:
            if inList[self.vert_num[v.get_id()]] == 1:
                continue
            c += 1
            connected_component_of_v[self.vert_num[v.get_id()]] = c;
            component = [v.get_id()]
            inList[self.vert_num[v.get_id()]] = 1
            qq = 0
            while qq < len(component):
                vv = component[qq]
                for u in self.vert_dict[vv].get_connections():
                    if inList[self.vert_num[u.get_id()]] == 0:
                        connected_component_of_v[self.vert_num[u.get_id()]] = c;
                        component.append(u.get_id())
                        inList[self.vert_num[u.get_id()]] = 1
                qq += 1
        return connected_component_of_v


    def contract_edge(self, node1, node2):
        u = node1.get_id()
        v = node2.get_id()
        # contract the edge (node1, node2) and merge it
        ## first pick the vertex with less # neighbors (w.l.g. u)
        if node1.get_num_neighbors() > node2.get_num_neighbors():
            u, v = v, u
        # print u, v 
        ## then move all neighbors of u to v
        ## consider weight updates, and edges in opposite direction
        self.remove_edge(v, u)
        self.remove_edge(u, v)
        self.vert_dict[v].add_contracted(self.vert_dict[u])
        for w in self.vert_dict[u].get_connections():
            self.increment_weight(v, w.get_id(), self.get_weight(u, w.get_id()))
            self.increment_weight(w.get_id(), v, self.get_weight(u, w.get_id()))
            self.remove_edge(u, w.get_id())
            self.remove_edge(w.get_id(), u)
        del self.vert_dict[u]
        return v


    # Finds k-edge-connected components of the graph using random contraction
    def decompose_kecc(self, k):
        # First decompose the graph into kcores
        #self.print_graph()
        self.decompose_kcore(k)
        while (len(self.vert_dict) > 1): # 1 will be replaced with a condition on the number of edges
            # randomly pick an edge
            #self.print_edges()
            u = random.randrange(0, len(self.vert_dict))
            u = self.vert_dict.keys()[u]
            v = random.randrange(0, self.vert_dict[u].get_num_neighbors())
            v = self.vert_dict[u].get_neighbor(v).get_id()
            # contract the randomly selected edge
            #print u, v
            if u == v:
                self.remove_edge(self.vert_dict[u], self.vert_dict[v])
                print "An exception happened here; We found a self loop"
                continue
            # v is the remaining vertex after contraction
            v = self.contract_edge(self.vert_dict[u], self.vert_dict[v])
            if self.vert_dict[v].get_sum_weights() < k:
                print self.vert_dict[v].get_contracted()
                self.decompose_kcore_by_vertex(k, v)
            #self.print_edges()
            # remove the updated vertex if its degree is less than k
            #break
            # if the degree of resulting vertex is less than k cut it
        #print "Resulted int he graph"
        #self.print_graph()
        #print self.vert_dict.values()[0].get_contracted()


    # This is finding kECC for different values of k until there is not a connected component that contains all query vertices
    def query_kecc(self, query):
        k = -1
        must_increase_k = True
        community = []
        while must_increase_k:
            k += 1
            # Let's decompose the graph into k-truss
            self.decompose_ktruss(k)
            rcomponents = self.detect_connected_components_inversely()
            t = rcomponents[self.vert_num[query[0]]]
            for q in query:
                if rcomponents[self.vert_num[q]] != t:
                    must_increase_k = False
            if must_increase_k:
                community = []
                for v in self:
                    if rcomponents[self.vert_num[v.get_id()]] == t:
                        community.append(v.get_id())

        return community







g = Graph()
# Test for large networks
#g.read_graph("edges.txt")
#g.detect_kecc(2)

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

g.add_edge('a', 'b', 7)  
g.add_edge('a', 'c', 9)
g.add_edge('a', 'f', 14)
g.add_edge('b', 'c', 10)
g.add_edge('b', 'd', 15)
g.add_edge('c', 'd', 11)
g.add_edge('c', 'f', 2)
g.add_edge('d', 'e', 6)
g.add_edge('e', 'f', 9)
g.add_edge('e', 'g', 9)
g.add_edge('g', 'h', 9)
g.add_edge('g', 'i', 9)
g.add_edge('g', 'j', 9)
g.add_edge('h', 'i', 9)
g.add_edge('h', 'j', 9)
g.add_edge('i', 'j', 9)

# Test for detecting kecc
#g.print_edges()
g.decompose_kecc(20)
#
#g.print_graph()
#g.print_edges()

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
#g.decompose_ktruss(2)
#g.print_graph()
#components = g.detect_connected_components()
#print components

# Test for community search 
#g.print_graph()
#components = g.query_ktruss(['a', 'b'])
#components = g.query_ktruss(['i', 'j'])
#print components


