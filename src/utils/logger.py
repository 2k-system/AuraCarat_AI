import os
import sys
from datetime import datetime
import logging

# Generate a unique log filename based on the current execution timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Define and create the absolute path for logs storage
logs_path = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configure the core tracking logging layout
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Add a stdout stream handler to simultaneously mirror logs directly to the terminal screen
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter("[ %(asctime)s ] %(levelname)s - %(message)s"))
logging.getLogger().addHandler(stdout_handler)