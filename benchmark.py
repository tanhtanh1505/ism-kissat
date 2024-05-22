import main as m
import helper as h
import time
import os

def benchmark(modes=[1, 2, 3], 
              find_all=False, 
              auto_save_each_test=False, 
              write_data_to_graph=False, 
              gen_input=False, 
              range_trans = [20, 21, 22, 23, 24, 25, 26, 27, 28],
              range_min_support = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
              ):
    inputs = [
            (101, 36, 0.9, './input/real_world/zoo-1.txt'),
            (336, 31, 0.9, './input/real_world/primary-tumor.txt'),
            (435, 48, 0.9, './input/real_world/vote.txt'),
            (630, 50, 0.9, './input/real_world/soybean.txt'),
            (3196, 75, 0.6, './input/real_world/chess.txt'),
            (3196, 75, 0.7, './input/real_world/chess.txt'),
            (3196, 75, 0.8, './input/real_world/chess.txt'),
            (3196, 75, 0.9, './input/real_world/chess.txt'),
            (3196, 75, 0.5, './input/real_world/chess.txt'),
            (8124, 119, 0.9, './input/real_world/mushroom.txt'),
            (8124, 119, 0.8, './input/real_world/mushroom.txt'),
            (8124, 119, 0.7, './input/real_world/mushroom.txt'),
            (8124, 119, 0.6, './input/real_world/mushroom.txt'),
            (8124, 119, 0.5, './input/real_world/mushroom.txt'),
            (8124, 119, 0.4, './input/real_world/mushroom.txt'),

            #   (49046, 2113, 0.03, './input/real_world/pumsb.txt'),
            #   (67558, 129, 0.35, './input/real_world/connect.txt'),
            #   (88162, 16470, 0.0006, './input/real_world/retail.txt'),
            ]

    if gen_input:
        os.system("rm -f ./input/*.txt")
        inputs = []
        n_items = 8
        for n_transactions in range_trans:
            for min_support in range_min_support:
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
                    find_all=find_all)
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
                find_all=find_all,
                time_out=360000)
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
                find_all=find_all)
            print("Sequential encoding:", n_items, n_transactions, min_support, n_solutions, n_vars, n_clauses)
            result["sequential_encoding/vars"] = n_vars
            result["sequential_encoding/clauses"] = n_clauses
            result["sequential_encoding/solutions"] = n_solutions
            result["sequential_encoding/time"] = elapsed_time

        excel_results.append(result)
        if auto_save_each_test:
            t = time.strftime("%Y%m%d_00")
            output_path = f'./output/{t}'
            os.makedirs(output_path, exist_ok=True)
            h.write_data_to_excel(excel_results, output_path + f'/benchmark_{n_transactions}_{min_support}.xlsx', True)
            print("Writen to excel")
    
    if auto_save_each_test == False:
        t = time.strftime("%Y%m%d_%H")
        output_path = f'./output/{t}'
        os.makedirs(output_path, exist_ok=True)
        raw_output_path = f'./output/{t}/benchmark_raw.xlsx'
        beauty_output_path = f'./output/{t}/benchmark.xlsx'
        h.write_data_to_excel(excel_results, beauty_output_path, False)
        h.write_data_to_excel(excel_results, raw_output_path)
    
    if write_data_to_graph:
        h.write_data_to_graph(raw_output_path, output_path, modes)
        h.write_data_to_each_graph(raw_output_path, output_path, modes)
    

if __name__ == "__main__":
    benchmark(modes=[1,2,3], 
              find_all=True, 
              write_data_to_graph=True,
              gen_input=True, 
              range_trans=[20],
              range_min_support=[0.1, 0.2, 0.3]
              )
