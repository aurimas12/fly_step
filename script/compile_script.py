import compileall
from pathlib import Path

script_path = "./script"

def compile_project(directory_path):
    """Compiles all .py files in the given directory and subdirectories."""
    compileall.compile_dir(Path(directory_path), force=True)
    print("Compilation complete. All .pyc files are in __pycache__ folders.")

if __name__ == '__main__':
    compile_project(script_path)
