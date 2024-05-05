# encode x1 + x2 + ... + xn >= k using sequential encoding

n: int
k: int
start_at: int

# 1 -> n: xi

# xi => ri1
def constraint_1():
    c = []
    for i in range (1, n+1):
        c.append([-get_x(i), get_r(i, 1)])
        if i <= k:
            c.append([get_x(i), -get_r(i, i)])
    return c

# -rij
def constraint_2():
    c = []
    for i in range (1, k):
        for j in range (i+1, k+1):
            c.append([-get_r(i, j)])
    return c

# ri-1,j => rij
def constraint_3():
    c = []
    for i in range (2, n+1):
        for j in range (1, k+1):
            c.append([-get_r(i-1, j), get_r(i, j)])
    return c
    
# xi ^ ri-1,j-1 => rij
# -xi ^ -ri-1,j => -rij
# -ri-1,j ^ -ri-1,j-1 => -rij
def constraint_4():
    c = []
    for i in range (2, n+1):
        for j in range (1, k+1):
            if j > 1:
                c.append([-get_x(i), -get_r(i-1, j-1), get_r(i,j)])
                c.append([get_r(i-1,j), get_r(i-1,j-1), -get_r(i,j)])
            c.append([get_x(i), get_r(i-1, j), -get_r(i,j)])
    return c


# rn-1,k v (xn ^ rn-1,k-1) (5.1)
# -xn => rn-1,k (5.2)
# -xi ^ rik => ri-1,k for i > k (5.3)
def constraint_5():
    c = []
    # 5.1
    c.append([get_r(n-1,k), get_x(n)])
    c.append([get_r(n-1,k), get_r(n-1,k-1)])
    # 5.2
    c.append([get_x(n), get_r(n-1,k)])
    # 5.3
    for i in range (k+1, n+1):
        c.append([get_x(i), -get_r(i,k), get_r(i-1,k)])
    return c

def constraints(i_n, i_k, i_start_at):
    global n, k, start_at
    n = i_n
    k = i_k
    start_at = i_start_at
    clauses = []
    clauses.extend(constraint_1())
    clauses.extend(constraint_2())
    clauses.extend(constraint_3())
    clauses.extend(constraint_4())
    clauses.extend(constraint_5())
    return clauses

def get_r(i, j):
    return n+(i-1)*k+j+start_at

def get_x(i):
    return i+start_at
