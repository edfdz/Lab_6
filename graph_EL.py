
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import interp1d
import graph_AL
import graph_AM
from collections import deque

class Edge:
    def __init__(self, source, dest, weight=1):
        self.source = source
        self.dest = dest
        self.weight = weight
        
class Graph:
    # Constructor
    def __init__(self,  vertices, weighted=False, directed = False):
        self.vertices = vertices
        self.el = []
        self.weighted = weighted
        self.directed = directed
        self.representation = 'EL'
        
    def insert_edge(self,source,dest,weight=1):
        if source >= self.vertices or dest >= self.vertices or source < 0 or dest < 0:
            print('Error, vertex number out of range')
        elif weight != 1 and not self.weighted:
            print('Error, inserting weighted edge to unweighted graph')
        else:
            self.el.append(Edge(source, dest, weight))
            if not self.directed:
                self.el.append(Edge(dest, source, weight))
    
    def delete_edge(self,source,dest):
        if source >= self.vertices or dest >= self.vertices or source < 0 or dest < 0:
            print('Error, vertex number out of range')
        else:
            index = -1
            for i in range(len(self.el)):
                if self.el[i].source == source and self.el[i].dest == dest:
                    index = i
            if index != -1:
                del self.el[index]

                if not self.directed:
                    index = -1
                    for i in range(len(self.el)):
                        if self.el[i].source == dest and self.el[i].dest == source:
                            index = i
                    if index != -1:
                        del self.el[index]
            else:
                print('Error, edge to delete not found') 
                
    def display(self):
        print('[', end='')
        for i in range(self.vertices):
            print('[', end='')
            for j in self.el:
                if j.source == i:
                    print('(' + str(j.dest) + ',' + str(j.weight) + ')', end='')
            print(']', end=' ')
        print(']')
     
    def draw(self):
        g = self.as_AL()
        g.draw() 
            
    def as_EL(self):
        return self
    
    def as_AM(self):
        g = graph_AM.Graph(self.vertices, weighted=self.weighted, directed=self.directed)
        for i in range(self.vertices):
            for j in self.el:
                if j.source == i:
                    if not self.directed:
                        if i < j.dest:
                            g.insert_edge(i, j.dest, j.weight)
                    else:
                        g.insert_edge(i, j.dest, j.weight)
        return g 
    
    def as_AL(self):
        g = graph_AL.Graph(self.vertices, weighted=self.weighted, directed=self.directed)
        for i in range(self.vertices):
            for j in self.el:
                if j.source == i:
                    if not self.directed:
                        if i < j.dest:    # prevent double edges
                            g.insert_edge(i, j.dest, j.weight)
                    else:
                        g.insert_edge(i, j.dest, j.weight)
        return g
    
    
     #  depth-first search recursive
    def dfsR(self, begin, end, visited):
        if begin == end:
            return [end]
        tempVisited = list(visited)
        tempVisited.append(begin)
        for j in self.el:
            if j.source == begin:
                if j.dest not in tempVisited:
                    path = self.dfsR(j.dest, end, tempVisited)
                    if path is not None:  
                        path.insert(0, begin)
                        return path  

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
        parent = [-1 for i in range(self.vertices)]
        found = False
        while not found and len(q) != 0:
            temp = q.popleft()
            visited.append(temp)
            for j in self.el:
                if j.source == temp:
                    if j.dest not in visited:
                        parent[j.dest] = temp
                        if j.dest == end:
                            found = True
                            break
                        q.append(j.dest)
        path = []
        if not found:
            return path 
        temp = end
        while temp != begin:
            path.insert(0, temp)
            temp = parent[temp]
        path.insert(0, begin)
        return path
