# program2.py
import random
import sys

if __name__ == "__main__":
    if sys.stdin.isatty():
        sys.stdin = open("lab2_independentset/data/g4.in")

def get_input() :
    n = int(input())
    dic = {}
    nodes = set()
    for i in range(1,n+1) :
        nodes.add(i)
        for j, k in enumerate([int(m) for m in input().split()]) :
            dic[(i,j+1)] = k
    
    return (n, nodes, dic)

def alg_R0(n, nodes, dic) :
    if len(nodes) == 0 :
        return 0

    max_degree = -1
    node_max_degree = -1
    degree = get_degree(nodes, dic)
    for i in nodes :
        node_degree = degree(i)
        if node_degree == 0 :
            nodes.remove(i)
            return 1 + alg_R0(n, nodes, dic)
        
        if node_degree > max_degree :
            node_max_degree = i
            max_degree = node_degree
    
    nodes.remove(node_max_degree)
    nodes_without_neighbors = nodes.copy()
    for j in nodes :
        if dic[(node_max_degree,j)] == 1 :
            nodes_without_neighbors.remove(j)
    
    return max(1 + alg_R0(n, nodes_without_neighbors, dic), alg_R0(n, nodes, dic))

def alg_R1(n, nodes, dic) :
    if len(nodes) == 0 :
        return 0

    max_degree = -1
    max_node = -1
    node_degree_1 = -1
    node_degree_0 = -1
    for i in nodes :
        degree = len(dic[i])
        if degree == 1 :    # Find node with 1 neighbor
            node_degree_1 = i
            break
        elif degree == 0 or node_degree_0 != -1 :    # Find node with 0 neighbors
            node_degree_0 = i
        elif degree > max_degree :
            max_node = i
            max_degree = degree

    if node_degree_1 != -1 :
        node_neighbor = dic[node_degree_1].pop()
        nodes.remove(node_degree_1)
        nodes.remove(node_neighbor)
        for k in dic[node_neighbor] :
            dic[k].remove(node_neighbor)
        return 1 + alg_R1(n, nodes, dic)
    
    if node_degree_0 != -1 :
        nodes.remove(node_degree_0)
        return 1 + alg_R1(n, nodes, dic)
    
    nodes.remove(max_node)
    for j in dic[max_node] :
        dic[j].remove(max_node)
    
    dic_neighbors = {key: set(value) for key, value in dic.items()}
    nodes_neighbors = nodes.copy()
    for k in dic[max_node] :
        nodes_neighbors.remove(k)
        for l in dic[k] :
            dic_neighbors[l].remove(k)
    dic[max_node] = set()
    dic_neighbors[max_node] = set()
    return max(1 + alg_R1(n, nodes_neighbors, dic_neighbors), alg_R1(n, nodes, dic))

def get_degree(nodes, dic) :
    degree = {}
    for i in nodes :
        degree[i] = 0
        for j in nodes :
            degree[i] += dic[(i,j)]
    return degree

def main() :
    (n, nodes, dic) = get_input()
    # print(n)
    print(dic)
    degree = get_degree(nodes, dic)
    print(degree)
    # print(nodes)
    max_size = alg_R0(n, nodes, dic)
    print(max_size)


main()