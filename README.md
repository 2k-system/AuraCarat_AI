# 💎 AuraCarat AI — Industrial Diamond Pricing Engine

AuraCarat AI is a production-grade, end-to-end MLOps regression pipeline designed to predict the market valuation of diamonds based on their physical characteristics. It features a complete pipeline lifecycle wrapper—from automated ingestion and schema validation firewalls to modular ensemble training and a clean web-serving user interface.

---

## 🏗️ System Architecture & Framework
This project follows strict clean-code architecture dividing utilities, core pipeline orchestration components, and the API serving framework:

* **Data Ingestion Layer:** Pulls pristine raw record sets and distributes clean stratifications.
* **Data Validation Firewall:** Dynamically reads and evaluates strict type constraints against `configs/config.yaml`.
* **Feature Engineering Engine:** Injects domain-specific indicators like *Diamond Volume* and *Symmetry Ratio*.
* **Data Transformation Pipeline:** Imutes missing fields and applies standard scaled / One-Hot configurations.
* **Model Trainer & Pusher Gate:** Executes tuned Random Forest Ensemble routines and pushes validated files to application paths if metrics crack standard thresholds.

---

## ⚡ Quick Start Guide

### 1. Environment Setup
Clone this repository and establish your package dependencies inside a clean virtual workspace:
```bash
# Install the environment requirements and setup module package
pip install -r requirements.txt

2. Execute the Machine Learning Pipeline
Trigger the automated master conductor script to pull data, validate, transform, train, and deploy models with one command:

Bash
python -m src.pipeline.training_pipeline

3. Launch the Application Interface
Boot the FastAPI application backend locally to view the semi-transparent web dashboard layout:

Bash
uvicorn app.api:app --reload --port 8080
Open your browser and navigate to: http://127.0.0.1:8080

