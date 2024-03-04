from openpyxl import Workbook
import random
import math

def extract_numbers(line):
    numbers = []
    is_end = False
    for word in line.split():
        if word.isdigit() or (word.startswith('-') and word[1:].isdigit()):
            numbers.append(int(word))
            if int(word) == 0:
                is_end = True
                break
    return numbers, is_end

def extract_solutions_from_result(filename):
    solutions = []
    try:
        with open(filename, 'r') as file:
            found_result = False
            equation = []
            for line in file:
                if "c ---- [ result ]" in line:
                    found_result = True
                if found_result and line.startswith("v"):
                        e, is_end = extract_numbers(line.strip())
                        equation.extend(e)
                        if is_end:
                            solutions.append(equation)
                            equation = []
                if "c ---- [ profiling ]" in line:
                    break
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", str(e))
    return solutions

def save_equation_to_file(filename, solutions, num_items, num_transactions, min_support):
    with open(filename, 'a') as f:
        for equation in solutions:
            item_set = set()
            valid_transactions = set()
            for item in equation:
                if item > 0:
                    if item <= num_items:
                        item_set.add(item)
                    elif item <= num_items + num_transactions:
                        valid_transactions.add(item - num_items)
            f.write("=================================================================\n")
            f.write(' '.join([str(x) for x in equation]) + '\n')
            f.write("Number of items: " + str(num_items) + '\n')
            f.write("Number of transactions: " + str(num_transactions) + '\n')
            f.write("Minimum support: " + str(min_support) + '\n')
            f.write("Item set found: " + str(item_set) + '\n')
            f.write("Valid transactions: " + str(valid_transactions) + '\n')
            f.write("=================================================================\n")

def ignore_solved_solutions(file_input, solutions):
    # convert all to negative
    solutions = [[-int(x) for x in equation] for equation in solutions]
    num_clauses = 0
    num_vals = 0
    # append all to file_input
    with open(file_input, 'a') as f:
        for equation in solutions:
            f.write(' '.join([str(x) for x in equation]) + '\n')
    # update the number of clauses
    with open(file_input, 'r') as f:
        lines = f.readlines()
        _,_, num_vals,num_clauses = lines[0].split()
        new_num_clauses = int(num_clauses) + len(solutions)
        lines[0] = "p cnf " + num_vals + " " + str(new_num_clauses) + "\n"
    # write back to file_input
    with open(file_input, 'w') as f:
        f.writelines(lines)
    return solutions

def get_max_item(clauses):
    max_item = 0
    for clause in clauses:
        for item in clause:
            max_item = max(max_item, abs(item))
    return max_item

def write_cnf_to_file(vars, clauses, output_file):
    with open(output_file, 'w') as writer:
        # Write a line of information about the number of variables and constraints
        writer.write("p cnf " + str(vars) + " " + str(len(clauses)) + "\n")
        # Write each clause to the file
        for clause in clauses:
            for literal in clause:
                writer.write(str(literal) + " ")
            writer.write("0\n")

def write_data_to_excel(data, path):
    # Generate header
    raw_header = data[0].keys()
    header = []
    sub_header = []
    list_need_merge = []
    cur_col = 'A'
    header_merge = ""
    start_merge_cel = ""
    end_merge_cel = ""
    for idx, key in enumerate(raw_header):
        num_sub_header = len(key.split("/"))
        if num_sub_header > 1:
            cur_header = key.split("/")[0]
            header.append(cur_header)
            sub_header.append(key.split("/")[1])
            
            if header_merge != cur_header:
                if start_merge_cel != "" and end_merge_cel != "" and start_merge_cel != end_merge_cel:
                    list_need_merge.append(f'{start_merge_cel}:{end_merge_cel}')
                start_merge_cel = cur_col + str(1)
                header_merge = cur_header
            
            end_merge_cel = cur_col + str(1)
            if idx == len(raw_header) - 1:
                list_need_merge.append(f'{start_merge_cel}:{end_merge_cel}')
        else:
            header.append(key)
            sub_header.append("")
            list_need_merge.append(f'{cur_col + str(1)}:{cur_col + str(2)}')
        cur_col = chr(ord(cur_col) + 1)
    # write to excel
    book = Workbook()
    sheet = book.active
    sheet.append(header)
    sheet.append(sub_header)
    for d in data:
        sheet.append([d[key] for key in raw_header])
    for merge in list_need_merge:
        sheet.merge_cells(merge)
    book.save(path)

def generate_input(n_items, n_transactions, output):
    with open(output, "w") as f:
        for i in range(n_transactions):
            for j in range(n_items):
                is_true = random.choice([0, 1])
                f.write(str(j*2 + is_true) + " ")
            f.write("0\n")

def get_c_k_n(k, n):
    return int(math.factorial(n) / (math.factorial(k) * math.factorial(n - k)))