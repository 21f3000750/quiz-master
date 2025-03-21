from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import nulls_last
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32), unique=True, nullable=False)
    passhash = db.Column(db.String(512), nullable=False)
    name = db.Column(db.String(64), nullable=True)
    qualification = db.Column(db.String(64), nullable=True)
    dob = db.Column(db.String(64), nullable=True)
    created_on = db.Column(db.Date)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passhash, password)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.String(255), nullable=True)
    created_on=db.Column(db.Date)
    chapters=db.relationship("Chapter", backref=db.backref('subject', lazy=True))

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    desc = db.Column(db.String(255), nullable=True)
    created_on = db.Column(db.Date)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    chapter_title= db.Column(db.String(255), nullable=True)
    date_of_quiz = db.Column(db.String(255), nullable=True)
    hour_duration = db.Column(db.String(255), nullable=True)
    min_duration = db.Column(db.String(255), nullable=True)
    questions=db.relationship("Question", backref=db.backref('quiz', lazy=True))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    question_title = db.Column(db.String(255), nullable=True)
    question_statement = db.Column(db.String(255), nullable=True)
    option_1 = db.Column(db.String(255), nullable=True)
    option_2 = db.Column(db.String(255), nullable=True)
    option_3 = db.Column(db.String(255), nullable=True)
    option_4 = db.Column(db.String(255), nullable=True)
    correct_option = db.Column(db.String(255), nullable=True)
    remarks = db.Column(db.String(255), nullable=True)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_stamp_of_attempt = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    total_scored = db.Column(db.String(64), nullable=False)