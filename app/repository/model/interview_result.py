from datetime import datetime

from sqlalchemy import Column, Text, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.repository.model import Base

class InterviewResult(Base):
    __tablename__ = "interview_result"

    interview_result_id: int = Column(Integer, primary_key=True)
    interview_id: int = Column(Integer, ForeignKey('interview.interview_id'), nullable=False)
    name: str = Column(String(100, collation="utf8_unicode_ci"), nullable=False)
    interview_url: str = Column(Text(collation="utf8_unicode_ci"))
    interview_contents: str = Column(Text(collation="utf8_unicode_ci"))
    interview_summary: str = Column(Text(collation="utf8_unicode_ci"))
    interview_insight: str = Column(Text(collation="utf8_unicode_ci"))
    created_at: DateTime = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at: DateTime = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f"Interview-Result-{self.interview_result_id}-{self.name}"
