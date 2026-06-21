import gradio as gr
import pandas as pd
import sys
from src.pipeline.prediction_pipeline import PredictionPipeline, CustomData
from src.utils.logger import logging

def evaluate_diamond(carat, cut, color, clarity, depth, table, x, y, z):
    """
    Interface wrapper passing raw UI input values cleanly into the backend Pipeline.
    """
    try:
        logging.info("Gradio interface prediction transaction initialized.")
        
        # Structure the inputs into our verified CustomData packet schema
        data_packet = CustomData(
            carat=float(carat), 
            cut=cut, 
            color=color, 
            clarity=clarity,
            depth=float(depth), 
            table=float(table), 
            x=float(x), 
            y=float(y), 
            z=float(z)
        )
        
        # Convert packet payload directly to a standard pandas DataFrame frame
        features_df = data_packet.get_data_as_data_frame()
        
        # Instantiate prediction pipeline and infer outcome
        pipeline = PredictionPipeline()
        predicted_value = pipeline.predict(features_df)
        
        logging.info(f"Gradio evaluation processed successfully. Value: ${predicted_value:.2f}")
        return f"  Estimated Market Value : ${predicted_value:,.2f}"
        
    except Exception as e:
        logging.error(f"Gradio prediction execution exception encountered: {str(e)}")
        return f"❌ Evaluation Error: {str(e)}"

# Setup premium UI styling layout blocks with strict non-negative input constraints
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("#  AuraCarat AI — Precision Valuator  ")
    gr.Markdown("Provide the diamond's physical traits below for an automated valuation mapping inference.")
    
    with gr.Row():
        with gr.Column():
            # Corrected parameter names to use 'maximum' instead of 'max'
            carat = gr.Number(value=0.7, label="Carat Weight", minimum=0.2, maximum=5.0)
            cut = gr.Dropdown(choices=["Ideal", "Premium", "Very Good", "Good", "Fair"], value="Ideal", label="Cut Quality")
            color = gr.Dropdown(choices=["G", "E", "F", "H", "D", "I", "J"], value="G", label="Color Grade")
            clarity = gr.Dropdown(choices=["SI1", "VS2", "SI2", "VS1", "VVS2", "VVS1", "IF", "I1"], value="SI1", label="Clarity")
        
        with gr.Column():
            # Set minimum logical thresholds to prevent negative dimensions or un-physical zeros
            depth = gr.Number(value=61.5, label="Total Depth %", minimum=43.0, maximum=79.0)
            table = gr.Number(value=57.0, label="Table Width %", minimum=43.0, maximum=95.0)
            x = gr.Number(value=5.7, label="Length (x) mm", minimum=0.1)
            y = gr.Number(value=5.7, label="Width (y) mm", minimum=0.1)
            z = gr.Number(value=3.5, label="Depth (z) mm", minimum=0.1)
            
    submit_btn = gr.Button("Run AI Price Prediction", variant="primary")
    output_text = gr.Textbox(label="Market Value Assessment", interactive=False)
    
    # Mapping interactive trigger bindings
    submit_btn.click(
        fn=evaluate_diamond,
        inputs=[carat, cut, color, clarity, depth, table, x, y, z],
        outputs=output_text
    )

if __name__ == "__main__":
    # Standardized local loopback configurations for reliable local serving operations
    demo.launch(server_name="127.0.0.1", server_port=8081, share=False)