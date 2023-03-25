from .database import db 

class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(50), unique = True, nullable = False)
  
class Temp(db.Model):
    __tablename__ = 'Temperature'
    temp_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    temp_time = db.Column(db.DateTime, nullable = False)
    temp_value = db.Column(db.Float)
    temp_note = db.Column(db.String)
    
class Moods(db.Model):
    __tablename__ = 'Mood'
    mood_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    mood_time = db.Column(db.DateTime, nullable = False)
    mood_choice = db.Column(db.String)
    mood_value = db.Column(db.Integer)
    mood_note = db.Column(db.String)

class Run(db.Model):
    __tablename__ = 'Running'
    run_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    run_time = db.Column(db.DateTime, nullable = False)
    run_value = db.Column(db.Integer)
    run_note = db.Column(db.String)

class SpO2(db.Model):
    __tablename__ = 'Sp02'
    s_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    s_time = db.Column(db.DateTime, nullable = False)
    s_value = db.Column(db.Integer)
    s_note = db.Column(db.String)

class Calorie(db.Model):
    __tablename__ = 'Calorie'
    cal_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    cal_time = db.Column(db.DateTime, nullable = False)
    cal_value = db.Column(db.Integer)
    cal_note = db.Column(db.String)

# class User(db.Model):
#     __tablename__ = 'Users'
#     user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
#     username = db.Column(db.String(20), unique = True, nullable = False)
#     emailid = db.Column(db.String(50), unique = True, nullable = False)
#     trackers = db.relationship("Track", secondary="Tracker", backref = "Users")
    
# class Track(db.Model):
#     __tablename__ = 'Tracker'
#     track_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
#     track_name = db.Column(db.String)
#     track_value = db.Column(db.Integer)
#     track_note = db.Column(db.String)
#     user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=False)
#     logs = db.relationship("Logs", secondary="logs", backref = "Tracker")

# class Logs(db.Model):
#     __tablename__ = 'logs'
#     log_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     tracker_id = db.Column(db.Integer, db.ForeignKey("Tracker.track_id"), nullable=False)
#     timestamp = db.Column(db.DateTime, nullable=False)
#     log_value = db.Column(db.Integer)
#     log_note = db.Column(db.String)