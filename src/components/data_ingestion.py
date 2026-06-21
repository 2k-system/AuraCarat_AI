import os
import sys
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from src.utils.logger import logging
from src.utils.exception import CustomException
from src.utils.common import create_directories

class DataIngestion:
    def __init__(self, config: dict):
        """
        Initializes the data ingestion configuration paths from config.yaml.
        """
        self.config = config['data_ingestion']

    def initiate_data_ingestion(self) -> tuple:
        """
        Loads the diamonds dataset from seaborn, saves the raw records, 
        and performs a clean train-test split.
        """
        logging.info("===== Data Ingestion Phase Started =====")
        try:
            # 1. Fetch data from built-in seaborn repository
            logging.info("Fetching raw diamonds dataset from seaborn library...")
            df = sns.load_dataset('diamonds')
            logging.info(f"Dataset successfully fetched. Row/Col Shape: {df.shape}")

            # 2. Establish structural raw directory paths
            raw_data_dir = self.config['raw_data_dir']
            create_directories([raw_data_dir])

            # 3. Perform Train-Test split
            logging.info("Initiating split execution (80% Train / 20% Test)...")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # 4. Save splits to the artifacts folder
            train_path = self.config['train_data_path']
            test_path = self.config['test_data_path']

            logging.info(f"Saving training data split artifact to: {train_path}")
            train_set.to_csv(train_path, index=False, header=True)

            logging.info(f"Saving testing data split artifact to: {test_path}")
            test_set.to_csv(test_path, index=False, header=True)

            logging.info("===== Data Ingestion Phase Completed Successfully =====")
            return (train_path, test_path)

        except Exception as e:
            raise CustomException(e, sys)
    
    def log_data_profile_summary(df: pd.DataFrame, dataset_name: str = "Dataset"):
    #" Prints a lightweight, clean profile summary of the dataset to the console."
        print("\n" + "="*50)
        print(f"📊 DATA QUALITY PROFILE SUMMARY: {dataset_name.upper()}")
        print("="*50)
        print(f"🔹 Total Rows (Observations): {df.shape[0]}")
        print(f"🔹 Total Columns (Features):  {df.shape[1]}")
        print("-"*50)
    
        print("🔍 DATA TYPES & MISSING VALUES:")
        missing_info = pd.DataFrame({
        'Data Type': df.dtypes,
        'Missing Values': df.isnull().sum(),
        'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
    })
        print(missing_info)
        print("-"*50)
    
        print("📈 PHYSICAL DIMENSIONS HIGHLIGHTS (Min / Max Validation):")
        # Quick sanity check on our crucial x, y, z physical traits
        metrics = ['carat', 'x', 'y', 'z']
        valid_metrics = [m for m in metrics if m in df.columns]
        if valid_metrics:
            print(df[valid_metrics].describe().loc[['min', 'max', 'mean']])
        print("="*50 + "\n")

# if __name__ == "__main__":
#     # 1. Run Data Ingestion
#     ingestion = DataIngestion()
#     train_path, test_path = ingestion.initiate_data_ingestion()
    
#     # 2. Read raw data for an instant profile audit
#     raw_df = pd.read_csv(train_path) 
    
#     # 3. Print out your instant data snapshot right in your terminal!
#     log_data_profile_summary(df=raw_df, dataset_name="Ingested Train Set"