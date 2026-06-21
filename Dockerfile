# Use an official lightweight Python runtime
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /workspace

# Copy the requirements file first to leverage Docker's caching layers
COPY requirements.txt .

# Install dependencies and the local package structure
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Run the training pipeline once to ensure artifacts exist upon startup
RUN python -m src.pipeline.training_pipeline

# Expose the API serving port
EXPOSE 8080

# Command to boot up the FastAPI production server
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8080"]