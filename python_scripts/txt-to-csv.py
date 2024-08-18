import os

def txt_to_csv(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace(".txt", ".csv"))

            # Open the input and output files
            with open(input_path, "r") as input_file, open(output_path, "w") as output_file:
                for line in input_file:
                    # Replace spaces with commas and write to the output file
                    line = line.strip().replace(" ", ",")
                    output_file.write(line + "\n")

# Example usage
input_folder = "permutation_sequences/sequences"
output_folder = "output_folder"
txt_to_csv(input_folder, output_folder)