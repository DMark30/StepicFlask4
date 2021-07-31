import json
from flask import render_template, request
from app import app, forms, db
from app.models import Teacher, Goal, Request, Booking
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import lazyload


week_days = {"mon": ["monday", "Понедельник"], "tue": ["tuesday", "Вторник"], "wed": ["wednesday", "Среда"],
             "thu": ["thursday", "Четверг"], "fri": ["friday", "Пятница"]}

goals = {}
goals_db = db.session.query(Goal).all()
for goal in goals_db:
    goals[goal.code] = goal.name


@app.route("/")
def index_page():
    #teachers_show = random.sample(data["teachers"], k=6)
    teachers_show = db.session.query(Teacher).order_by(func.random()).limit(6)

    return render_template("index.html", teachers=teachers_show, goals=goals)


@app.route("/all/", methods=["GET", "POST"])
def all_page():
    sort_value = ""
    if request.method == 'POST':
        sort_value = request.form.get("inlineFormCustomSelectPref")
    if sort_value == "1":
        teachers = db.session.query(Teacher).order_by(Teacher.price.desc()).all()
    elif sort_value == "2":
        teachers = db.session.query(Teacher).order_by(Teacher.price).all()
    elif sort_value == "3":
        teachers = db.session.query(Teacher).order_by(Teacher.rating.desc()).all()
    else:
        teachers = db.session.query(Teacher).order_by(func.random()).all()
    return render_template("all.html", teachers=teachers, sort_value=sort_value)


@app.route("/goals/<goal>/")
def goal_page(goal):
    goal_id = db.session.query(Goal.id).filter(Goal.code == goal).first_or_404()
    teachers_show = db.session.query(Teacher).options(lazyload(Teacher.goals)).filter(Teacher.goals.any(id=goal_id.id)).all()
    return render_template("goal.html", teachers=teachers_show)


@app.route("/profiles/<int:teacher_id>/")
def profile_page(teacher_id):
    teacher = db.session.query(Teacher).options(lazyload(Teacher.goals)).get_or_404(teacher_id)
    #free = json.loads(teacher.free)
    return render_template("profile.html", teacher=teacher, free=teacher.free, week_days=week_days, goals=goals)


@app.route("/request/")
def request_page():
    form = forms.RequestForm()
    return render_template("request.html", form=form)


@app.route("/request_done/", methods=["POST"])
def request_done_page():
    form = forms.RequestForm()
    if form.validate_on_submit():
        new_request = Request()
        new_request.clientName = form.clientName.data
        new_request.clientPhone = form.clientPhone.data
        new_request.clientGoal = db.session.query(Goal).filter(Goal.code == form.clientGoal.data).first()
        new_request.clientHours = form.clientHours.data
        db.session.add(new_request)
        db.session.commit()
        value = form.clientHours.data
        choices = dict(form.clientHours.choices)
        label = choices[value]
        return render_template("request_done.html", request=new_request, hours=label)
    else:
        return render_template("request.html", form=form)


@app.route("/booking/<int:teacher_id>/<day>/<time>/")
def booking_page(teacher_id, day, time):
    form = forms.BookingForm()
    for key, value in week_days.items():
        if value[0] == day:
            form.clientWeekday.data = key
            form.clientTime.label = value[1]
    form.clientTime.data = time + ":00"
    form.clientTime.label = form.clientTime.label + ", " + form.clientTime.data
    form.clientTeacher.data = teacher_id
    teacher = db.session.query(Teacher).get_or_404(teacher_id)
    form.clientTeacher.label = teacher.name
    return render_template("booking.html", form=form, picture=teacher.picture)


@app.route("/booking_done/", methods=["POST"])
def booking_done_page():
    form = forms.BookingForm()
    if form.validate_on_submit():
        new_booking = {"clientName": form.clientName.data, "clientPhone": form.clientPhone.data,
                       "clientWeekday": form.clientWeekday.data, "clientTime": form.clientTime.data,
                       "clientTeacher": form.clientTeacher.data
                       }
        new_booking = Booking()
        new_booking.clientName = form.clientName.data
        new_booking.clientPhone = form.clientPhone.data
        new_booking.clientWeekday = form.clientWeekday.data
        new_booking.clientTime = form.clientTime.data
        new_booking.clientTeacher = db.session.query(Teacher).get_or_404(form.clientTeacher.data)
        db.session.add(new_booking)
        db.session.commit()
        for key, value in week_days.items():
            if key == form.clientWeekday.data:
                day = value[1] + ", " + form.clientTime.data
        return render_template("booking_done.html", booking=new_booking, day=day)
    else:
        return render_template("booking.html", form=form)
