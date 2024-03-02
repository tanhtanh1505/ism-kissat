import subprocess

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

def benchmark():
    # standard
    run_script()
    # sequential encoding
    run_script(use_se=True,
        output_folder="./output/sequential_encoding/",
        prefix_raw_output="raw_")

if __name__ == "__main__":
    benchmark()