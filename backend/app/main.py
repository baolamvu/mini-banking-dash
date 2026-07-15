import os
import socket
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine, get_db
from app.models import Transaction
from app.schemas import StatsResponse, TransactionCreate, TransactionResponse
from app.seed import generate_random_transaction, seed_transactions

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_THEME = os.getenv("APP_THEME", "blue")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_transactions(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Mini Banking API",
    description="Demo API for OpenShift",
    version=APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "version": APP_VERSION, "hostname": socket.gethostname()}


@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ready", "database": "connected"}

#general data
@app.get("/metrics")
def metrics(db: Session = Depends(get_db)):
    count = db.query(Transaction).count()
    return {
        "app_transactions_total": count,
        "app_version_info": APP_VERSION,
        "app_theme": APP_THEME,
    }


@app.get("/api/config")
def config():
    return {"version": APP_VERSION, "theme": APP_THEME}


@app.get("/api/transactions", response_model=list[TransactionResponse])
def list_transactions(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return (
        db.query(Transaction)
        .order_by(Transaction.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@app.post("/api/transactions", response_model=TransactionResponse, status_code=201)
def create_transaction(
    payload: TransactionCreate | None = None,
    db: Session = Depends(get_db),
):
    if payload is None:
        return generate_random_transaction(db)

    transaction = Transaction(
        type=payload.type,
        amount=payload.amount,
        description=payload.description,
        account_from=payload.account_from,
        account_to=payload.account_to,
        status="completed",
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@app.post("/api/transactions/generate", response_model=TransactionResponse, status_code=201)
def generate_transaction(db: Session = Depends(get_db)):
    return generate_random_transaction(db)


@app.get("/api/stats", response_model=StatsResponse)
def stats(db: Session = Depends(get_db)):
    total = db.query(Transaction).count()
    credit = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(Transaction.type == "credit")
        .scalar()
    )
    debit = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(Transaction.type.in_(["debit", "transfer"]))
        .scalar()
    )
    return StatsResponse(
        total_transactions=total,
        total_credit=float(credit),
        total_debit=float(debit),
        net_balance=float(credit) - float(debit),
    )
