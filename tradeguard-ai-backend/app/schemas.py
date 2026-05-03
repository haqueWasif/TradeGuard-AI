from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., max_length=72)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TradeCreate(BaseModel):
    symbol: str
    trade_type: str
    entry_price: float
    exit_price: float
    lot_size: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    profit_loss: float
    risk_reward: Optional[float] = None
    emotion: Optional[str] = None
    mistake: Optional[str] = None
    lesson: Optional[str] = None


class TradeResponse(BaseModel):
    id: int
    symbol: str
    trade_type: str
    entry_price: float
    exit_price: float
    lot_size: float
    stop_loss: Optional[float]
    take_profit: Optional[float]
    profit_loss: float
    risk_reward: Optional[float]
    emotion: Optional[str]
    mistake: Optional[str]
    lesson: Optional[str]
    trade_date: datetime

    class Config:
        from_attributes = True


class RiskCalculatorInput(BaseModel):
    account_balance: float
    risk_percent: float
    stop_loss_pips: float
    pip_value: float = 10.0


class RiskCalculatorOutput(BaseModel):
    risk_amount: float
    recommended_lot_size: float
    warning: str
    
class TradeRiskPredictionInput(BaseModel):
    symbol: str
    trade_type: str
    session: str
    risk_reward: float
    stop_loss_pips: float
    lot_size: float
    recent_loss_streak: int


class TradeRiskPredictionOutput(BaseModel):
    risk_label: str
    confidence: float
    explanation: str