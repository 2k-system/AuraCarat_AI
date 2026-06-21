import os
import sys
import pandas as pd
from src.utils.logger import logging
from src.utils.exception import CustomException
from src.utils.common import load_object

class PredictionPipeline:
    def __init__(self):
        """
        Points directly to the active production model files deployed by the Model Pusher.
        """
        self.model_path = os.path.join("app", "saved_models", "model.pkl")
        self.preprocessor_path = os.path.join("app", "saved_models", "preprocessor.pkl")

    def predict(self, features: pd.DataFrame) -> float:
        """
        Transforms raw feature attributes using the serialized preprocessor 
        and extracts final pricing predictions from the ensemble regressor model.
        """
        try:
            logging.info("Prediction request received. Loading core deployed models...")
            
            # 1. Load active production model binary elements
            model = load_object(file_path=self.model_path)
            preprocessor = load_object(file_path=self.preprocessor_path)

            logging.info("Preprocessing input features matrix...")
            # 2. Map input variables through transformation rules
            scaled_data = preprocessor.transform(features)

            logging.info("Calculating final pricing prediction inference...")
            # 3. Extract final prediction array value
            prediction = model.predict(scaled_data)

            return float(prediction[0])

        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    def __init__(self, carat: float, cut: str, color: str, clarity: str, 
                 depth: float, table: float, x: float, y: float, z: float):
        """
        Mapping class that cleanly models user inputs from web interfaces or API payloads 
        and structures them directly into standard pandas dataframe shapes.
        """
        self.carat = carat
        self.cut = cut
        self.color = color
        self.clarity = clarity
        self.depth = depth
        self.table = table
        self.x = x
        self.y = y
        self.z = z

    def get_data_as_data_frame(self) -> pd.DataFrame:
        """
        Converts the initialization parameters into a tabular format, 
        injecting the exact synthetic feature engineering formulas (Volume & Symmetry) 
        required by the data pipeline schema layer.
        """
        try:
            # Calculate engineered features exactly as done in training
            volume = self.x * self.y * self.z
            symmetry_ratio = self.x / self.y if self.y > 0 else 1.0

            custom_data_input_dict = {
                "carat": [self.carat],
                "cut": [self.cut],
                "color": [self.color],
                "clarity": [self.clarity],
                "depth": [self.depth],
                "table": [self.table],
                "x": [self.x],
                "y": [self.y],
                "z": [self.z],
                "volume": [volume],
                "symmetry_ratio": [symmetry_ratio]
            }

            df = pd.DataFrame(custom_data_input_dict)
            logging.info(f"Custom client request successfully mapped to DataFrame layout. Features shape: {df.shape}")
            return df

        except Exception as e:
            raise CustomException(e, sys)