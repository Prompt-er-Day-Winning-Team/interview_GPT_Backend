from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship, backref

from app.repository.model import Base
from app.repository.model.interview import Interview


class User(Base):
    __tablename__ = "user"

    user_id: int = Column(Integer, primary_key=True)
    id: str = Column(String(100, collation="utf8_unicode_ci"), nullable=False)
    password: str = Column(String(255, collation="utf8_unicode_ci"), nullable=False)
    created_at: DateTime = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at: DateTime = Column(DateTime, nullable=False)

    # interview: Interview = relationship('interview', lazy='subquery')

    def __repr__(self):
        return f"User-{self.user_id}-{self.id}"
