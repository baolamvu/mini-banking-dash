import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import Transaction

DESCRIPTIONS = [
    "Salary deposit",
    "ATM withdrawal",
    "Online transfer",
    "Utility bill payment",
    "Mobile top-up",
    "Investment dividend",
    "Loan repayment",
    "Merchant payment",
    "Peer-to-peer transfer",
    "Cashback reward",
]

ACCOUNTS = [
    "ACC-1001",
    "ACC-1002",
    "ACC-1003",
    "ACC-2001",
    "ACC-2002",
    "ACC-3001",
]


def seed_transactions(db: Session, count: int = 20) -> None:
    if db.query(Transaction).count() > 0:
        return

    now = datetime.utcnow()
    for i in range(count):
        tx_type = random.choice(["credit", "debit", "transfer"])
        amount = round(random.uniform(10, 5000), 2)
        from_acc = random.choice(ACCOUNTS)
        to_acc = random.choice([a for a in ACCOUNTS if a != from_acc])

        db.add(
            Transaction(
                type=tx_type,
                amount=amount,
                description=random.choice(DESCRIPTIONS),
                account_from=from_acc,
                account_to=to_acc,
                status="completed",
                created_at=now - timedelta(hours=random.randint(1, 720)),
            )
        )

    db.commit()


def generate_random_transaction(db: Session) -> Transaction:
    tx_type = random.choice(["credit", "debit", "transfer"])
    amount = round(random.uniform(50, 3000), 2)
    from_acc = random.choice(ACCOUNTS)
    to_acc = random.choice([a for a in ACCOUNTS if a != from_acc])

    transaction = Transaction(
        type=tx_type,
        amount=amount,
        description=random.choice(DESCRIPTIONS),
        account_from=from_acc,
        account_to=to_acc,
        status="completed",
        created_at=datetime.utcnow(),
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
