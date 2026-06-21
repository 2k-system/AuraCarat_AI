import os
import sys
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import r2_score

from src.utils.logger import logging
from src.utils.exception import CustomException
from src.utils.common import create_directories, save_object

class ModelTrainer:
    def __init__(self, config: dict):
        """
        Initializes configuration maps for the model training directory framework.
        """
        self.config = config['model_trainer']

    def initiate_model_trainer(self, train_array: np.ndarray, test_array: np.ndarray) -> str:
        """
        Extracts features/targets, performs hyperparameter tuning over an 
        Ensemble Random Forest structure, and serializes the optimal fitted model.
        """
        logging.info("===== Model Training Phase Started =====")
        try:
            # 1. Split training and validation arrays into X matrices and y target vectors
            logging.info("Splitting processed arrays into train/test features and target labels...")
            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            # 2. Define the core Ensemble algorithm and hyperparameter search space
            logging.info("Configuring Random Forest Ensemble hyperparameter search space...")
            rf_regressor = RandomForestRegressor(random_state=42)

            # Keeping grid compact to ensure fast execution via config arguments
            param_distributions = {
                'n_estimators': [50, 100],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5]
            }

            # 3. Initialize Randomized Search cross-validation setup
            search_cv = RandomizedSearchCV(
                estimator=rf_regressor,
                param_distributions=param_distributions,
                n_iter=self.config.get('n_iter', 3),
                cv=self.config.get('cv', 3),
                verbose=1,
                random_state=42,
                n_jobs=-1
            )

            logging.info("Executing grid tune optimization across data arrays...")
            search_cv.fit(X_train, y_train)

            # 4. Extract the best performing estimator layout
            best_model = search_cv.best_estimator_
            logging.info(f"Hyperparameter tuning complete. Best parameters identified: {search_cv.best_params_}")

            # 5. Evaluate the model score on the test array to prevent severe overfitting
            predictions = best_model.predict(X_test)
            r2_evaluation_score = r2_score(y_test, predictions)
            logging.info(f"Model Training validation R2 Score: {r2_evaluation_score * 100:.2f}%")

            if r2_evaluation_score < 0.60:
                raise CustomException("Trained model baseline performance is below the acceptable 60% standard limit.", sys)

            # 6. Secure model directory structure destination and serialize model object
            model_dir = self.config['model_dir']
            create_directories([model_dir])

            model_file_path = os.path.join(model_dir, self.config['model_name'])
            save_object(
                file_path=model_file_path,
                obj=best_model
            )

            logging.info("===== Model Training Phase Completed Successfully =====")
            return model_file_path

        except Exception as e:
            raise CustomException(e, sys)