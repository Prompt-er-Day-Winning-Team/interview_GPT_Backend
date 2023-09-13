from datetime import datetime

from sqlalchemy import Column, Text, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.repository.model import Base
from app.repository.model.interview_result import InterviewResult


class Interview(Base):
    __tablename__ = "interview"

    interview_id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    product_name: str = Column(String(100, collation="utf8_unicode_ci"), nullable=False)
    product_detail: str = Column(Text(collation="utf8_unicode_ci"))
    interview_goal: str = Column(Text(collation="utf8_unicode_ci"))
    target_user: str = Column(Text(collation="utf8_unicode_ci"))
    status: int = Column(Integer, nullable=False)
    question_list: str = Column(Text(collation="utf8_unicode_ci"))
    persona: str = Column(Text(collation="utf8_unicode_ci"))
    virtual_interview: str = Column(Text(collation="utf8_unicode_ci"))
    total_interview_summary: str = Column(Text(collation="utf8_unicode_ci"))
    total_interview_insight: str = Column(Text(collation="utf8_unicode_ci"))
    word_cloud: str = Column(Text(collation="utf8_unicode_ci"))
    created_at: DateTime = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at: DateTime = Column(DateTime, default=datetime.now())

    # interview_result: InterviewResult = relationship('InterviewResult', lazy='subquery')

    def __repr__(self):
        return (
            f"Interview-{self.interview_id}-{self.product_name}-{self.interview_goal}"
        )
