import os
import sys
import pandas as pd
from src.utils.logger import logging
from src.utils.exception import CustomException
from src.utils.common import create_directories

class DataValidation:
    def __init__(self, config: dict):
        """
        Initializes data validation configuration maps and targets from config.yaml.
        """
        self.config = config['data_validation']

    def validate_all_columns(self, csv_path: str) -> bool:
        """
        Compares data columns and data types against the required configuration schema map.
        Writes validation reports to a tracking text file artifact destination.
        """
        try:
            validation_status = True
            df = pd.read_csv(csv_path)
            
            # Extract expected columns and datatypes map from configs
            expected_schema = self.config['required_columns']
            all_cols = list(df.columns)

            # Ensure reports path directory folder exists
            status_file_path = self.config['status_file']
            create_directories([os.path.dirname(status_file_path)])

            # Core validation logic loop
            report_msg = []
            for col, expected_dtype in expected_schema.items():
                if col not in all_cols:
                    validation_status = False
                    report_msg.append(f"CRITICAL: Missing column attribute -> [{col}]")
                else:
                    # Match clean standard strings for data types
                    actual_dtype = str(df[col].dtype)
                    if actual_dtype != expected_dtype:
                        # Allow flexible matching for integers (e.g., int64 vs int32)
                        if "int" in actual_dtype and "int" in expected_dtype:
                            continue
                        validation_status = False
                        report_msg.append(f"TYPE ERROR: Column [{col}] expected {expected_dtype}, got {actual_dtype}")

            # 3. Write final assessment records into the status report artifact
            with open(status_file_path, "w") as f:
                if validation_status:
                    f.write(f"Validation Status: SUCCESS\nFile evaluated: {csv_path}\nAll data criteria matched structural schema rules.")
                    logging.info("Schema validation passed cleanly. Data structure is stable.")
                else:
                    f.write(f"Validation Status: FAILED\nIssues detected:\n" + "\n".join(report_msg))
                    logging.warning(f"Data structural validation failed for file {csv_path}. Review logs at {status_file_path}")

            return validation_status

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_validation(self, train_path: str, test_path: str) -> bool:
        """
        Triggers explicit schema checks on both your train and test data splits.
        """
        logging.info("===== Data Validation Phase Started =====")
        try:
            # Validate train data
            train_status = self.validate_all_columns(train_path)
            # Validate test data
            test_status = self.validate_all_columns(test_path)
            
            overall_status = train_status and test_status
            
            logging.info(f"===== Data Validation Complete. Status Result: {overall_status} =====")
            return overall_status

        except Exception as e:
            raise CustomException(e, sys)