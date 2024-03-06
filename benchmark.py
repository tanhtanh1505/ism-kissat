import subprocess
import main as m
import helper as h
import time
import os

def run_script(
    input_raw_data: str = "./input/converted_raw_data.txt",
    path_cnf: str = "./input/input.cnf",
    min_support: int = 0.2,
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
    n_items = 8
    for n_transactions in [20, 22, 25, 28, 30]:
        for min_support in [0.1, 0.2, 0.3 ,0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]:
            if n_transactions > 22:
                continue
            path = f'./input/{n_items}_items_{n_transactions}_trans.txt'
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

        if h.get_c_k_n(n_transactions - int(n_transactions*min_support) + 1, n_transactions) > 8000000:
            continue
        
        # standard
        n_solutions, n_vars, n_clauses, elapsed_time = m.process(
            input_raw_data=input_raw_data,
            min_support=min_support,
            find_all=True)
        print("Standard:", n_items, n_transactions, min_support, n_solutions, n_vars, n_clauses)
        result["standard/vars"] = n_vars
        result["standard/clauses"] = n_clauses
        result["standard/solutions"] = n_solutions
        result["standard/time"] = elapsed_time
        
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
    t = time.strftime("%Y%m%d_%H%M%S")
    raw_output_path = f'./output/benchmark_raw_{t}.xlsx'
    output_path = f'./output/benchmark_{t}.xlsx'
    h.write_data_to_excel(excel_results, raw_output_path)
    h.write_data_to_excel(excel_results, output_path, False)
    h.write_data_to_graph(raw_output_path)
    

if __name__ == "__main__":
    benchmark()