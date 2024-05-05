import methods.sequential_encoding as se
import methods.sequential_encoding_old as old_se
import methods.standard as st
import helper as h
import math

num_items: int
num_transactions: int
min_support: int
mode: int # 1: standard, 2: sequential encoding, 3: old sequential encoding

clauses = []

# q1 ↔ ¬p1 ^ ¬p2 ^ ¬p3
# expect: ((¬q1 | ¬p1) & (¬q1 | ¬p2) & (¬q1 | ¬p3) & (q1 | p1 | p2 | p3))
def build_cnf_for_each_transaction(items, transaction_idx):
    global clauses
    indice_q = num_items + transaction_idx
    neg_items = [item for item in items if item % 2 == 0]
    # constaint (5)
    clauses.extend([[-indice_q, -int(item/2+1)] for item in neg_items])
    # constaint (6)
    c_6 = [indice_q]
    c_6.extend([int(item/2+1) for item in neg_items])
    clauses.append(c_6)

def additional_constraints():
    global clauses
    # at least 1 item in set
    c = [i for i in range(1,num_items+1)]
    clauses.append(c)

def at_least_k():
    global clauses
    # at least k: q1 + q2 + q3 + ... + qn >= k
    c_4 = st.combinations(num_transactions - min_support + 1, num_transactions, num_items)
    clauses.extend(c_4)
    # at least 1 transaction
    c_4_1 = [i + num_items for i in range(1,num_transactions+1)]
    clauses.append(c_4_1)

def at_least_k_se():
    global clauses
    c = se.constraints(num_transactions, min_support, num_items)
    clauses.extend(c)

def at_least_k_old_se():
    global clauses
    c = old_se.constraints(num_transactions, min_support, num_items)
    clauses.extend(c)

def process_file(input_file):
    with open(input_file) as f:
        if mode == 2:
            at_least_k_se()
        elif mode == 3:
            at_least_k_old_se()
        else:
            at_least_k()
        additional_constraints()
        for i, line in enumerate(f):
            # Split the line into individual values
            transaction_idx = i + 1
            values = line.strip().split()
            values = [int(value) for value in values]
            print("Process transaction:", transaction_idx)
            build_cnf_for_each_transaction(values, transaction_idx)
            

def read_params(input_file):
    global num_items, num_transactions, min_support
    with open(input_file) as f:
        lines = f.readlines()
        num_transactions = len(lines)
        min_support = int(math.ceil(min_support * num_transactions))
        num_items = int(max([int(value) for value in [int(value) for line in lines for value in line.strip().split()]])/2 + 1)

def run(input_file = './input/converted_raw_data.txt', output_file = './input/input.cnf', min_supp = 0.2, i_mode = 2):
    global min_support, mode, clauses
    min_support = min_supp
    mode = i_mode
    clauses.clear()
    read_params(input_file)
    process_file(input_file)
    n_vars = h.get_max_item(clauses)
    h.write_cnf_to_file(n_vars, clauses, output_file)
    return num_items, num_transactions, n_vars, len(clauses)
