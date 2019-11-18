
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import interp1d
import graph_AL
import graph_EL
from collections import deque

class Graph:
    # Constructor
    def __init__(self, vertices, weighted=False, directed = False):
        self.am = np.zeros((vertices,vertices),dtype=int)-1
        self.weighted = weighted
        self.directed = directed
        self.representation = 'AM'
        
    def insert_edge(self, source, dest, weight=1):
        if source >= len(self.am) or dest >= len(self.am) or source < 0 or dest < 0:
            print('Error, vertex number out of range')
        elif weight != 1 and not self.weighted:
            print('Error, inserting weighted edge to unweighted graph')
        else:
            self.am[source][dest] = weight
            if not self.directed:
                self.am[dest][source] = weight

    def delete_edge(self, source, dest):
        if source >= len(self.am) or dest >= len(self.am) or source < 0 or dest < 0:
            print('Error, vertex number out of range')
        else:
            if self.am[source][dest] == 0:
                print('Error, edge to delete not found')
            self.am[source][dest] = 0
            if not self.directed:
                self.am[dest][source] = 0

    def display(self):
        print('[', end='')
        for i in range(len(self.am)):
            print('[', end='')
            for j in range(len(self.am[i])):
                if self.am[i][j] != 0:
                    print('(' + str(j) + ',' + str(self.am[i][j]) + ')', end='')
            print(']', end=' ')
        print(']')

    def draw(self):
        g = self.as_AL()
        g.draw()

    def as_EL(self):
        g = graph_EL.Graph(len(self.am), weighted=self.weighted, directed=self.directed)
        for i in range(len(self.am)):
            for j in range(len(self.am[i])):
                if self.am[i][j] != 0:
                    if not self.directed:
                        if i < j:
                            g.insert_edge(i, j, self.am[i][j])
                    else:
                        g.insert_edge(i, j, self.am[i][j])
        return g

    def as_AM(self):
        return self

    def as_AL(self):
        g = graph_AL.Graph(len(self.am), weighted=self.weighted, directed=self.directed)
        for i in range(len(self.am)):
            for j in range(len(self.am[i])):
                if self.am[i][j] != 0:
                    if not self.directed:
                        if i < j:  # prevent double edges
                            g.insert_edge(i, j, self.am[i][j])
                    else:
                        g.insert_edge(i, j, self.am[i][j])
        return g

   
    #  depth-first search recursive
    def dfsR(self, begin, end, visited):
        if begin == end:
            return [end]
        tempVisited = list(visited)
        tempVisited.append(begin)
        for j in range(len(self.am[begin])):
            if self.am[begin][j] != 0:
                if j not in tempVisited:
                    path = self.dfsR(j, end, tempVisited)
                    if path is not None:  
                        path.insert(0, begin)
                        return path

    #  depth-first search
    def dfs(self, begin, end):
        path = self.dfsR(begin, end, [])
        if path is None:
            return []  
        return path

    # breadth - first search
    def bfs(self, begin, end):
        q = deque()   
        q.append(begin) 
        visited = [] 
        parent = [0 for i in range(len(self.am))]
        found = False
        while not found and len(q) != 0:
            temp = q.popleft()
            visited.append(temp)
            for j in range(len(self.am[temp])):
                if self.am[temp][j] != 0:
                    if j not in visited:
                        parent[j] = temp
                        if j == end:
                            found = True
                            break
                        q.append(j)
        path = []
        if not found:
            return path
        temp = end
        while temp != begin:
            path.insert(0, temp)
            temp = parent[temp]
        path.insert(0, begin)
        return path



