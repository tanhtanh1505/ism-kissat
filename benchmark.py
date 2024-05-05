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
    mode: int = 1, # 1: standard, 2: sequential encoding, 3: old sequential encoding
    time_out: int = 900):
    subprocess.run([
        "python", "main.py", 
        "--input-raw-data", input_raw_data, 
        "--path-cnf", path_cnf, 
        "--min-support", str(min_support), 
        "--output-folder", output_folder, 
        "--prefix-raw-output", prefix_raw_output, 
        "--merged-name", merged_name, 
        "--mode", str(mode), 
        "--time-out", str(time_out)])

def get_info(input):
    n_items = 0
    n_transactions = 0
    with open(input) as f:
        lines = f.readlines()
        n_transactions = len(lines)
        n_items = int(max([int(value) for value in [int(value) for line in lines for value in line.strip().split()]])/2 + 1)
    return n_items, n_transactions

def benchmark(modes=[1, 2, 3], gen_input=False, auto_save_each_test=False):
    inputs = [
              (101, 36, 0.1, './input/real_world/zoo-1.txt'),
              (336, 31, 0.1, './input/real_world/primary-tumor.txt'),
              (435, 48, 0.1, './input/real_world/vote.txt'),
              (630, 50, 0.1, './input/real_world/soybean.txt'),
            (3196, 75, 0.1, './input/real_world/chess.txt'),
            (3196, 75, 0.2, './input/real_world/chess.txt'),
            (3196, 75, 0.3, './input/real_world/chess.txt'),
            (3196, 75, 0.4, './input/real_world/chess.txt'),
            (3196, 75, 0.5, './input/real_world/chess.txt'),
              (8124, 119, 0.1, './input/real_world/mushroom.txt'),
              (8124, 119, 0.2, './input/real_world/mushroom.txt'),
              (8124, 119, 0.3, './input/real_world/mushroom.txt'),

            #   (49046, 2113, 0.03, './input/real_world/pumsb.txt'),
            #   (67558, 129, 0.35, './input/real_world/connect.txt'),
            #   (88162, 16470, 0.0006, './input/real_world/retail.txt'),
            ]

    if gen_input:
        os.system("rm -f ./input/*.txt")
        inputs = []
        n_items = 8
        for n_transactions in [20, 21, 22, 23, 24, 25, 26, 27, 28]:
            for min_support in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]:
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

        if 1 in modes:
            # standard
            if h.get_c_k_n(n_transactions - int(n_transactions*min_support) + 1, n_transactions) > 8000000:
                n_vars = 0
                n_clauses = 0
                n_solutions = 0
                elapsed_time = 0
            else:
                n_solutions, n_vars, n_clauses, elapsed_time = m.process(
                    input_raw_data=input_raw_data,
                    min_support=min_support,
                    mode=1,
                    find_all=True)
            print("Standard:", n_items, n_transactions, min_support, n_solutions, n_vars, n_clauses)
            result["standard/vars"] = n_vars
            result["standard/clauses"] = n_clauses
            result["standard/solutions"] = n_solutions
            result["standard/time"] = elapsed_time
        
        if 3 in modes:
            # old sequential encoding
            n_solutions, n_vars, n_clauses, elapsed_time = m.process(
                input_raw_data=input_raw_data,
                min_support=min_support,
                mode=3,
                output_folder="./output/old_sequential_encoding/",
                find_all=True)
            print("Old sequential encoding:", n_items, n_transactions, min_support, n_solutions, n_vars, n_clauses)
            result["old_sequential_encoding/vars"] = n_vars
            result["old_sequential_encoding/clauses"] = n_clauses
            result["old_sequential_encoding/solutions"] = n_solutions
            result["old_sequential_encoding/time"] = elapsed_time

        if 2 in modes:
            # sequential encoding
            n_solutions, n_vars, n_clauses, elapsed_time = m.process(
                input_raw_data=input_raw_data,
                min_support=min_support,
                mode=2,
                output_folder="./output/sequential_encoding/",
                find_all=True)
            print("Sequential encoding:", n_items, n_transactions, min_support, n_solutions, n_vars, n_clauses)
            result["sequential_encoding/vars"] = n_vars
            result["sequential_encoding/clauses"] = n_clauses
            result["sequential_encoding/solutions"] = n_solutions
            result["sequential_encoding/time"] = elapsed_time

        excel_results.append(result)
        if auto_save_each_test:
            t = time.strftime("%Y%m%d_00")
            h.write_data_to_excel(excel_results, f'./output/{t}/benchmark_{n_transactions}_{min_support}.xlsx', False)
            print("Writen to excel")
    #get unique file name
    t = time.strftime("%Y%m%d_%H")
    # create output path if not exist
    output_path = f'./output/{t}'
    os.makedirs(output_path, exist_ok=True)
    raw_output_path = f'./output/{t}/benchmark_raw.xlsx'
    beauty_output_path = f'./output/{t}/benchmark.xlsx'
    h.write_data_to_excel(excel_results, beauty_output_path, False)
    h.write_data_to_excel(excel_results, raw_output_path)
    h.write_data_to_graph(raw_output_path, output_path, modes)
    

if __name__ == "__main__":
    benchmark(modes=[1, 2, 3], gen_input=True)
