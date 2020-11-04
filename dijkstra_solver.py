import array
import math
import numpy as np

# int_max = np.iinfo(np.int32).max
int_max = 1000000

class DijstraSolver:
    def __init__(self, adj_matrix, n_points, start_point):
        self.distances = np.ones(shape = n_points, dtype = np.int32) * int_max
        self.distances[start_point] = 0
        self.labels = np.zeros(shape = n_points, dtype = np.bool)
        self.n_points = n_points
        self.adj_matrix = adj_matrix

    def solve(self):
        for _ in range(self.n_points):
            min_dist_val = int_max
            min_dist_idx = -1
            for i in range(self.n_points):
                if (self.labels[i] == False):
                    if (self.distances[i] < min_dist_val):
                        min_dist_val = self.distances[i]
                        min_dist_idx = i
            if (min_dist_val == int_max):
                break
            else:
                self.labels[min_dist_idx] = True 
                for i in range(self.n_points):
                    cur_edje_len = self.adj_matrix[min_dist_idx, i]
                    if (cur_edje_len != int_max):
                        self.distances[i] = min(self.distances[i], min_dist_val + cur_edje_len)
        return self.distances

def graph_generator(n):
    graph = np.random.randint(low = 1, high = 10, size = [n, n])
    for i in range(n):
        for j in range(n):
            if (i == j):
                graph[i, j] = int_max
            if (i < j):
                graph[i, j] = graph[j, i]
    return graph


def check_solution(adj_matrix):
    from dijkstra import Graph, DijkstraSPF
    n = len(adj_matrix)
    node_names = [str(i) for i in adj_matrix]
    graph = Graph()
    for i in range(n):
        for j in range(n):
            graph.add_edge(node_names[i], node_names[j], adj_matrix[i,j])
    solution = DijkstraSPF(graph, node_names[0])
    result = [solution.get_distance(i) for i in node_names]
    return result

if __name__ == "__main__":
    n = 1000
    adj_matrix = graph_generator(n)
    print(adj_matrix)
    solver = DijstraSolver(adj_matrix, n, 0)
    import time
    now = time.time()
    distances = solver.solve()
    print("Elapsed time: {}".format(time.time() - now))
    print("Is solution right: {}".format(list(distances) == check_solution(adj_matrix)))