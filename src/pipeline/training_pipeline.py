import os
import sys
from src.utils.logger import logging
from src.utils.exception import CustomException
from src.utils.common import read_yaml

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.feature_engineering import FeatureEngineering
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher

class TrainingPipeline:
    def __init__(self):
        """
        Loads the core YAML configuration file path to pass down to components.
        """
        self.config_path = os.path.join("configs", "config.yaml")

    def run_pipeline(self):
        """
        Orchestrates and executes the complete MLOps components sequential loop lifecycle.
        """
        try:
            logging.info("==================================================")
            logging.info(">>>>>> STARTING GLOBAL MLOPS TRAINING PIPELINE <<<<<<")
            logging.info("==================================================")
            
            # 0. Load the Configuration Schema Matrix
            config = read_yaml(self.config_path)

            # 1. Component: Data Ingestion
            ingestion = DataIngestion(config=config)
            train_path, test_path = ingestion.initiate_data_ingestion()

            # 2. Component: Data Validation
            validation = DataValidation(config=config)
            validation_status = validation.initiate_data_validation(train_path, test_path)
            
            if not validation_status:
                raise RuntimeError("Pipeline halted: Data validation metrics did not match config schema requirements.")

            # 3. Component: Feature Engineering
            feature_eng = FeatureEngineering(config=config)
            train_path, test_path = feature_eng.initiate_feature_engineering(train_path, test_path)

            # 4. Component: Data Transformation
            transformation = DataTransformation(config=config)
            train_arr, test_arr, _ = transformation.initiate_data_transformation(train_path, test_path)

            # 5. Component: Model Trainer
            trainer = ModelTrainer(config=config)
            model_pkl_path = trainer.initiate_model_trainer(train_arr, test_arr)

            # 6. Component: Model Evaluation
            evaluation = ModelEvaluation(config=config)
            eval_report = evaluation.initiate_model_evaluation(test_arr, model_pkl_path)

            # 7. Component: Model Pusher (Deployment Gate)
            pusher = ModelPusher(config=config)
            push_results = pusher.initiate_model_pusher(evaluation_report=eval_report)

            logging.info("==================================================")
            logging.info(f">>>>>> PIPELINE COMPLETE Execution Status: {push_results['push_status']} <<<<<<")
            logging.info("==================================================")

        except Exception as e:
            logging.error("CRITICAL: Pipeline execution failed mid-lifecycle sequence.")
            raise CustomException(e, sys)

if __name__ == "__main__":
    # Allows direct command line execution test run
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()