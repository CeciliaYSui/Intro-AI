class Graph:
    # use python dictonary to represent the graph 
    def __init__(self, graph = {}):
        self.graph = graph

    def connect(self, vertex, adj, distance):
        if vertex not in self.graph.keys():
            self.graph[vertex] = {}
        if adj not in self.graph.keys():
            self.graph[adj] = {}
        # assume symmetric distances between 2 cities 
        self.graph[vertex][adj] = distance
        self.graph[adj][vertex] = distance
        return self

    def getVertices(self):
        return list(self.graph.keys())

    def getChildren(self, vertex):
        return self.graph[vertex]

    def getCost(self, path):
        cost = 0
        extend = path[1:] + [path[0]]
        for vrt, adj in zip(path, extend):
            cost += float(self.graph[vrt][adj])
        return cost

if __name__ == '__main__':
    graph = Graph()
    file = open("test1.txt", "r")
    n = int(file.readline())
    print(n)
    matrix = file.readlines()
    matrix = [i.split() for i in matrix]
    # symmetric matrix 
    for i in range(n):
        for j in range(i+1,n):
            graph.connect(str(i), str(j), matrix[i][j])

    path = ["0", "2", "1", "4", "3"] # input as a list (optimal path for test1.txt, direction doesn't matter)
    print (graph.getCost(path)) # 19
    file.close()