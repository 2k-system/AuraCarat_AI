import os
import sys
import json
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.utils.logger import logging
from src.utils.exception import CustomException
from src.utils.common import create_directories, load_object

class ModelEvaluation:
    def __init__(self, config: dict):
        """
        Initializes the model evaluation class configuration targets.
        """
        self.config = config
        self.reports_dir = os.path.join(self.config['artifacts_root'], "reports")

    def eval_metrics(self, actual, pred) -> tuple:
        """
        Calculates standard continuous regression metrics.
        """
        mae = mean_absolute_error(actual, pred)
        rmse = np.sqrt(mean_squared_error(actual, pred))
        r2 = r2_score(actual, pred)
        return mae, rmse, r2

    def initiate_model_evaluation(self, test_array: np.ndarray, model_path: str) -> dict:
        """
        Loads the pickled machine learning model, executes inferences over the 
        test array matrix, and writes the performance report to artifacts.
        """
        logging.info("===== Model Evaluation Phase Started =====")
        try:
            # 1. Separate features (X) and target label pricing values (y) from test matrix
            logging.info("Splitting evaluation array into features and target labels...")
            X_test = test_array[:, :-1]
            y_test = test_array[:, -1]

            # 2. Re-hydrate our trained model binary object
            logging.info(f"Loading trained model asset from path: {model_path}")
            model = load_object(file_path=model_path)

            # 3. Generate pricing inferences
            logging.info("Executing prediction matrix inferences on evaluation test set...")
            predictions = model.predict(X_test)

            # 4. Generate core regression analysis metrics
            mae, rmse, r2 = self.eval_metrics(y_test, predictions)
            
            metrics_report = {
                "Mean_Absolute_Error_USD": float(mae),
                "Root_Mean_Squared_Error_USD": float(rmse),
                "R2_Score_Percentage": float(r2 * 100)
            }
            
            logging.info(f"Evaluation Metrics Calculated: {metrics_report}")

            # 5. Create structural directory for saving evaluation reports
            create_directories([self.reports_dir])
            report_file_path = os.path.join(self.reports_dir, "model_evaluation_report.json")

            # 6. Save the metrics dictionary down as a JSON tracking record
            logging.info(f"Writing calculated metrics summary packet to: {report_file_path}")
            with open(report_file_path, "w") as f:
                json.dump(metrics_report, f, indent=4)

            logging.info("===== Model Evaluation Phase Completed Successfully =====")
            return metrics_report

        except Exception as e:
            raise CustomException(e, sys)