import os
import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Housing Price Prediction API", version="1.0")

# Define the expected JSON input structure from the user
class HouseFeatures(BaseModel):
    sqft: float
    bedrooms: int

model_path = os.path.join("models", "model.pkl")
model = None

@app.on_event("startup")
def load_model():
    """Load the trained model artifact when the web server starts."""
    global model
    if not os.path.exists(model_path):
        raise RuntimeError(f"Model file not found at {model_path}. Please run training first.")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    print("✅ Machine Learning model loaded into memory successfully!")

@app.get("/")
def home():
    return {"message": "Housing Price API is up and running!"}

@app.post("/predict")
def predict_price(features: HouseFeatures):
    """Accept house details via POST request and return the price prediction."""
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
    
    try:
        # Format the user's input into a DataFrame matching the training data structure
        input_data = pd.DataFrame([[features.sqft, features.bedrooms]], columns=["sqft", "bedrooms"])
        
        # Run prediction
        prediction = model.predict(input_data)[0]
        
        return {
            "input_received": features.dict(),
            "estimated_price": round(float(prediction), 2)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
