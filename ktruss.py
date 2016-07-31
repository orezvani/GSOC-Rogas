#!/usr/bin/env python

#################################################
#   This code finds k-truss of a given graph    #
#   It also queries vertices in k-trusses       #
#   Author: Mojtaba (Omid) Rezvani              #
#################################################

import sys
from os.path import isfile, join

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]


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


    def add_edge(self, frm, to, cost = 0):
        """ Add connection between frm and to """

        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)


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
            return self.vert_dict[node1].adjacent.has_key(self.vert_dict[node2])
        else:
            return False


    def get_weight(self, node1, node2):
        if node1 in self.vert_dict and node2 in self.vert_dict:
            return self.vert_dict[node1].adjacent.get(self.vert_dict[node2])
        else:
            return -1


    def update_weight(self, node1, node2, new_weight):
        if self.is_connected(node1, node2):
            self.vert_dict[node1].adjacent[self.vert_dict[node2]] = new_weight
            return self.vert_dict[node1].adjacent.get(self.vert_dict[node2])
        else:
            return -1



    def get_vertices(self):
        return self.vert_dict.keys()


    def count_triangles(self):
        # Let's count the number of triangles
        marked = [0] * self.num_vertices
        for v in self:
            for w in v.get_connections():
                marked[self.vert_num[w.get_id()]] = 1
            for w in v.get_connections():
                if self.vert_num[v.get_id()] < self.vert_num[w.get_id()]:
                    kk = 0
                    for y in w.get_connections():
                        if marked[self.vert_num[y.get_id()]] > 0:
                            kk += 1
                    self.update_weight(v.get_id(), w.get_id(), kk)
                    self.update_weight(w.get_id(), v.get_id(), kk)
            for w in v.get_connections():
                marked[self.vert_num[w.get_id()]] = 0


    def detect_ktruss(self, k):
        # Let's detect the k-truss

        # First count the number of triangles
        self.count_triangles()

        # Find some edges to be removed
        to_be_removed = []
        for v in self:
            for w in v.get_connections():
                if self.get_weight(v.get_id(), w.get_id()) < k and self.vert_num[v.get_id()] < self.vert_num[w.get_id()]:
                    to_be_removed.append((v.get_id(), w.get_id()))

        # Iteratively removed edges with support no less than k
        marked = [0] * self.num_vertices
        to_be_decreased = []
        while len(to_be_removed) > 0:
            a, b = to_be_removed.pop()
            self.update_weight(a, b, -1)
            self.update_weight(b, a, -1)
            # mark neighbours of vertex a
            for w in self.vert_dict[a].get_connections():
                if self.get_weight(a, w.get_id()) != -1:
                    marked[self.vert_num[w.get_id()]] = 1
            # get common neighbours of a and b
            for w in self.vert_dict[b].get_connections():
                if marked[self.vert_num[w.get_id()]] > 0 and self.get_weight(b, w.get_id()) != -1:
                    to_be_decreased.append(w.get_id())
            # decrease the support of triangles that were formed by (a,b) using common neighbours of a and b
            for w in to_be_decreased:
                self.update_weight(a, w, self.get_weight(a, w)-1)
                self.update_weight(w, a, self.get_weight(w, a)-1)
                if self.get_weight(a, w) < k and self.get_weight(a, w) > -1:
                    to_be_removed.append((min(a, w), max(a, w)))
                self.update_weight(w, b, self.get_weight(w, b)-1)
                self.update_weight(b, w, self.get_weight(b, w)-1)
                if self.get_weight(b, w) < k and self.get_weight(b, w) > -1:
                    to_be_removed.append((min(b, w), max(b, w)))
            # unmark all neighbours of a for consistency
            for w in self.vert_dict[a].get_connections():
                marked[self.vert_num[w.get_id()]] = 0
            to_be_decreased = []
            







g = Graph()
g.read_graph("edges.txt")
g.detect_ktruss(2)
#g.add_vertex('a')
#g.add_vertex('b')
#g.add_vertex('c')
#g.add_vertex('d')
#g.add_vertex('e')
#g.add_vertex('f')
#
#g.add_vertex('g')
#g.add_vertex('h')
#g.add_vertex('i')
#g.add_vertex('j')
#
#g.add_edge('a', 'b', 7)  
#g.add_edge('a', 'c', 9)
#g.add_edge('a', 'f', 14)
#g.add_edge('b', 'c', 10)
#g.add_edge('b', 'd', 15)
#g.add_edge('c', 'd', 11)
#g.add_edge('c', 'f', 2)
#g.add_edge('d', 'e', 6)
#g.add_edge('e', 'f', 9)
#g.add_edge('e', 'g', 9)
#g.add_edge('g', 'h', 9)
#g.add_edge('g', 'i', 9)
#g.add_edge('g', 'j', 9)
#g.add_edge('h', 'i', 9)
#g.add_edge('h', 'j', 9)
#g.add_edge('i', 'j', 9)
#
#g.count_triangles()
#g.print_edges()
#g.detect_ktruss(2)
#
#g.print_graph()
#g.print_edges()
#
#
