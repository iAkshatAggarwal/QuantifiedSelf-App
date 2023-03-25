import os
from tempfile import tempdir
from flask import Flask, redirect, request, session
from flask import render_template
from flask import current_app as app
from application.config import LocalDevelopmentConfig
from application.database import db 
from application.models import Calorie, SpO2, User, Temp, Run, Moods
from sqlalchemy import and_, desc
import datetime
import json


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("user_login.html")
    elif request.method == "POST": 
        tlastmodified = Temp.query.filter(Temp.temp_time).order_by(desc(Temp.temp_time)).first()
        mlastmodified = Moods.query.filter(Moods.mood_time).order_by(desc(Moods.mood_time)).first()
        rlastmodified = Run.query.filter(Run.run_time).order_by(desc(Run.run_time)).first()
        slastmodified = SpO2.query.filter(SpO2.s_time).order_by(desc(SpO2.s_time)).first()
        clastmodified = Calorie.query.filter(Calorie.cal_time).order_by(desc(Calorie.cal_time)).first()
        #Adding data to "User" table
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter(and_(User.username == username, User.password == password)).first():
            return render_template("dashboard.html", display_name = username, tlm = tlastmodified, mlm = mlastmodified, rlm = rlastmodified, slm = slastmodified, clm = clastmodified)

        else:
            return redirect("/")

@app.route("/logout", methods=["GET", "POST"])
def logout():
        return redirect("/")

#User Registration

