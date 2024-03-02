import subprocess
import main as m
import helper as h

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
    inputs = [
        ("./input/converted_raw_data.txt", 6),
        ("./input/input_20_trans.txt", 8),
        ("./input/input_25_trans.txt", 9),
        ("./input/input_28_trans.txt", 10),
        # ("./input/input_30_trans.txt", 8),
    ]
    excel_results = []

    for input_raw_data, min_support in inputs:
        n_items, n_transactions = get_info(input_raw_data)
        result = {
            "input_path": input_raw_data,
            "num_items": n_items,
            "num_transactions": n_transactions,
            "min_support": min_support
        }

        # standard
        n_solutions, n_vars, n_clauses, elapsed_time = m.process(
            input_raw_data=input_raw_data,
            min_support=min_support,
            find_all=False)
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
            find_all=False)
        print("Sequential encoding:", n_items, n_transactions, min_support, n_solutions, n_vars, n_clauses)
        result["sequential_encoding/vars"] = n_vars
        result["sequential_encoding/clauses"] = n_clauses
        result["sequential_encoding/solutions"] = n_solutions
        result["sequential_encoding/time"] = elapsed_time

        excel_results.append(result)
    h.write_data_to_excel(excel_results, "./output/benchmark.xlsx")
    

if __name__ == "__main__":
    benchmark()