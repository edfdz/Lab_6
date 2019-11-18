import matplotlib.pyplot as plt

import graph_AM as graph


if __name__ == "__main__":
    plt.close("all")
    g = graph.Graph(16)
    g.insert_edge(0, 10)
    g.insert_edge(10, 2)
    g.insert_edge(2, 14)
    g.insert_edge(2, 11)
    g.insert_edge(14, 4)
    g.insert_edge(11, 1)
    g.insert_edge(4, 13)
    g.insert_edge(1, 13)
    g.insert_edge(13, 5)
    g.insert_edge(5, 15)
    g.display()
#    g.draw()
    print("Breadth-first search:")
    print(g.bfs(0, 15))
    print("Depth-first search:")
    print(g.dfs(0, 15))


