from pathlib import Path
import json
import logging
import logging.config
from logging_config import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def check_or_directory_exists(directory_path: str):
    """
    Check if a directory exists at the specified path.
    If it does not exist, create it.
    Parameters:
        directory_path (str): The path to the directory to check or create.
    Returns:
        bool: True if the directory was created, False if it already existed.
    """
    path = Path(directory_path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory '{directory_path}' created.")
        return f"Directory '{directory_path}' created."
    else:
        logger.info(f"Directory '{directory_path}' already exists.")
        return f"Directory '{directory_path}' already exists."


def write_data_to_json_file(data: list | dict, json_file_path: str) -> str:
    """
    Writes data to a JSON file. If the file does not exist,
    it creates the file and writes the data.
    If the file exists, it append a new data.
    Args:
        data (list | dict): The data to write to the JSON file.
        Can be a list or a dictionary.
        json_file_path (str): The path to the JSON file.
    Returns:
        str: A message indicating whether the file was created or updated.
    """
    path = Path(json_file_path)

    try:
        if isinstance(data, list):
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
                logger.info(f"Data: list successfully written to '{json_file_path}'.")
                return f"Data successfully written to '{json_file_path}'."

        elif isinstance(data, dict):
            with open(path, 'w', encoding='utf-8') as file:
                json.dump([data], file, indent=4)
                logger.info(f"Data: dict successfully written to '{json_file_path}'.")
                return f"Data successfully written to '{json_file_path}'."

        else:
            logger.warning("The provided data must be a list or a dictionary.")
            raise ValueError("The provided data must be a list or a dictionary.")

    except Exception as e:
        logger.error(f"Error writing data to '{json_file_path}': {e}")
        raise


def read_load_json_file(json_file_path: str) -> list:
    """
    Reads JSON data from a file. If the file does not exist, is empty,
    or contains invalid JSON, it returns an empty list without creating a new file.
    Args:
        json_file_path (str): Path to the JSON file.
    Returns:
        list: Parsed JSON data as a list, or an empty list if the file is empty, missing, or invalid.
    """
    path = Path(json_file_path)
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = file.read()
            if data.strip():
                logger.info(f"Successfully loaded data from '{json_file_path}'.")
                return json.loads(data)
            else:
                logger.warning(f"File '{json_file_path}' is empty. Returning an empty list.")
                return []
    except FileNotFoundError:
        logger.warning(f"File '{json_file_path}' not found. Returning an empty list.")
        return []
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON in file '{json_file_path}'. Returning an empty list.")
        return []
