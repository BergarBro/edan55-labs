# r2.py
import random
import sys
import math

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.stdin = open("lab2_independentset/data/g30.in")

def get_input() :
    n = int(input())
    dic = {}
    nodes = set()
    for i in range(1,n+1) :
        nodes.add(i)
        for j, k in enumerate([int(m) for m in input().split()]) :
            dic[(i,j+1)] = k
    
    return (n, nodes, dic)

def alg_R2(n, nodes, dic) :
    if len(nodes) == 0 :    # Check if nodes set is empty
        return 0,0

    max_degree = -1
    node_max_degree = -1
    # Computes the degree of all nodes, and looking for specifc degrees
    degree, node_degree_0, node_degree_1, node_degree_2 = get_degree(nodes, dic, True, True, True)
    if node_degree_2 != -1 :    # If node u has degree 2
        nodes.remove(node_degree_2)
        neighbors = []
        for j in nodes :    # Removes neighbor of node u
            if dic[(node_degree_2, j)] == 1 :
                neighbors.append(j)
        neighbor_1 = neighbors.pop()
        neighbor_2 = neighbors.pop()
        nodes.remove(neighbor_1)
        nodes.remove(neighbor_2)

        if dic[(neighbor_1,neighbor_2)] == 1 :
            size, nbr_rec_call = alg_R2(n, nodes, dic)
            return size + 1, nbr_rec_call + 1
        new_node = n + 1
        for i in nodes :
            edge = dic[(neighbor_1,i)] | dic[(neighbor_2,i)]
            dic[(new_node,i)] = edge
            dic[(i,new_node)] = edge
        dic[(new_node,new_node)] = 0
        nodes.add(new_node)
        size, nbr_rec_call = alg_R2(new_node, nodes, dic)
        return size + 1, nbr_rec_call + 1
    
    if node_degree_1 != -1 :    # If node u has degree 1
        neighbor = -1
        for j in nodes :    # Removes neighbor of node u
            if dic[(node_degree_1, j)] == 1 :
                neighbor = j
                break
        nodes.remove(node_degree_1)
        nodes.remove(neighbor)
        size, nbr_rec_call = alg_R2(n, nodes, dic)
        return size + 1, nbr_rec_call + 1

    if node_degree_0 != -1 :    # If node u has degree 0
        nodes.remove(node_degree_0)
        size, nbr_rec_call = alg_R2(n, nodes, dic)
        return size + 1, nbr_rec_call + 1
    
    for i in nodes :    # Find node with biggest degree
        node_degree = degree[i]
        if node_degree > max_degree :
            node_max_degree = i
            max_degree = node_degree
    
    nodes.remove(node_max_degree)   # Remove node u from graph
    nodes_without_neighbors = nodes.copy()
    for j in nodes :    # Remove node u:s neighbors
        if dic[(node_max_degree,j)] == 1 :
            nodes_without_neighbors.remove(j)   
    size_1, nbr_rec_call_1 = alg_R2(n, nodes_without_neighbors, dic) 
    size_2, nbr_rec_call_2 = alg_R2(n, nodes, dic)
    return max(size_1 + 1, size_2), nbr_rec_call_1 + nbr_rec_call_2 + 2

def get_degree(nodes, dic, look_for_degree_0, look_for_degree_1, look_for_degree_2) :
    degree = {}
    for i in nodes :
        acc_degree = 0
        for j in nodes :
            acc_degree += dic[(i,j)]
        degree[i] = acc_degree
        if acc_degree == 2 and look_for_degree_2:
            return degree, -1, -1, i
        if acc_degree == 1 and look_for_degree_1:
            return degree, -1, i, -1
        if acc_degree == 0 and look_for_degree_0:
            return degree, i, -1, -1
    return degree, -1, -1, -1

def main() :
    (n, nodes, dic) = get_input()
    max_size, rec_calls = alg_R2(n, nodes, dic)
    print(n, max_size, rec_calls, round(math.log(rec_calls),1))


main()