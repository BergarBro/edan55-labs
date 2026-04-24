# program.py
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
        dic[i] = set()
        for j, k in enumerate([int(m) for m in input().split()]) :
            if k == 1 :
                dic[i].add(j+1)
    
    return (n, nodes, dic)

def alg_R0(n, nodes, dic) :
    # print(len(nodes))
    if len(nodes) == 0 :
        return 0

    max_degree = 0
    max_node = 0
    for i in nodes :
        degree = len(dic[i])
        if degree == 0 :
            nodes.remove(i)
            return 1 + alg_R0(n, nodes, dic)
        
        if degree > max_degree :
            max_node = i
            max_degree = degree
    
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
    return max(1 + alg_R0(n, nodes_neighbors, dic_neighbors), alg_R0(n, nodes, dic))

def main() :
    (n, nodes, dic) = get_input()
    # print(n)
    # print(dic)
    # print(nodes)
    max_size = alg_R0(n, nodes, dic)
    print(max_size)


main()