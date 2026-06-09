import os
import pickle
import csv
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Housing Price Prediction API with Monitoring", version="2.0")

# Instrument the app to automatically expose a /metrics endpoint for Prometheus
Instrumentator().instrument(app).expose(app)

class HouseFeatures(BaseModel):
    sqft: float
    bedrooms: int

model_path = os.path.join("models", "model.pkl")
log_path = os.path.join("models", "prediction_log.csv")
model = None

@app.on_event("startup")
def load_model():
    global model
    if not os.path.exists(model_path):
        raise RuntimeError(f"Model file not found at {model_path}.")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    # Initialize the log file with header if it doesn't exist
    if not os.path.exists(log_path):
        os.makedirs("models", exist_ok=True)
        with open(log_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["sqft", "bedrooms"])

@app.post("/predict")
def predict_price(features: HouseFeatures):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    
    try:
        # Log incoming production data for drift analysis
        with open(log_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([features.sqft, features.bedrooms])

        input_data = pd.DataFrame([[features.sqft, features.bedrooms]], columns=["sqft", "bedrooms"])
        prediction = model.predict(input_data)
        
        return {
            "input_received": features.dict(),
            "estimated_price": round(float(prediction), 2)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
