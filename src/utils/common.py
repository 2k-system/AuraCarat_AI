import os
import sys
import yaml
import pickle
from src.utils.logger import logging
from src.utils.exception import CustomException

def read_yaml(path_to_yaml: str) -> dict:
    """
    Reads a YAML configuration file securely and returns a parsed dictionary.
    """
    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"YAML configuration loaded successfully from: {path_to_yaml}")
            return content
    except Exception as e:
        logging.error(f"Failed to read YAML file at {path_to_yaml}")
        raise CustomException(e, sys)

def create_directories(path_to_directories: list):
    """
    Accepts a list of folder paths and creates them if they do not already exist.
    """
    try:
        for path in path_to_directories:
            if path and not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
                logging.info(f"Directory established: {path}")
    except Exception as e:
        logging.error(f"Failed to create directory tracking array at paths: {path_to_directories}")
        raise CustomException(e, sys)

def save_object(file_path: str, obj):
    """
    Serializes and saves a Python object (such as a model or transformer) as a binary pickle file.
    """
    try:
        # Guarantee parent directory layers exist before dumping binary stream
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info(f"Object serialized and saved successfully at: {file_path}")
    except Exception as e:
        logging.error(f"Error occurred during serialization of object to {file_path}")
        raise CustomException(e, sys)

def load_object(file_path: str):
    """
    Loads and re-hydrates a serialized pickle binary file back into a live Python object.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No serial artifact found at target destination: {file_path}")
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        logging.error(f"Failed to load binary artifact from path: {file_path}")
        raise CustomException(e, sys)