import os
import pickle
import pandas as pd


def test_data_quality():
    """Ensure the training data exists and is not empty."""
    data_path = os.path.join("data", "housing_data.csv")
    assert os.path.exists(data_path), "Data file missing!"

    df = pd.read_csv(data_path)
    assert not df.empty, "Data file is empty!"
    assert "price" in df.columns, "Target column 'price' is missing!"
    assert df.isnull().sum().sum() == 0, "Data contains missing NaN values!"


def test_model_prediction():
    """Ensure the model can load and output a positive price prediction."""
    model_path = os.path.join("models", "model.pkl")
    assert os.path.exists(model_path), "Model artifact file missing!"

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Mock house: 1800 sqft, 3 bedrooms
    mock_house = pd.DataFrame([[1800, 3]], columns=["sqft", "bedrooms"])
    prediction = model.predict(mock_house)[0]

    assert prediction > 0, "Model predicted a negative or zero price!"
