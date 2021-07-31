from app import db


teacher_goals_table = db.Table('teacher_goals',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
    db.Column('goal_id', db.Integer, db.ForeignKey('goals.id'))
)

class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    name = db.Column(db.String(100), nullable=False)
    about = db.Column(db.String(2000))
    rating = db.Column(db.Float(1), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    picture = db.Column(db.String(250))
    free = db.Column(db.JSON)
    bookings = db.relationship('Booking', back_populates='clientTeacher')
    goals = db.relationship("Goal", secondary=teacher_goals_table, back_populates="teachers")

    def __repr__(self):
        return '<Teacher {} ({})>'.format(self.name, self.id)


class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    clientName = db.Column(db.String(100))
    clientPhone = db.Column(db.String(15))
    clientWeekday = db.Column(db.String(15))
    clientTime = db.Column(db.Time)
    clientTeacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    clientTeacher = db.relationship('Teacher', back_populates='bookings')

    def __repr__(self):
        return '<Booking {}>'.format(self.id)


class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(15), unique=True, nullable=False)
    name = db.Column(db.String(100))
    requests = db.relationship('Request', back_populates='clientGoal')
    teachers = db.relationship("Teacher", secondary=teacher_goals_table, back_populates="goals")

    def __repr__(self):
        return '<Goal {}: {}, {}>'.format(self.id, self.code, self.name)


class Request(db.Model):
    __tablename__ = "requests"
    id = db.Column(db.Integer, primary_key=True)
    clientName = db.Column(db.String(100))
    clientPhone = db.Column(db.String(15))
    clientHours = db.Column(db.String(15))
    clientGoal_id = db.Column(db.Integer, db.ForeignKey('goals.id'))
    clientGoal = db.relationship('Goal', back_populates='requests')

    def __repr__(self):
        return '<Request {}>'.format(self.id)