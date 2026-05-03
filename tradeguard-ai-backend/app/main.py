from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth_routes, trade_routes, risk_routes, ml_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TradeGuard AI API",
    description="A smart trading journal and risk management backend for forex and crypto traders.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(trade_routes.router)
app.include_router(risk_routes.router)
app.include_router(ml_routes.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to TradeGuard AI Backend",
        "docs": "/docs"
    }