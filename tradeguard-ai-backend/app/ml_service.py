import os
import joblib
import pandas as pd
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent.parent
print(ROOT_DIR)
MODEL_PATH = ROOT_DIR / "saved_models" / "trade_risk_model.pkl"



class TradeRiskPredictor:
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "ML model not found. Please run: python ml/train_risk_model.py"
            )

        self.model = joblib.load(MODEL_PATH)

    def predict(self, input_data: dict):
        df = pd.DataFrame([input_data])

        prediction = self.model.predict(df)[0]

        probabilities = self.model.predict_proba(df)[0]
        confidence = round(float(max(probabilities)) * 100, 2)

        explanation = self.generate_explanation(input_data, prediction)

        return {
            "risk_label": prediction,
            "confidence": confidence,
            "explanation": explanation
        }

    def generate_explanation(self, data: dict, prediction: str):
        reasons = []

        if data["risk_reward"] < 1:
            reasons.append("risk-reward ratio is below 1")

        elif data["risk_reward"] < 1.5:
            reasons.append("risk-reward ratio is not very strong")

        if data["lot_size"] > 1:
            reasons.append("lot size is high")

        if data["recent_loss_streak"] >= 3:
            reasons.append("recent loss streak is high")

        if data["stop_loss_pips"] > 100:
            reasons.append("stop loss is wide")

        if data["symbol"].upper() in ["BTCUSDT", "XAUUSD"]:
            reasons.append("the selected instrument is usually more volatile")

        if not reasons:
            reasons.append("your trade setup looks balanced")

        return f"The model classified this trade as {prediction} because " + ", ".join(reasons) + "."