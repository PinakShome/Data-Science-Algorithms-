#!/usr/bin/env python
# coding: utf-8

# In[2]:


def loadGraph(edgeFilename):
    graph = {}
    with open(edgeFilename, 'r') as file:
        for line in file:
            u, v = map(int, line.strip().split())
            if u not in graph:
                graph[u] = []
            if v not in graph:
                graph[v] = []
            graph[u].append(v)
            graph[v].append(u) #undirected graph
    return graph


# In[4]:


class MyQueue:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, item):
        self.queue.append(item)
    
    def dequeue(self):
        return self.queue.pop(0)
    
    def empty(self):
        return len(self.queue) == 0
    
    def __str__(self):
        return str(self.queue)


# In[5]:


def BFS(G, s):
    distances = [-1] * len(G) # Initialize distances to -1 (not visited)
    visited = set()
    q = MyQueue()
    
    q.enqueue(s)
    visited.add(s)
    distances[s] = 0

    while not q.empty():
        current = q.dequeue()
        for neighbor in G[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.enqueue(neighbor)
                distances[neighbor] = distances[current] + 1
                
    return distances


# In[6]:


def distanceDistribution(G):
    distribution = {}
    total_pairs = 0

    for vertex in G:
        distances = BFS(G, vertex)
        for dist in distances:
            if dist > 0: # Avoid self-loop distances
                distribution[dist] = distribution.get(dist, 0) + 1
                total_pairs += 1

    for key in distribution:
        distribution[key] = (distribution[key] / total_pairs) * 100

    return distribution


# In[7]:


if __name__ == '__main__':
    G = loadGraph("/Users/pinakshome/Downloads/edges.txt")
    distribution = distanceDistribution(G)
    print(distribution)


# - Short Path Existence: A large percentage of nodes (approximately 60.35% when you sum percentages for distances 2, 3, and 4) are within 2 to 4 steps away from each other. This provides evidence supporting the small world phenomenon in the dataset.
# 
# - Six Degrees of Separation: If we consider the cumulative percentage up to a distance of 6, we get approximately 95.96%. This means that about 96% of all node pairs are 6 or fewer steps away from each other, echoing the "six degrees of separation" concept.
# 
# - Long Paths Are Rare: Only a small percentage of node pairs have distances greater than 6. For example, only about 2.03% of node pairs are separated by 7 or 8 steps. This further strengthens the idea that most nodes are closely connected.

# - In conclusion, based on the data, the network seems to exhibit the small world phenomenon, with a significant portion of node pairs being closely connected, and the majority of them being within six steps of each other.
