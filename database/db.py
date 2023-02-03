from sqlalchemy import exists, update
from sqlalchemy.orm import sessionmaker
from database.models import Users, UserAnswers, Questions, QuestionCategory, Base, engine
from datetime import datetime


def create_database():
    Base.metadata.create_all(engine)


def register(username, password):
    engine_session = sessionmaker(bind=engine)
    session = engine_session()
    user_exists = session.query(exists().where(Users.username == username)).scalar()
    if not user_exists:
        new_user = Users(username=username, password=password)
        session.add(new_user)
        session.commit()
        user = session.query(Users).filter_by(username=username).first()
        questions_for_new_user(user.user_id)
        return True
    else:
        return False


def login(username, password):
    engine_session = sessionmaker(bind=engine)
    session = engine_session()
    user = session.query(Users).filter_by(username=username, password=password).first()
    return bool(user)


def question_category():
    engine_session = sessionmaker(bind=engine)
    session = engine_session()
    categories = session.query(QuestionCategory.question_category_name)
    return [category.question_category_name for category in categories]


def get_questions(user_id, question_category_id):
    engine_session = sessionmaker(bind=engine)
    session = engine_session()
    current_time = datetime.now()

    questions = session.query(Questions). \
        join(UserAnswers). \
        filter(UserAnswers.user_id == user_id,
               UserAnswers.date_of_answer < current_time,
               Questions.question_category == question_category_id). \
        all()
    question_data = [(question.question_id ,question.question_text, question.question_answer) for question in questions]
    return question_data


def questions_for_new_user(user_id):
    engine_session = sessionmaker(bind=engine)
    session = engine_session()
    questions_list = session.query(Questions).all()
    for question in questions_list:
        new_question = UserAnswers(user_id=user_id, question_id=question.question_id, date_of_answer=datetime.now())
        session.add(new_question)
    session.commit()


def get_user_id(username):
    engine_session = sessionmaker(bind=engine)
    session = engine_session()
    user = session.query(Users).filter_by(username=username).first()
    return user.user_id


def update_user_answer(user_id, question_id, date):
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    engine_session = sessionmaker(bind=engine)
    session = engine_session()
    query = session.query(UserAnswers).filter_by(user_id=user_id, question_id=question_id)
    query.update({UserAnswers.date_of_answer: date})
    session.commit()