@app.route("/register", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST": 
        #Adding data to "User" table
        username = request.form["username"]
        password = request.form["password"]
        rpassword = request.form["rpassword"]

        if User.query.filter(and_(User.username == username, User.password == password)).first():
                return redirect("/")

        elif User.query.filter(and_(User.username != username, User.password != password)).first():
            if(password == rpassword):    
                ud = User(username=username, password=password)

                db.session.add(ud)
                db.session.commit()

                return redirect("/")
            
           
@app.route("/dash", methods=["GET", "POST"])
def dash():
    if request.method == "GET":
        tlastmodified = Temp.query.filter(Temp.temp_time).order_by(desc(Temp.temp_time)).first()
        mlastmodified = Moods.query.filter(Moods.mood_time).order_by(desc(Moods.mood_time)).first()
        rlastmodified = Run.query.filter(Run.run_time).order_by(desc(Run.run_time)).first()
        slastmodified = SpO2.query.filter(SpO2.s_time).order_by(desc(SpO2.s_time)).first()
        clastmodified = Calorie.query.filter(Calorie.cal_time).order_by(desc(Calorie.cal_time)).first()
        return render_template("dashboard.html", tlm = tlastmodified, mlm = mlastmodified, rlm = rlastmodified, slm = slastmodified, clm = clastmodified)


#For Temperature Table

@app.route("/temp_record/", methods=["GET", "POST"])
def tdisp():
    if request.method == "GET":
        #For graph
        over_time_temperature = []
        dates = db.session.query(db.func.sum(Temp.temp_value), Temp.temp_time).group_by(Temp.temp_time).order_by(Temp.temp_time).all()
        dates_label = []
        for amount, date in dates:
            dates_label.append(date.strftime("%m-%d-%y"))
            over_time_temperature.append(amount)

        #For Table
        data = Temp.query.all()
        return render_template("disp_temp.html", s_d = data, over_time_temperature = json.dumps(over_time_temperature), dates_label =json.dumps(dates_label))


@app.route("/add_temp/", methods=["GET", "POST"])
def add_temp():
    if request.method == "GET":
        return render_template("add_temp.html")
    else:
        # get the current datetime and store it in a variable
        currentDateTime = datetime.datetime.now()   

        tvalue = request.form["temp"]
        tnote = request.form["temp_note"]

        t = Temp(temp_time = currentDateTime, temp_value=tvalue, temp_note=tnote)

        db.session.add(t)
        db.session.commit()

        return redirect("/temp_record/")

@app.route("/temp/<int:tid>/delete")
def del_temp(tid):
    data = Temp.query.filter(Temp.temp_id == tid).one()
    db.session.delete(data)
    db.session.commit()
    return redirect('/temp_record')

@app.route("/temp/<int:tid>/update", methods=["GET", "POST"])
def update_temp(tid):
    if request.method == "GET":
        data = Temp.query.filter(Temp.temp_id == tid).first()
        return render_template("update_temp.html", c_d=data)

    else:

        new = Temp.query.filter_by(temp_id=tid).first()

        new.temp_value = request.form["value"]
        new.temp_note = request.form["note"]

        db.session.commit()
        return redirect('/temp_record')
        

#For Run Table

@app.route("/run_record/", methods=["GET", "POST"])
def rdisp():
    if request.method == "GET":
        #For graph
        over_time_run = []
        dates = db.session.query(db.func.sum(Run.run_value), Run.run_time).group_by(Run.run_time).order_by(Run.run_time).all()
        dates_label = []
        for amount, date in dates:
            dates_label.append(date.strftime("%m-%d-%y"))
            over_time_run.append(amount)

        #For Table
        data = Run.query.all()
        return render_template("disp_run.html", s_d  = data, over_time_run = json.dumps(over_time_run), dates_label =json.dumps(dates_label))


@app.route("/add_run/", methods=["GET", "POST"])
def add_run():
    if request.method == "GET":
        return render_template("add_run.html")
    else:
        # get the current datetime and store it in a variable
        currentDateTime = datetime.datetime.now() 

        rvalue = request.form["run"]
        rnote = request.form["run_note"]

        r = Run(run_time = currentDateTime, run_value=rvalue, run_note=rnote)

        db.session.add(r)
        db.session.commit()

        return redirect("/run_record/")

@app.route("/run/<int:tid>/delete")
def del_run(tid):
    data = Run.query.filter(Run.run_id == tid).one()
    db.session.delete(data)
    db.session.commit()
    return redirect("/run_record")


@app.route("/run/<int:tid>/update", methods=["GET", "POST"])
def update_run(tid):
    if request.method == "GET":
        data = Run.query.filter(Run.run_id == tid).first()
        return render_template("update_run.html", s_d=data)

    else:

        new = Run.query.filter_by(run_id=tid).first()

        new.run_value = request.form["value"]
        new.run_note = request.form["note"]

        db.session.commit()
        return redirect('/run_record')


#For Mood Table

@app.route("/mood_record/", methods=["GET", "POST"])
def mdisp():
    if request.method == "GET":
    #For graph
        over_time_mood = []
        dates = db.session.query(db.func.sum(Moods.mood_value), Moods.mood_time).group_by(Moods.mood_time).order_by(Moods.mood_time).all()
        dates_label = []
        for amount, date in dates:
            dates_label.append(date.strftime("%m-%d-%y"))
            over_time_mood.append(amount)
    #For Table
        data = Moods.query.all()
        return render_template("disp_mood.html", s_d  = data, over_time_mood = json.dumps(over_time_mood), dates_label =json.dumps(dates_label))


@app.route("/add_mood/", methods=["GET", "POST"])
def add_mood():
    if request.method == "GET":
        return render_template("add_mood.html")
    else:
        # get the current datetime and store it in a variable
        currentDateTime = datetime.datetime.now() 

        mood = request.form["mood"]
        mvalue = request.form["mood_val"]
        mnote = request.form["mood_note"]

        m = Moods(mood_time = currentDateTime, mood_choice=mood, mood_value=mvalue, mood_note=mnote)

        db.session.add(m)
        db.session.commit()

        return redirect('/mood_record')

@app.route("/mood/<int:tid>/delete")
def del_mood(tid):
    data = Moods.query.filter(Moods.mood_id == tid).one()
    db.session.delete(data)
    db.session.commit()
    return redirect("/mood_record")


@app.route("/mood/<int:tid>/update", methods=["GET", "POST"])
def update_mood(tid):
    if request.method == "GET":
        data = Moods.query.filter(Moods.mood_id == tid).first()
        return render_template("update_mood.html", c_d=data)

    else:

        new = Moods.query.filter_by(mood_id=tid).first()

        new.mood_choice = request.form["choice"]
        new.mood_value = request.form["value"]
        new.mood_note = request.form["note"]

        db.session.commit()
        return redirect('/mood_record')

#For SpO2 table

@app.route("/spo2_record/", methods=["GET", "POST"])
def sdisp():
    if request.method == "GET":
        #For graph
        over_time_spo2 = []
        dates = db.session.query(db.func.sum(SpO2.s_value), SpO2.s_time).group_by(SpO2.s_time).order_by(SpO2.s_time).all()
        dates_label = []
        for amount, date in dates:
            dates_label.append(date.strftime("%m-%d-%y"))
            over_time_spo2.append(amount)

        #For Table
        data = SpO2.query.all()
        return render_template("disp_spo2.html", s_d = data, over_time_spo2 = json.dumps(over_time_spo2), dates_label =json.dumps(dates_label))


@app.route("/add_spo2/", methods=["GET", "POST"])
def add_spo2():
    if request.method == "GET":
        return render_template("add_spo2.html")
    else:
        # get the current datetime and store it in a variable
        currentDateTime = datetime.datetime.now()   

        tvalue = request.form["spo2"]
        tnote = request.form["spo2_note"]

        s = SpO2(s_time = currentDateTime, s_value=tvalue, s_note=tnote)

        db.session.add(s)
        db.session.commit()

        return redirect("/spo2_record/")

@app.route("/spo2/<int:tid>/delete")
def del_spo2(tid):
    data = SpO2.query.filter(SpO2.s_id == tid).one()
    db.session.delete(data)
    db.session.commit()
    return redirect('/spo2_record')

@app.route("/spo2/<int:tid>/update", methods=["GET", "POST"])
def update_spo2(tid):
    if request.method == "GET":
        data = SpO2.query.filter(SpO2.s_id == tid).first()
        return render_template("update_spo2.html", c_d=data)

    else:

        new = SpO2.query.filter_by(s_id=tid).first()

        new.s_value = request.form["value"]
        new.s_note = request.form["note"]

        db.session.commit()
        return redirect('/spo2_record')

#For Calorie table

@app.route("/cal_record/", methods=["GET", "POST"])
def cdisp():
    if request.method == "GET":
        #For graph
        over_time_cal = []
        dates = db.session.query(db.func.sum(Calorie.cal_value), Calorie.cal_time).group_by(Calorie.cal_time).order_by(Calorie.cal_time).all()
        dates_label = []
        for amount, date in dates:
            dates_label.append(date.strftime("%m-%d-%y"))
            over_time_cal.append(amount)

        #For Table
        data = Calorie.query.all()
        return render_template("disp_cal.html", c_d = data, over_time_cal = json.dumps(over_time_cal), dates_label =json.dumps(dates_label))


@app.route("/add_cal/", methods=["GET", "POST"])
def add_cal():
    if request.method == "GET":
        return render_template("add_cal.html")
    else:
        # get the current datetime and store it in a variable
        currentDateTime = datetime.datetime.now()   

        tvalue = request.form["cal"]
        tnote = request.form["cal_note"]

        c = Calorie(cal_time = currentDateTime, cal_value=tvalue, cal_note=tnote)

        db.session.add(c)
        db.session.commit()

        return redirect("/cal_record/")

@app.route("/cal/<int:tid>/delete")
def del_cal(tid):
    data = Calorie.query.filter(Calorie.cal_id == tid).one()
    db.session.delete(data)
    db.session.commit()
    return redirect('/cal_record')

@app.route("/cal/<int:tid>/update", methods=["GET", "POST"])
def update_cal(tid):
    if request.method == "GET":
        data = Calorie.query.filter(Calorie.cal_id == tid).first()
        return render_template("update_cal.html", c_d=data)

    else:

        new = Calorie.query.filter_by(cal_id=tid).first()

        new.cal_value = request.form["value"]
        new.cal_note = request.form["note"]

        db.session.commit()
        return redirect('/cal_record')