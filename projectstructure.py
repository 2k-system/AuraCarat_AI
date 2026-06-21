# import os
# import sys
# from pathlib import Path
# import logging

# # Configure a basic logging format for the setup script
# logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

# while True:
#     project_name = input("Enter the src Folder name (e.g., src) : ").strip()
#     if project_name != '':
#         break

# list_of_files = [
#     ".github/workflows/.gitkeep",
    
#     # Core Application Configuration
#     "configs/config.yaml",
    
#     # Notebooks Workspace 
#     "notebooks/exploration.ipynb",
    
#     # Source Package Structure
#     f"{project_name}/__init__.py",
    
#     # Source Components Layer
#     f"{project_name}/components/__init__.py",
#     f"{project_name}/components/data_ingestion.py",
#     f"{project_name}/components/data_validation.py",
#     f"{project_name}/components/data_transformation.py",
#     f"{project_name}/components/feature_engineering.py",
#     f"{project_name}/components/model_trainer.py",
#     f"{project_name}/components/model_evaluation.py",
#     f"{project_name}/components/model_pusher.py",
    
#     # Source Pipelines Layer
#     f"{project_name}/pipeline/__init__.py",
#     f"{project_name}/pipeline/training_pipeline.py",
#     f"{project_name}/pipeline/prediction_pipeline.py",
    
#     # Source Utilities Layer
#     f"{project_name}/utils/__init__.py",
#     f"{project_name}/utils/common.py",
#     f"{project_name}/utils/logger.py",
#     f"{project_name}/utils/exception.py",
    
#     # Serving / Presentation Layer (App Frontend Assets)
#     "app/static/style.css",
#     "app/templates/index.html",
#     "app/api.py",
#     "app/gradio_app.py",
    
#     # Verification Unit Testing Suite
#     "tests/__init__.py",
    
#     # Root Deployment Configuration Files
#     "Dockerfile",
#     "requirements.txt",
#     "README.md"
# ]

# for filepath in list_of_files:
#     filepath = Path(filepath)
#     filedir, filename = os.path.split(filepath)
    
#     # Securely create directory structure paths if missing
#     if filedir != "":
#         os.makedirs(filedir, exist_ok=True)
#         logging.info(f"Creating directory: {filedir} for the file: {filename}")
        
#     # Build empty target files if they don't exist yet, or keep old changes intact
#     if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
#         with open(filepath, "w") as f:
#             pass
#             logging.info(f"Creating empty file: {filepath}")
#     else:
#         logging.info(f"{filename} already exists and is populated.")

import os
import sys
from pathlib import Path
import logging

# Configure tracking logger format for structure setup execution
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

# Locking the core source package folder name cleanly to "src"
project_name = "src"

list_of_files = [
    ".github/workflows/.gitkeep",
    
    # Core Application Configuration
    "configs/config.yaml",
    
    # Notebooks Workspace 
    "notebooks/exploration.ipynb",
    
    # Artifacts Repositories
    "artifacts/raw_data/.gitkeep",
    "artifacts/processed_data/.gitkeep",
    "artifacts/trained_models/.gitkeep",
    "artifacts/reports/.gitkeep",
    
    # Source Package Base Init
    f"{project_name}/__init__.py",
    
    # Source Components Layer
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/feature_engineering.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/components/model_pusher.py",
    
    # Source Pipelines Layer
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/training_pipeline.py",
    f"{project_name}/pipeline/prediction_pipeline.py",
    
    # Source Utilities Layer
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/common.py",
    f"{project_name}/utils/logger.py",
    f"{project_name}/utils/exception.py",
    
    # Serving UI Layers (Aligned layout)
    "app/templates/index.html",
    "app/templates/style.css",
    "app/api.py",
    "app/gradio_app.py",
    
    # Verification Unit Testing Suite
    "tests/__init__.py",
    
    # Root Deployment Setup Files
    "Dockerfile",
    "requirements.txt",
    "setup.py",
    "README.md"
]

logging.info(f"Initializing structural tree expansion loop for project: {project_name}")

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    
    # Securely build missing nesting folders
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for target artifact asset: {filename}")
        
    # Drop pristine files if missing or currently empty
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass  # Creates empty file asset securely
        logging.info(f"Generated clean blueprint placeholder structure file: {filepath}")
    else:
        logging.info(f"File asset exists with historical code intact, skipping: {filename}")

logging.info("===== AuraCarat MLOps Structural Scaffold Complete! =====")