def convert_to_indices(input_file, output_file):
    try:
        with open(input_file, 'r') as source:
            with open(output_file, 'w') as destination:
                for line in source:
                    values = line.strip().split()  # Split the line into individual values
                    indices = [str(i*2 + int(value)) for i, value in enumerate(values)] 
                    destination.write(' '.join(indices) + '\n')  # Write indices to the output file
        print("Output file created successfully!")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", str(e))

input_file = 'raw_data.txt'
output_file = 'converted_raw_data.txt'
convert_to_indices(input_file, output_file)
