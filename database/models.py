from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine

engine = create_engine("sqlite:///database/sqlalchemy.sqlite", echo=True)
Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    userAnswers = relationship("UserAnswers")


class UserAnswers(Base):
    __tablename__ = "userAnswers"
    user_answer_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    question_id = Column(Integer, ForeignKey('questions.question_id'))
    date_of_answer = Column(DateTime)


class Questions(Base):
    __tablename__ = "questions"
    question_id = Column(Integer, primary_key=True)
    question_text = Column(String)
    question_answer = Column(String)
    question_category = Column(Integer, ForeignKey('questionCategory.question_category_id'))
    userAnswers = relationship("UserAnswers")


class QuestionCategory(Base):
    __tablename__ = "questionCategory"
    question_category_id = Column(Integer, primary_key=True)
    question_category_name = Column(String)
    questions = relationship("Questions")
