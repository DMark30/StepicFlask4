from app import db
from app.models import Goal, Teacher, Booking, Request, teacher_goals_table
import json

with open('data_file.json', encoding="utf-8") as json_read_file:
    data = json.load(json_read_file)
# очищаем от старых записей
db.session.query(teacher_goals_table).delete()
db.session.query(Goal).delete()
db.session.query(Teacher).delete()
db.session.query(Booking).delete()
db.session.query(Request).delete()
db.session.commit()
for key, value in data["goals"].items():
    new_goal = Goal()
    new_goal.code = key
    new_goal.name = value
    db.session.add(new_goal)
db.session.commit()
for teacher in data["teachers"]:
    new_teacher = Teacher()
    new_teacher.code = teacher["id"]
    new_teacher.name = teacher["name"]
    new_teacher.about = teacher["about"]
    json_data = json.dumps(teacher["free"])
    new_teacher.free = json.loads(json_data)
    new_teacher.price = teacher["price"]
    new_teacher.rating = teacher["rating"]
    new_teacher.picture = teacher["picture"]
    db.session.add(new_teacher)
db.session.commit()
for teacher in data["teachers"]:
    for goal in teacher["goals"]:
        target_goal = db.session.query(Goal).filter(Goal.code == goal).first()
        target_teacher = db.session.query(Teacher).filter(Teacher.code == teacher["id"]).first()
        target_teacher.goals.append(target_goal)
db.session.commit()
