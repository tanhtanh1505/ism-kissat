import subprocess
import main as m
import helper as h
import time
import os

def run_script(
    input_raw_data: str = "./input/converted_raw_data.txt",
    path_cnf: str = "./input/input.cnf",
    min_support: int = 6,
    output_folder: str = "./output/standard/",
    prefix_raw_output: str = "raw_",
    merged_name: str = "merged_equation.txt",
    use_se: bool = False,
    time_out: int = 900):
    subprocess.run([
        "python", "main.py", 
        "--input-raw-data", input_raw_data, 
        "--path-cnf", path_cnf, 
        "--min-support", str(min_support), 
        "--output-folder", output_folder, 
        "--prefix-raw-output", prefix_raw_output, 
        "--merged-name", merged_name, 
        "--use-se", str(use_se), 
        "--time-out", str(time_out)])

def get_info(input):
    n_items = 0
    n_transactions = 0
    with open(input) as f:
        lines = f.readlines()
        n_transactions = len(lines)
        n_items = int(max([int(value) for value in [int(value) for line in lines for value in line.strip().split()]])/2 + 1)
    return n_items, n_transactions

def benchmark():
    #clear old input
    os.system("rm -f ./input/*.txt")

    # generate input
    inputs = []
    for n_transactions in [20, 25, 28, 30]:
        for percent_item in [10, 15, 20]:
            for percent_k in [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 100]:
                n_items = int(n_transactions * percent_item / 100)
                min_support = int(n_transactions * percent_k / 100)
                path = f'./input/{n_transactions}_trans_{n_items}_items.txt'
                h.generate_input(n_items, n_transactions, path)
                inputs.append((n_transactions, n_items, min_support, path))
    
    excel_results = []

    for n_transactions, n_items, min_support, input_raw_data in inputs:
        result = {
            "input_path": input_raw_data,
            "num_items": n_items,
            "num_transactions": n_transactions,
            "min_support": min_support
        }

        # standard
        if h.get_c_k_n(min_support, n_transactions) <= 8000000:
            # if the number of clauses is too large, the standard method will be skipped
            n_solutions, n_vars, n_clauses, elapsed_time = m.process(
                input_raw_data=input_raw_data,
                min_support=min_support,
                find_all=True)
            print("Standard:", n_items, n_transactions, min_support, n_solutions, n_vars, n_clauses)
            result["standard/vars"] = n_vars
            result["standard/clauses"] = n_clauses
            result["standard/solutions"] = n_solutions
            result["standard/time"] = elapsed_time
        else:
            result["standard/vars"] = "-"
            result["standard/clauses"] = "-"
            result["standard/solutions"] = "-"
            result["standard/time"] = "-"

        # sequential encoding
        n_solutions, n_vars, n_clauses, elapsed_time = m.process(
            input_raw_data=input_raw_data,
            min_support=min_support,
            use_se=True,
            output_folder="./output/sequential_encoding/",
            find_all=True)
        print("Sequential encoding:", n_items, n_transactions, min_support, n_solutions, n_vars, n_clauses)
        result["sequential_encoding/vars"] = n_vars
        result["sequential_encoding/clauses"] = n_clauses
        result["sequential_encoding/solutions"] = n_solutions
        result["sequential_encoding/time"] = elapsed_time

        excel_results.append(result)
    #get unique file name
    name = time.strftime("%Y%m%d_%H%M%S")
    h.write_data_to_excel(excel_results, "./output/benchmark_"+name+".xlsx")
    

if __name__ == "__main__":
    benchmark()