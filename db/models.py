from datetime import datetime

from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Question(Base):
    __tablename__ = "question"
    id = Column(BigInteger, primary_key=True, index=True)
    question_text = Column(String)
    answer_text = Column(String)
    created_at = Column(DateTime)

    def __str__(self):
        return f"<Question {self.id}>"
