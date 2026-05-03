import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


np.random.seed(42)


def create_training_data(rows=1000):
    symbols = ["EURUSD", "GBPUSD", "XAUUSD", "BTCUSDT", "USDJPY"]
    trade_types = ["buy", "sell"]
    sessions = ["Asian", "London", "New York"]

    data = []

    for _ in range(rows):
        symbol = np.random.choice(symbols)
        trade_type = np.random.choice(trade_types)
        session = np.random.choice(sessions)

        risk_reward = round(np.random.uniform(0.5, 4.0), 2)
        stop_loss_pips = round(np.random.uniform(10, 150), 2)
        lot_size = round(np.random.uniform(0.01, 2.0), 2)
        recent_loss_streak = np.random.randint(0, 6)

        risk_score = 0

        if risk_reward < 1:
            risk_score += 2
        elif risk_reward < 1.5:
            risk_score += 1

        if lot_size > 1:
            risk_score += 2
        elif lot_size > 0.5:
            risk_score += 1

        if stop_loss_pips > 100:
            risk_score += 1

        if recent_loss_streak >= 3:
            risk_score += 2
        elif recent_loss_streak >= 2:
            risk_score += 1

        if symbol in ["BTCUSDT", "XAUUSD"]:
            risk_score += 1

        if risk_score <= 2:
            risk_label = "Low Risk"
        elif risk_score <= 4:
            risk_label = "Medium Risk"
        else:
            risk_label = "High Risk"

        data.append({
            "symbol": symbol,
            "trade_type": trade_type,
            "session": session,
            "risk_reward": risk_reward,
            "stop_loss_pips": stop_loss_pips,
            "lot_size": lot_size,
            "recent_loss_streak": recent_loss_streak,
            "risk_label": risk_label
        })

    return pd.DataFrame(data)


def train_model():
    df = create_training_data()

    X = df.drop("risk_label", axis=1)
    y = df["risk_label"]

    categorical_features = ["symbol", "trade_type", "session"]
    numerical_features = [
        "risk_reward",
        "stop_loss_pips",
        "lot_size",
        "recent_loss_streak"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", StandardScaler(), numerical_features)
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(
                n_estimators=100,
                random_state=42
            ))
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("Model training completed.")
    print(f"Accuracy: {round(accuracy * 100, 2)}%")
    print()
    print(classification_report(y_test, predictions))

    os.makedirs("saved_models", exist_ok=True)

    joblib.dump(model, "saved_models/trade_risk_model.pkl")

    print("Model saved at: saved_models/trade_risk_model.pkl")


if __name__ == "__main__":
    train_model()