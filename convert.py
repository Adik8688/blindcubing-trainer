import os
import json
import sys

def convert_file(input_path, output_path):
    # Load the old JSON data from file
    with open(input_path, 'r') as infile:
        data = json.load(infile)
    
    # Initialize the new data structure
    new_data = {}

    # Process each record from the old JSON
    for key, record in data.items():
        # Extract common fields
        buffer = record.get("buffer")
        first_target = record.get("first_target")
        second_target = record.get("second_target")
        
        # Create a new key combining buffer and targets (e.g., "UF;BD;BL")
        new_key = f"{buffer};{first_target};{second_target}"
        
        # Build the algorithm entry from the record
        alg_entry = {
            "alg": record.get("alg"),
            "results": record.get("results"),
            "latest": record.get("latest"),
            "lp": record.get("lp")
        }
        
        # If this case doesn't exist yet, initialize it with an empty algorithms list
        if new_key not in new_data:
            new_data[new_key] = {"algorithms": []}
        
        # Append the current algorithm entry
        new_data[new_key]["algorithms"].append(alg_entry)
    
    # Write the new data structure to the output file with indentation for readability
    with open(output_path, 'w') as outfile:
        json.dump(new_data, outfile, indent=4)
    
    print(f"Converted {input_path} -> {output_path}")

def convert_directory(input_dir, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate over each file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            try:
                convert_file(input_path, output_path)
            except Exception as e:
                print(f"Failed to convert {input_path}: {e}")

if __name__ == "__main__":
    # Expecting two command-line arguments: input_dir and output_dir
    if len(sys.argv) != 3:
        print("Usage: python convert.py <input_directory> <output_directory>")
        sys.exit(1)
    
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    
    convert_directory(input_directory, output_directory)
