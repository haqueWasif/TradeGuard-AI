import pandas as pd

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Trade, User
from app.schemas import TradeCreate, TradeResponse
from app.auth import get_current_user
from app.analytics import TradeAnalyzer

router = APIRouter(prefix="/trades", tags=["Trades"])


@router.post("/", response_model=TradeResponse)
def create_trade(
    trade_data: TradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_trade = Trade(
        symbol=trade_data.symbol.upper(),
        trade_type=trade_data.trade_type.lower(),
        entry_price=trade_data.entry_price,
        exit_price=trade_data.exit_price,
        lot_size=trade_data.lot_size,
        stop_loss=trade_data.stop_loss,
        take_profit=trade_data.take_profit,
        profit_loss=trade_data.profit_loss,
        risk_reward=trade_data.risk_reward,
        emotion=trade_data.emotion,
        mistake=trade_data.mistake,
        lesson=trade_data.lesson,
        user_id=current_user.id
    )

    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)

    return new_trade


@router.get("/", response_model=list[TradeResponse])
def get_my_trades(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trades = db.query(Trade).filter(Trade.user_id == current_user.id).all()
    return trades


@router.post("/upload-csv")
def upload_trade_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    try:
        df = pd.read_csv(file.file)

        required_columns = [
            "symbol",
            "trade_type",
            "entry_price",
            "exit_price",
            "lot_size",
            "profit_loss"
        ]

        for column in required_columns:
            if column not in df.columns:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required column: {column}"
                )

        inserted_count = 0

        for _, row in df.iterrows():
            trade = Trade(
                symbol=str(row["symbol"]).upper(),
                trade_type=str(row["trade_type"]).lower(),
                entry_price=float(row["entry_price"]),
                exit_price=float(row["exit_price"]),
                lot_size=float(row["lot_size"]),
                stop_loss=float(row["stop_loss"]) if "stop_loss" in df.columns and pd.notna(row["stop_loss"]) else None,
                take_profit=float(row["take_profit"]) if "take_profit" in df.columns and pd.notna(row["take_profit"]) else None,
                profit_loss=float(row["profit_loss"]),
                risk_reward=float(row["risk_reward"]) if "risk_reward" in df.columns and pd.notna(row["risk_reward"]) else None,
                emotion=str(row["emotion"]) if "emotion" in df.columns and pd.notna(row["emotion"]) else None,
                mistake=str(row["mistake"]) if "mistake" in df.columns and pd.notna(row["mistake"]) else None,
                lesson=str(row["lesson"]) if "lesson" in df.columns and pd.notna(row["lesson"]) else None,
                user_id=current_user.id
            )

            db.add(trade)
            inserted_count += 1

        db.commit()

        return {
            "message": "CSV uploaded successfully",
            "inserted_trades": inserted_count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/summary")
def get_trade_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trades = db.query(Trade).filter(Trade.user_id == current_user.id).all()

    analyzer = TradeAnalyzer(trades)

    return {
        "total_trades": analyzer.total_trades(),
        "total_profit_loss": analyzer.total_profit_loss(),
        "win_rate": analyzer.win_rate(),
        "loss_rate": analyzer.loss_rate(),
        "average_profit": analyzer.average_profit(),
        "average_loss": analyzer.average_loss(),
        "risk_score": analyzer.risk_score(),
        "ai_feedback": analyzer.ai_feedback()
    }


@router.get("/analytics/by-symbol")
def get_symbol_performance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trades = db.query(Trade).filter(Trade.user_id == current_user.id).all()

    symbol_data = {}

    for trade in trades:
        if trade.symbol not in symbol_data:
            symbol_data[trade.symbol] = {
                "total_trades": 0,
                "total_profit_loss": 0,
                "wins": 0,
                "losses": 0
            }

        symbol_data[trade.symbol]["total_trades"] += 1
        symbol_data[trade.symbol]["total_profit_loss"] += trade.profit_loss

        if trade.profit_loss > 0:
            symbol_data[trade.symbol]["wins"] += 1
        elif trade.profit_loss < 0:
            symbol_data[trade.symbol]["losses"] += 1

    return symbol_data