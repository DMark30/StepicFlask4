from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectField, RadioField, IntegerField
from wtforms.fields.html5 import TelField
from wtforms.validators import InputRequired, DataRequired
from wtforms.widgets import HiddenInput
from app import db
from app.models import Goal


time_limits = [("hour1_2", "1-2 часа в неделю"),
               ("hour3_5", "3-5 часов в неделю"),
               ("hour5_7", "5-7 часов в неделю"),
               ("hour7_10", "7-10 часов в неделю")]


class BookingForm(FlaskForm):
    clientName = StringField("Вас зовут", [InputRequired(message="Необходимо указать имя")])
    clientPhone = TelField("Ваш телефон", [InputRequired(message="Необходимо указать телефон")])
    clientWeekday = HiddenField()
    clientTime = HiddenField()
    clientTeacher = IntegerField(widget=HiddenInput())


class RequestForm(FlaskForm):
    choices = []
    goals = db.session.query(Goal).all()
    for goal in goals:
        choices.append((goal.code, goal.name))
    clientGoal = RadioField("Какова цель занятий?", choices=choices, default="travel", validators=[DataRequired()])
    clientHours = RadioField("Сколько времени есть?", choices=time_limits, default="hour5_7",
                             validators=[DataRequired()])
    clientName = StringField("Вас зовут", [InputRequired(message="Необходимо указать имя")])
    clientPhone = TelField("Ваш телефон", [InputRequired(message="Необходимо указать телефон")])