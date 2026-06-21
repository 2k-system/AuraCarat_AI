# import os
# import sys
# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel

# from src.pipeline.prediction_pipeline import PredictionPipeline, CustomData
# from src.utils.logger import logging

# app = FastAPI(title="AuraCarat AI Serving API Architecture")

# # Mount directory references to access style.css safely
# app.mount("/templates", StaticFiles(directory="app/templates"), name="templates")

# # Form input parsing data model contract schema
# class DiamondInputModel(BaseModel):
#     carat: float = Field(default=0.7, gt=0, le=5.0)
#     cut: str
#     color: str
#     clarity: str
#     depth: float = Field(default=61.5, gt=0, le=100.0)
#     table: float = Field(default=57.0, gt=0, le=100.0)
#     x: float = Field(default=5.7, gt=0)
#     y: float = Field(default=5.7, gt=0)
#     z: float = Field(default=3.5, gt=0)

# @app.get("/", response_class=HTMLResponse)
# async def serve_home_page():
#     """
#     Renders the custom HTML dashboard client application layout.
#     """
#     return FileResponse("app/templates/index.html")

# @app.post("/predict")
# async def process_valuation_prediction(payload: DiamondInputModel):
#     """
#     Exposes an automated REST API endpoint that ingests client configurations, 
#     maps values to structural frames, and returns a raw prediction response.
#     """
#     try:
#         logging.info("Incoming transaction initialization request hit via web client app.")
        
#         # Instantiate pipeline structures
#         data_packet = CustomData(
#             carat=payload.carat,
#             cut=payload.cut,
#             color=payload.color,
#             clarity=payload.clarity,
#             depth=payload.depth,
#             table=payload.table,
#             x=payload.x,
#             y=payload.y,
#             z=payload.z
#         )
        
#         features_df = data_packet.get_data_as_data_frame()
        
#         pipeline = PredictionPipeline()
#         predicted_value = pipeline.predict(features_df)
        
#         logging.info(f"Transaction prediction request processed successfully. Result: ${predicted_value:.2f}")
#         return {"estimated_price": predicted_value}
        
#     except Exception as e:
#         logging.error(f"Failed to process live prediction call target object matrix: {str(e)}")
#         return {"error": "Internal pipeline transaction exception occurred."}

import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.pipeline.prediction_pipeline import PredictionPipeline, CustomData
from src.utils.logger import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.pipeline.prediction_pipeline import PredictionPipeline, CustomData
from src.utils.logger import logging

app = FastAPI(title="AuraCarat AI Serving API Architecture")

# Mount directory references to access style.css safely
app.mount("/templates", StaticFiles(directory="app/templates"), name="templates")

# Form input parsing data model contract schema with strict non-negative validations
class DiamondInputModel(BaseModel):
    # gt=0 ensures incoming fields are strictly greater than zero mathematically
    carat: float = Field(default=0.7, gt=0, le=5.0)
    cut: str
    color: str
    clarity: str
    depth: float = Field(default=61.5, gt=0, le=100.0)
    table: float = Field(default=57.0, gt=0, le=100.0)
    x: float = Field(default=5.7, gt=0)
    y: float = Field(default=5.7, gt=0)
    z: float = Field(default=3.5, gt=0)

@app.get("/", response_class=HTMLResponse)
async def serve_home_page():
    """
    Renders the custom HTML dashboard client application layout.
    """
    return FileResponse("app/templates/index.html")

@app.post("/predict")
async def process_valuation_prediction(payload: DiamondInputModel):
    """
    Exposes an automated REST API endpoint that ingests client configurations, 
    maps values to structural frames, and returns a raw prediction response.
    """
    try:
        logging.info("Incoming transaction initialization request hit via web client app.")
        
        # Instantiate pipeline structures with validated payload numbers
        data_packet = CustomData(
            carat=payload.carat,
            cut=payload.cut,
            color=payload.color,
            clarity=payload.clarity,
            depth=payload.depth,
            table=payload.table,
            x=payload.x,
            y=payload.y,
            z=payload.z
        )
        
        # Convert custom data model to DataFrame format
        features_df = data_packet.get_data_as_data_frame()
        
        # Run inference using the validated prediction engine
        pipeline = PredictionPipeline()
        predicted_value = pipeline.predict(features_df)
        
        logging.info(f"Transaction prediction request processed successfully. Result: ${predicted_value:.2f}")
        return {"estimated_price": predicted_value}
        
    except Exception as e:
        logging.error(f"Failed to process live prediction call target object matrix: {str(e)}")
        return {"error": "Internal pipeline transaction exception occurred."}