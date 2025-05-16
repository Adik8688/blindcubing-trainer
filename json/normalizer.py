import json
import os
from pathlib import Path

def normalize_add_difficulty_flag():
    current_dir = Path(__file__).parent  # The directory of the current script

    for filename in os.listdir(current_dir):
        if not filename.endswith(".json"):
            continue

        file_path = current_dir / filename
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        modified = False

        for case_key, record in data.items():
            if "difficult" not in record:
                record["difficult"] = False
                modified = True

        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"✔ Updated '{filename}' with 'difficult': false")
        else:
            print(f"– No changes needed in '{filename}'")

if __name__ == "__main__":
    normalize_add_difficulty_flag()
