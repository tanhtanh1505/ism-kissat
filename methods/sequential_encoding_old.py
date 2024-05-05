# encode x1 + x2 + ... + xn >= k using old sequential encoding

n: int
k: int
start_at: int

# 1 -> n: xi

# xi or ri1
def constraint_1():
    c = []
    for i in range (1, n):
        c.append([get_x(i), get_r(i, 1)])
    return c

# -r1j
def constraint_2():
    c = []
    for j in range (2, k+1):
        c.append([-get_r(1, j)])
    return c

# -ri-1,j or rij
# xi or -ri-1,j-1 or rij
def constraint_3():
    c = []
    for i in range (2, n):
        for j in range (1, k+1):
            c.append([-get_r(i-1, j), get_r(i, j)])
        for j in range (2, k+1):
            c.append([get_x(i), -get_r(i-1, j-1), get_r(i, j)])
    return c
    
# xi or -ri-1,k
def constraint_4():
    c = []
    for i in range (2, n+1):
        c.append([get_x(i), -get_r(i-1, k)])
    return c

def constraints(i_n, i_k, i_start_at):
    global n, k, start_at
    n = i_n
    k = i_n - i_k
    start_at = i_start_at
    clauses = []
    clauses.extend(constraint_1())
    clauses.extend(constraint_2())
    clauses.extend(constraint_3())
    clauses.extend(constraint_4())
    return clauses

def get_r(i, j):
    return n+(i-1)*k+j+start_at

def get_x(i):
    return i+start_at
