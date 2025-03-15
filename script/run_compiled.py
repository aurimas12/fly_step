import importlib.util
from pathlib import Path
from count_timer import count_timer



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
    # TODO: mano path skirsis del to geriau nenaudot taip,pasiziurek cia  budus https://www.geeksforgeeks.org/find-path-to-the-given-file-using-python/
    compiled_file_path = "/Users/home/Github/fly_step/script/__pycache__/ryanair_one_way_cheap.cpython-312.pyc"
    run_compiled_pyc(compiled_file_path)
