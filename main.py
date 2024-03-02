import os
import helper as h
import build_cnf as bc
import argparse

def call_kissat(cnf_file, out_put_path, time_out, times=0):
    os.system("./kissat/build/kissat "+cnf_file+" --time="+str(time_out)+" > "+out_put_path + str(times) +".txt")

def process(input_raw_data: str = "./input/converted_raw_data.txt",
    path_cnf: str = "./input/input.cnf",
    min_support: int = 6,
    output_folder: str = "./output/standard/",
    prefix_raw_output: str = "raw_",
    merged_name: str = "merged_equation.txt",
    use_se: bool = False,
    time_out: int = 900):

    #clear old result
    os.system("rm -f "+output_folder+"*.txt")

    # first run to get the result
    times = 1
    # build cnf file to path_cnf
    num_items, num_transactions, min_support = bc.run(input_raw_data, path_cnf, 6, use_se)
    # call kissat to solve path_cnf
    call_kissat(path_cnf, output_folder + prefix_raw_output, time_out ,times)

    # loop until no more result
    # statistic and ignore solved equations
    while True:
        equations = h.extract_equations_from_result(output_folder + prefix_raw_output + str(times) + ".txt")
        if len(equations) == 0:
            break
        h.save_equation_to_file(output_folder + merged_name , equations, num_items, num_transactions, min_support)
        h.ignore_solved_equations(path_cnf, equations)
        times += 1
        call_kissat(path_cnf,output_folder + prefix_raw_output, time_out, times)
        # if times > 10:
        #     break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-raw-data', type=str, default='./input/converted_raw_data.txt', help='Path to the input raw data file', required=False, dest='input_raw_data')
    parser.add_argument('--path-cnf', type=str, default='./input/input.cnf', help='Path to the output CNF file', required=False, dest='path_cnf')
    parser.add_argument('--min-support', type=int, default=6, help='Minimum support', required=False, dest='min_support')
    parser.add_argument('--output-folder', type=str, default='./output/standard/', help='Path to the output folder', required=False, dest='output_folder')
    parser.add_argument('--prefix-raw-output', type=str, default='raw_', help='Prefix for the raw output files', required=False, dest='prefix_raw_output')
    parser.add_argument('--merged-name', type=str, default='merged_equation.txt', help='Name of the merged equation file', required=False, dest='merged_name')
    parser.add_argument('--use-se', type=bool, default=False, help='Use sequential encoding', required=False, dest='use_se')
    parser.add_argument('--time-out', type=int, default=900, help='Time out for kissat', required=False, dest='time_out')
    args = parser.parse_args()
    process(args.input_raw_data, args.path_cnf, args.min_support, args.output_folder, args.prefix_raw_output, args.merged_name, args.use_se, args.time_out)