import compileall
import importlib.util
from pathlib import Path
from count_timer import count_timer

script_folder_path = "./script"
compiled_file_path = "/Users/home/Github/fly_step/script/__pycache__/ryanair_one_way_cheap.cpython-312.pyc"

def compile_project(directory_pyc_path):
    """Compiles all .py files in the given directory and subdirectories."""
    compileall.compile_dir(Path(directory_pyc_path), force=True)
    print("Compilation complete. All .pyc files are in __pycache__ folders.")

@count_timer
def run_compiled_pyc(compiled_file_apth):
    path = Path(compiled_file_apth)
    if path.exists():
        spec = importlib.util.spec_from_file_location("ryanair_one_way_cheap", compiled_file_apth)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.main()
    else:
        print(f"Compiled .pyc file not found at {compiled_file_apth}")

if __name__ == "__main__":
    compile_project(script_folder_path)
    run_compiled_pyc(compiled_file_path)
