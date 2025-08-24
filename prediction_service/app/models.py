import joblib
from pathlib import Path
import numpy as np
from app.config import logger


class ModelService:
    def __init__(self, models_dir: Path):
        self.model_path = models_dir / "saved_models/linear_regression_model.joblib"
        logger.info(f"Loading model from {self.model_path}")
        self.model = joblib.load(self.model_path)

    def predict(self, features: list[float]) -> float:
        """Prosta predykcja dla jednego wektora cech"""
        X = np.array(features).reshape(1, -1)
        prediction = self.model.predict(X)[0]
        logger.debug(f"Prediction result: {prediction}")
        return float(prediction)