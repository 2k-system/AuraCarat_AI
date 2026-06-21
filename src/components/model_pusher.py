import os
import sys
import shutil
from src.utils.logger import logging
from src.utils.exception import CustomException
from src.utils.common import create_directories

class ModelPusher:
    def __init__(self, config: dict):
        """
        Initializes the model pusher component.
        Maps the trained source artifacts to the active serving destination.
        """
        self.config = config
        self.trainer_config = config['model_trainer']
        
        # Define the target serving directory inside your app folder
        self.app_model_dir = os.path.join("app", "saved_models")

    def initiate_model_pusher(self, evaluation_report: dict) -> dict:
        """
        Checks performance metrics criteria and deploys the model 
        to the app/ workspace for downstream inference serving.
        """
        logging.info("===== Model Pusher Phase Started =====")
        try:
            # 1. Set performance threshold requirements (e.g., R2 Score > 85%)
            min_r2_threshold = 85.0
            actual_r2 = evaluation_report.get("R2_Score_Percentage", 0.0)

            logging.info(f"Evaluating deployment viability. Min Required R2: {min_r2_threshold}%, Model R2: {actual_r2}%")

            if actual_r2 < min_r2_threshold:
                logging.warning("Model performance did not meet the deployment threshold. Pusher aborted.")
                return {"push_status": "REJECTED", "message": "Performance threshold not achieved."}

            # 2. Define source paths for both the trained model and the matching preprocessing pipeline
            source_model_path = os.path.join(self.trainer_config['model_dir'], self.trainer_config['model_name'])
            source_preprocessor_path = os.path.join(self.config['data_transformation']['processed_dir'], 
                                                    self.config['data_transformation']['preprocessor_name'])

            # 3. Create active application deployment folders
            create_directories([self.app_model_dir])

            dest_model_path = os.path.join(self.app_model_dir, self.trainer_config['model_name'])
            dest_preprocessor_path = os.path.join(self.app_model_dir, self.config['data_transformation']['preprocessor_name'])

            # 4. Copy model and preprocessor objects straight into the app workspace
            logging.info(f"Deploying production model file artifact to: {dest_model_path}")
            shutil.copy_file = shutil.copy(source_model_path, dest_model_path)

            logging.info(f"Deploying production preprocessor transformation asset to: {dest_preprocessor_path}")
            shutil.copy_file = shutil.copy(source_preprocessor_path, dest_preprocessor_path)

            logging.info("===== Model Pusher Phase Completed Successfully (Model Deployed!) =====")
            
            return {
                "push_status": "SUCCESS",
                "deployed_model_path": dest_model_path,
                "deployed_preprocessor_path": dest_preprocessor_path
            }

        except Exception as e:
            raise CustomException(e, sys)