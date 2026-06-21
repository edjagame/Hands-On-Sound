import subprocess
import sys
import os

def run_script(script_name):
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    if result.returncode != 0:
        print(f"Error: {script_name} failed with exit code {result.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    result = subprocess.run([sys.executable, "process_annotations.py"], cwd="data")
    if result.returncode != 0:
        print("Error: process_annotations.py failed")
        sys.exit(1)

    # The generated .npy files are created inside ml/data/
    # train.py is already configured to look for them in that directory
    # using Path(__file__).parent / "data"

    # Step 2: Train the model
    run_script("train.py")

    run_script("test.py")
