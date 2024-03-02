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

def extract_equations_from_result(filename):
    equations = []
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
                            equations.append(equation)
                            equation = []
                if "c ---- [ profiling ]" in line:
                    break
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", str(e))
    print("Equations extracted from result:", equations)
    return equations

def save_equation_to_file(filename, equations, num_items, num_transactions, min_support):
    with open(filename, 'a') as f:
        for equation in equations:
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

def ignore_solved_equations(file_input, equations):
    # convert all to negative
    equations = [[-int(x) for x in equation] for equation in equations]
    print("Equations converted to neg:", equations)
    num_clauses = 0
    num_vals = 0
    # append all to file_input
    with open(file_input, 'a') as f:
        for equation in equations:
            f.write(' '.join([str(x) for x in equation]) + '\n')
    # update the number of clauses
    with open(file_input, 'r') as f:
        lines = f.readlines()
        _,_, num_vals,num_clauses = lines[0].split()
        new_num_clauses = int(num_clauses) + len(equations)
        lines[0] = "p cnf " + num_vals + " " + str(new_num_clauses) + "\n"
    # write back to file_input
    with open(file_input, 'w') as f:
        f.writelines(lines)
    print("Ignored solved equations:", equations)
    return equations
