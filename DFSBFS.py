# Reilly McbRide 8/29/17
# DFS and BFS Practice for AI I
# http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/

def main():
    graph = {'A': set(['B', 'C']),
             'B': set(['A', 'D', 'E']),
             'C': set(['A', 'F']),
             'D': set(['B']),
             'E': set(['B', 'F']),
             'F': set(['C', 'E'])}

    def dfs(graph, start): # goes down as many adjacent vertices as possible before doubling back
        visited = set()
        stack = [start]
        while stack: # while the stack still has something in it
            vertex = stack.pop() #starts by popping the start, saved in the vertex variable
            if vertex not in visited: # if current vertex hasn't been visited before
                visited.add(vertex) # mark the current vertex as visited by adding it to the set
                #extend iterates through whatever you pass instead of append, which adds as one object
                stack.extend(graph[vertex] - visited) # returns the adjacency list for the current vertex without
                                                      # the ones that have already been visited
        return visited # return the array of all the vertices that were visited

    # key difference: uses a queue instead of a stack (pops least recent add instead of most recent add!)
    def bfs(graph, start): # explores all vertices at a given depth before moving on to their adjacent vertices
        visited = set()
        queue = [start]
        while queue:
            vertex = queue.pop(0) # things that were in the queue first are dealt with before the recent additions
            if vertex not in visited:
                visited.add(vertex)
                queue.extend(graph[vertex] - visited)
        return visited


