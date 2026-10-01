from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.domain_models import Train


def format_train_to_schema(train: Train) -> dict:
    return {
        "id": train.id,
        "number": train.number,
        "name": train.name,
        "line": train.line,
        "currentBlockSection": train.current_block_section,
        "positionX": train.position_x,
        "speedKmh": train.speed_kmh,
        "direction": train.direction,
        "status": train.status,
    }


def get_all_trains(db: Session) -> List[dict]:
    trains = db.query(Train).all()
    return [format_train_to_schema(t) for t in trains]


def get_train_by_id(db: Session, train_id: str) -> Optional[dict]:
    train = db.query(Train).filter(Train.id == train_id).first()
    if not train:
        return None
    return format_train_to_schema(train)
