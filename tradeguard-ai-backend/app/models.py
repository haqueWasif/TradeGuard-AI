from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    trades = relationship("Trade", back_populates="owner")


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String(50), nullable=False)
    trade_type = Column(String(10), nullable=False)  # buy or sell

    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=False)
    lot_size = Column(Float, nullable=False)

    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)

    profit_loss = Column(Float, nullable=False)
    risk_reward = Column(Float, nullable=True)

    emotion = Column(String(100), nullable=True)
    mistake = Column(String(255), nullable=True)
    lesson = Column(String(255), nullable=True)

    trade_date = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="trades")