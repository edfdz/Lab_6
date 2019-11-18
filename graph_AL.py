
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import interp1d
import graph_AM
import graph_EL
from collections import deque

class Edge:
    def __init__(self, dest, weight=1):
        self.dest = dest
        self.weight = weight
        
class Graph:
    # Constructor
    def __init__(self, vertices, weighted=False, directed = False):
        self.al = [[] for i in range(vertices)]
        self.weighted = weighted
        self.directed = directed
        self.representation = 'AL'
        
    def insert_edge(self,source,dest,weight=1):
        if source >= len(self.al) or dest>=len(self.al) or source <0 or dest<0:
            print('Error, vertex number out of range')
        elif weight!=1 and not self.weighted:
            print('Error, inserting weighted edge to unweighted graph')
        else:
            self.al[source].append(Edge(dest,weight)) 
            if not self.directed:
                self.al[dest].append(Edge(source,weight))
                
    
    def delete_edge_(self,source,dest):
        i = 0
        for edge in self.al[source]:
            if edge.dest == dest:
                self.al[source].pop(i)
                return True
            i+=1    
        return False
    
    def delete_edge(self,source,dest):
        if source >= len(self.al) or dest>=len(self.al) or source <0 or dest<0:
            print('Error, vertex number out of range')
        else:
            deleted = self.delete_edge_(source,dest)
            if not self.directed:
                deleted = self.delete_edge_(dest,source)
        if not deleted:        
            print('Error, edge to delete not found')      
            
    def display(self):
        print('[',end='')
        for i in range(len(self.al)):
            print('[',end='')
            for edge in self.al[i]:
                print('('+str(edge.dest)+','+str(edge.weight)+')',end='')
            print(']',end=' ')    
        print(']')   
     
    def draw(self):
        scale = 30
        fig, ax = plt.subplots()
        for i in range(len(self.al)):
            for edge in self.al[i]:
                d,w = edge.dest, edge.weight
                if self.directed or d>i:
                    x = np.linspace(i*scale,d*scale)
                    x0 = np.linspace(i*scale,d*scale,num=5)
                    diff = np.abs(d-i)
                    if diff == 1:
                        y0 = [0,0,0,0,0]
                    else:
                        y0 = [0,-6*diff,-8*diff,-6*diff,0]
                    f = interp1d(x0, y0, kind='cubic')
                    y = f(x)
                    s = np.sign(i-d)
                    ax.plot(x,s*y,linewidth=1,color='k')
                    if self.directed:
                        xd = [x0[2]+2*s,x0[2],x0[2]+2*s]
                        yd = [y0[2]-1,y0[2],y0[2]+1]
                        yd = [y*s for y in yd]
                        ax.plot(xd,yd,linewidth=1,color='k')
                    if self.weighted:
                        xd = [x0[2]+2*s,x0[2],x0[2]+2*s]
                        yd = [y0[2]-1,y0[2],y0[2]+1]
                        yd = [y*s for y in yd]
                        ax.text(xd[2]-s*2,yd[2]+3*s, str(w), size=12,ha="center", va="center")
            ax.plot([i*scale,i*scale],[0,0],linewidth=1,color='k')        
            ax.text(i*scale,0, str(i), size=20,ha="center", va="center",
             bbox=dict(facecolor='w',boxstyle="circle"))
        ax.axis('off') 
        ax.set_aspect(1.0)
        
    
            
    def as_EL(self):
         g = graph_EL.Graph(len(self.al), weighted=self.weighted, directed=self.directed)
         for i in range(len(self.al)):
             for edge in self.al[i]:
                 if not self.directed:
                     if i < edge.dest:
                           g.insert_edge(i, edge.dest, edge.weight)
                     else:
                        g.insert_edge(i, edge.dest, edge.weight)
         return g 
    
    def as_AM(self):
        g = graph_AM.Graph(len(self.al), weighted=self.weighted, directed=self.directed)
        for i in range(len(self.al)):
            for edge in self.al[i]:
                if not self.directed:
                    if i < edge.dest: 
                        g.insert_edge(i, edge.dest, edge.weight)
                else:
                    g.insert_edge(i, edge.dest, edge.weight)
        return g
    
    def as_AL(self):
        return self
    
     
    def dfsR(self, begin, end, visited):
        if begin == end:
            return [end]
        tempVisited = list(visited)
        tempVisited.append(begin)
        for edge in self.al[begin]:
            if edge.dest not in tempVisited:
                path = self.dfsR(edge.dest, end, tempVisited)
                if path is not None: 
                    path.insert(0, begin)
                    return path
            

    #  depth-first search
    def dfs(self, begin, end):
        path = self.dfsR(begin,end, [])
        if path is None:
            return [] 
        return path

    # breadth - first search
    def bfs(self, begin, end):
        q = deque()  
        q.append(begin)  
        visited = []  
        parent = [-1 for i in range(len(self.al))]
        found = False
        while not found and len(q) != 0:
            temp = q.popleft()
            visited.append(temp)
            for edge in self.al[temp]:
                if edge.dest not in visited:
                    parent[edge.dest] = temp
                    if edge.dest == end:
                        found = True
                        break
                    q.append(edge.dest)
        path = []
        if not found:
            return path 
        temp = end
        while temp != begin:
            path.insert(0, temp)
            temp = parent[temp]
        path.insert(0, begin)
        return path
