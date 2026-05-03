from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_user
from app.models import User
from app.schemas import TradeRiskPredictionInput, TradeRiskPredictionOutput
from app.ml_service import TradeRiskPredictor


router = APIRouter(prefix="/ml", tags=["Machine Learning"])


@router.post("/predict-risk", response_model=TradeRiskPredictionOutput)
def predict_trade_risk(
    trade_data: TradeRiskPredictionInput,
    current_user: User = Depends(get_current_user)
):
    try:
        predictor = TradeRiskPredictor()

        prediction = predictor.predict({
            "symbol": trade_data.symbol.upper(),
            "trade_type": trade_data.trade_type.lower(),
            "session": trade_data.session,
            "risk_reward": trade_data.risk_reward,
            "stop_loss_pips": trade_data.stop_loss_pips,
            "lot_size": trade_data.lot_size,
            "recent_loss_streak": trade_data.recent_loss_streak
        })

        return prediction

    except FileNotFoundError as error:
        raise HTTPException(status_code=500, detail=str(error))

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(error)}")