from fastapi import APIRouter

from app.schemas import RiskCalculatorInput, RiskCalculatorOutput

router = APIRouter(prefix="/risk", tags=["Risk Calculator"])


class RiskManager:
    def calculate_position_size(
        self,
        account_balance: float,
        risk_percent: float,
        stop_loss_pips: float,
        pip_value: float
    ):
        risk_amount = account_balance * (risk_percent / 100)
        recommended_lot_size = risk_amount / (stop_loss_pips * pip_value)

        return round(risk_amount, 2), round(recommended_lot_size, 2)

    def risk_warning(self, risk_percent: float):
        if risk_percent <= 1:
            return "Conservative risk. Good for long-term survival."

        if risk_percent <= 2:
            return "Moderate risk. Acceptable for experienced traders."

        return "High risk. You may lose capital quickly if you face a losing streak."


@router.post("/position-size", response_model=RiskCalculatorOutput)
def calculate_position_size(data: RiskCalculatorInput):
    risk_manager = RiskManager()

    risk_amount, lot_size = risk_manager.calculate_position_size(
        account_balance=data.account_balance,
        risk_percent=data.risk_percent,
        stop_loss_pips=data.stop_loss_pips,
        pip_value=data.pip_value
    )

    return {
        "risk_amount": risk_amount,
        "recommended_lot_size": lot_size,
        "warning": risk_manager.risk_warning(data.risk_percent)
    }