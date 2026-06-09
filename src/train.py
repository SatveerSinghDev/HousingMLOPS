import os
import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression


def train_model():
    # 1. Load data
    data_path = os.path.join("data", "housing_data.csv")
    df = pd.read_csv(data_path)

    # 2. Split features and target
    X = df[["sqft", "bedrooms"]]
    y = df["price"]

    # 3. Train Model
    model = LinearRegression()
    model.fit(X, y)

    # 4. Save the model artifact
    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print(f"✅ Model successfully trained and saved to {model_path}")


if __name__ == "__main__":
    train_model()
