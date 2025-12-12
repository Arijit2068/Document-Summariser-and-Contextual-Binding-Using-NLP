import os
import glob

def remove_temp_files():
    """
    Remove temporary files created during troubleshooting.
    """
    temp_files = [
        "replicate_issue.py",
        "temp_nltk_.download.py"
    ]
    
    for file_path in temp_files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Removed temporary file: {file_path}")

if __name__ == "__main__":
    remove_temp_files()