import os
import helper as h
import build_cnf as bc
import argparse
import time

def call_kissat(cnf_file, out_put_path, time_out, times=0):
    os.system("./kissat/build/kissat "+cnf_file+" --time="+str(time_out)+" > "+out_put_path + str(times) +".txt")

def process(input_raw_data: str = "./input/converted_raw_data.txt",
    path_cnf: str = "./input/input.cnf",
    min_support: int = 0.2,
    output_folder: str = "./output/standard/",
    prefix_raw_output: str = "raw_",
    merged_name: str = "merged_equation.txt",
    mode: int = 2, # 1: standard, 2: sequential encoding, 3: old sequential encoding
    time_out: int = 900,
    find_all: bool = False):

    #clear old result
    os.system("rm -f "+output_folder+"*.txt")

    # first run to get the result
    n_solutions = 1
    # build cnf file to path_cnf
    start_time = time.time()
    n_items, n_transactions, n_vars, n_clauses = bc.run(input_raw_data, path_cnf, min_support, mode)
    # call kissat to solve path_cnf
    call_kissat(path_cnf, output_folder + prefix_raw_output, time_out ,n_solutions)

    # loop until no more result
    # statistic and ignore solved solutions
    while find_all:
        equations = h.extract_solutions_from_result(output_folder + prefix_raw_output + str(n_solutions) + ".txt")
        if len(equations) == 0:
            break
        h.save_equation_to_file(output_folder + merged_name , equations, n_items, n_transactions, min_support)
        h.ignore_solved_solutions(path_cnf, equations, n_items)
        n_solutions += 1
        call_kissat(path_cnf,output_folder + prefix_raw_output, time_out, n_solutions)
        # if n_solutions > 10:
        #     break

    elapsed_time = time.time() - start_time
    return n_solutions, n_vars, n_clauses, elapsed_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-raw-data', type=str, default='./input/converted_raw_data.txt', help='Path to the input raw data file', required=False, dest='input_raw_data')
    parser.add_argument('--path-cnf', type=str, default='./input/input.cnf', help='Path to the output CNF file', required=False, dest='path_cnf')
    parser.add_argument('--min-support', type=int, default=0.2, help='Minimum support', required=False, dest='min_support')
    parser.add_argument('--output-folder', type=str, default='./output/standard/', help='Path to the output folder', required=False, dest='output_folder')
    parser.add_argument('--prefix-raw-output', type=str, default='raw_', help='Prefix for the raw output files', required=False, dest='prefix_raw_output')
    parser.add_argument('--merged-name', type=str, default='merged_equation.txt', help='Name of the merged equation file', required=False, dest='merged_name')
    parser.add_argument('--mode', type=bool, default=True, help='Use sequential encoding', required=False, dest='mode')
    parser.add_argument('--time-out', type=int, default=900, help='Time out for kissat', required=False, dest='time_out')
    args = parser.parse_args()
    process(args.input_raw_data, args.path_cnf, args.min_support, args.output_folder, args.prefix_raw_output, args.merged_name, args.mode, args.time_out)