import os
import sys
import pandas as pd
import numpy as np
from src.utils.logger import logging
from src.utils.exception import CustomException

class FeatureEngineering:
    def __init__(self, config: dict):
        """
        Initializes path references. Feature engineering safely acts on 
        the raw split data directly prior to column transformations.
        """
        self.config = config['data_ingestion']

    def engineer_diamond_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates geometric domain-specific properties: Volume and Symmetry.
        """
        try:
            # Avoid chained assignment warnings by working on a clean copy
            df_fe = df.copy()

            logging.info("Calculating engineered feature: Diamond Volume (x * y * z)...")
            # Avoid division/zero errors by adding a tiny epsilon constant to dimensions if 0 exists
            df_fe['volume'] = df_fe['x'] * df_fe['y'] * df_fe['z']

            logging.info("Calculating engineered feature: Dimension Symmetry Ratio (x / y)...")
            # Replace 0s in denominator with median or epsilon to safeguard calculation stability
            df_fe['symmetry_ratio'] = np.where(df_fe['y'] > 0, df_fe['x'] / df_fe['y'], 1.0)

            return df_fe

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_feature_engineering(self, train_path: str, test_path: str) -> tuple:
        """
        Executes feature creation modifications over train and test sets respectively.
        """
        logging.info("===== Feature Engineering Phase Started =====")
        try:
            # 1. Load dataframes
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Input dataset matrices loaded into memory.")

            # 2. Extract engineered features
            logging.info("Injecting synthetic mathematical features into Train partition...")
            train_fe_df = self.engineer_diamond_features(train_df)

            logging.info("Injecting synthetic mathematical features into Test partition...")
            test_fe_df = self.engineer_diamond_features(test_df)

            # 3. Save modified records right back over the target file paths
            train_fe_df.to_csv(train_path, index=False, header=True)
            test_fe_df.to_csv(test_path, index=False, header=True)
            
            logging.info(f"Feature columns engineered successfully. Final Shape: {train_fe_df.shape}")
            logging.info("===== Feature Engineering Phase Completed Successfully =====")
            return (train_path, test_path)

        except Exception as e:
            raise CustomException(e, sys)