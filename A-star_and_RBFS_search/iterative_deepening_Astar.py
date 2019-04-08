from queue import PriorityQueue

class Node:
    def __init__(self, name, h):
        self.name = name
        self.visited = 0
        self.h = h
        self.edge_list = {} #dictionary for edges
    def add_edge(self, vertex, length):
        self.edge_list[vertex] = length

class Graph:
    def __init__(self, glist, hlist):
        elist = glist[2]
        self.vertices = {} #key: node_name, val:node
        self.source_node = 0
        self.sink_node = 0
        #initialize vertices dictionary
        for u, v, _ in elist:
            self.vertices[u] = Node(u, hlist[u])
            self.vertices[v] = Node(v, hlist[v])

        for u, v, len in elist:
            self.vertices[u].add_edge(self.vertices[v], len) #type:0 for real edge
            if self.source_node == 0:
                if u == glist[0]:
                    self.source_node = self.vertices[u]
                if v == glist[0]:
                    self.source_node = self.vertices[v]
            if self.sink_node == 0:
                if u == glist[1]:
                    self.sink_node = self.vertices[u]
                if v == glist[1]:
                    self.sink_node = self.vertices[v]


def FLS(f_limit, q):
    if q.empty():
        return ("not found", f_limit)
    (f_score, g_score, node) = q.get()
    node.visited = 1
    print "node name = ", node.name
    print "node f_score = ", f_score
    if node.name == "g":
        return ("done", f_limit)
    if f_score > f_limit:
        return ("f_limit exceeded", f_score)

    m_limit = float('inf')
    msg = "not found"
    for child in node.edge_list:
        if child.visited == 0:
            child_g_score = node.edge_list[child] + g_score
            child_f_score = child_g_score + child.h
            q.put((child_f_score, child_g_score, child))
            msg, lim = FLS(f_limit, q)
            if msg == "done":
                return (msg, f_limit)
            if m_limit > lim:
                m_limit = lim
    return (msg, m_limit)


def idastar(graph):
    #initial f_limit
    g_score = 0
    f_score = graph.source_node.h + g_score
    f_limit = f_score
    msg = "not done"
    while msg != "done" and msg != "not found":
        q = PriorityQueue()
        q.put((f_score,g_score,graph.source_node))
        msg, f_limit = FLS(f_limit, q)
        print "F:", f_limit, " msg: ", msg
        #clean visits
        for vertex in graph.vertices:
            graph.vertices[vertex].visited = 0


def main():
    glist = ("a", "g", [("a","b",4), ("a","c",2), ("b","d",4), ("b","e",5), ("c","b",4), ("c","e",6), ("c","f",8), ("d","a",10), ("d","g",5), ("d","h",5), ("e","f",7), ("e","g",1), ("f","c",10), ("f","g",5), ("g","h",5), ("h","b",10)])

    hlist = {"a": 3, "b": 2, "c": 3, "d": 2, "e": 1, "f": 5, "g": 0, "h": 5}

    G = Graph(glist, hlist)
    idastar(G)
    #print("ans1: ", ans)

    # glist = (0, 4,  [(0, 1, 2), (0, 3, 6), (1, 2, 3), (1, 3, 8), (1, 4, 5), (2, 4, 7), (3, 4, 9)])
    # g = Graph(glist)
    # ans = Max_Flow_Fat(g)
    # print("ans2: ", ans)

if __name__ == '__main__':
    main()
