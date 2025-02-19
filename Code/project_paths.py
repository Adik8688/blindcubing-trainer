# project_paths.py
from pathlib import Path

# Calculate the project root based on this file's location.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define other common directories.
JSON_DIR = PROJECT_ROOT / "Json3"
EXPORTS_DIR = PROJECT_ROOT / "Exports"
FILES_DIR = PROJECT_ROOT / "Files"
STYLE_DIR = PROJECT_ROOT / "Style"
