# program.py
import random

def get_input() :
    n_m = [int(i) for i in input().split()]
    n = n_m[0]
    m = n_m[1]
    weight = {}
    connection = {}
    for k in range(m) :
        i_j_w = [int(i) for i in input().split()]
        i = i_j_w[0]
        j = i_j_w[1]
        w = i_j_w[2]
        weight[(i,j)] = w
        weight[(j,i)] = w
        if i not in connection :
            connection[i] = set()
        connection[i].add(j)
        if j not in connection :
            connection[j] = set()
        connection[j].add(i)
    return (n,m,weight,connection)

def alg_R(n) :
    A_B = (list([0]*(n+1)),list([0]*(n+1)))
    for i in range(n) :
        A_B[round(random.random())][i+1] = 1
    return A_B

def alg_S(n,m,weight,connection,A_B = None) :
    if A_B is None :
        A_B = (list([0]*(n+1)),list([1]*(n+1)))
    i = 1
    while i <= n :
        value = 0
        for j in connection[i] :
            value += weight[(i,j)] * (1 if A_B[1][j] == 1 else -1) # We assume node i is in B
        in_B = A_B[1][i] == 1 
        value *= (1 if in_B else -1)    # Here we correct if node i is in A
        if value > 0 :  # If True, we swap
            A_B[0][i] = (A_B[0][i] + 1) % 2
            A_B[1][i] = (A_B[1][i] + 1) % 2
            i = 1
            continue
        i += 1
    return A_B

def alg_RS(n,m,weight,connection) :
    return alg_S(n,m,weight,connection,alg_R(n))

def get_max_cut(n,m,weight,connection,A_B) :
    max_cut = 0
    for i in range(1,n+1) :
        i_set = A_B[0] if A_B[0][i] == 1 else A_B[1]
        for j in connection[i] :
            max_cut += weight[(i,j)] * (1 if i_set[j] != 1 else 0)
    max_cut /= 2    # Because I look throught all nodes, I double count the edges, so divide by 2
    return max_cut

def main() :
    (n,m,weight,connection) = get_input()
    t = 100
    algorithm = 0 # which algorithm to run, 0 = R, 1 = S, 2 = RS
    names = ["R", "S", "RS"]
    for algorithm in range(3) :
        print("Algorithm " + names[algorithm])
        max_cut = 0
        agr_max_cut = 0
        for i in range(t) :
            match algorithm :
                case 0:
                    (A,B) = alg_R(n)
                case 1:
                    (A,B) = alg_S(n,m,weight,connection)
                case 2:
                    (A,B) = alg_RS(n,m,weight,connection)
            new_max_cut = get_max_cut(n,m,weight,connection,(A,B))
            agr_max_cut += new_max_cut
            max_cut = max_cut if max_cut > new_max_cut else new_max_cut
            print(new_max_cut)
        print("Average max_cut: " + str(agr_max_cut/t))
        print("Best max_cut: " + str(max_cut))

main()