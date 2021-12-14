from datetime import datetime, timedelta, date
from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class Attendance:
    def setAttendance(self):
        # rule for timeIn and timeOut

        now = datetime.now()
        timeIn = now.replace(hour=8, minute=0, second=0, microsecond=0)
        timeOut = now.replace(hour=17, minute=0, second=0, microsecond=0)

        data = db.attendance.find_one({"email": session['email'], "timeOut" : ""})
        today = datetime.today()
        if session['email'] == "":
            return redirect('/user/')
        # check if data exist
        if data:
            # if data exist check data's date compare to today's, if not equal create new document 
            if today.strftime("%d/%m/%Y") > data['timeIn'].strftime("%d/%m/%Y"):
                if now < timeIn:  
                    attendance = db.attendance.insert_one({
                        "_id": uuid.uuid4().hex,
                        "email" : session['email'],
                        "status" : "Hadir",
                        "location": session['location'],
                        "timeIn" : today,
                        "timeOut" : "",
                        "late" : False
                    })
                    return redirect('/user/')
                if now > timeIn and now <= timeOut:  
                    attendance = db.attendance.insert_one({
                        "_id": uuid.uuid4().hex,
                        "email" : session['email'],
                        "status" : "Terlambat",
                        "location" : session['location'],
                        "timeIn" : today,
                         "timeOut" : "",
                        "late" : True
                    })
                    return redirect('/user/') 
                if now > timeOut:  
                    update = {
                    "location": session['location'],    
                    "status" : "Pulang",
                    "timeOut" : today
                    }
                    attendance = db.attendance.find_one_and_update({"email": session['email'], "timeOut" : ""}, { '$set': update } )
                    return redirect('/user/')
                return redirect('/user/')
            elif today.strftime("%d/%m/%Y") == data['timeIn'].strftime("%d/%m/%Y"):
                if now > timeIn and now < timeOut:
                    update = {
                    "location": session['location'],
                    "status" : "Terlambat",
                    "timeOut" : ""
                    }
                    attendance = db.attendance.find_one_and_update({"email": session['email'], "timeOut" : ""}, { '$set': update } )
                    return redirect('/user/')
                
                if now > timeOut:  
                    update = {
                    "location": session['location'],
                    "status" : "Pulang",
                    "timeOut" : today
                    }
                    attendance = db.attendance.find_one_and_update({"email": session['email'], "timeOut" : ""}, { '$set': update } )
                    return redirect('/user/')
                else:
                    return redirect('/user/')
            else:
                return redirect('/user/') 
        # if data doesn't exist create new document with rules
        else:  
            if now < timeIn:  
                attendance = db.attendance.insert_one({
                        "_id" : uuid.uuid4().hex,
                        "email" : session['email'],
                        "status" : "Hadir",
                        "location" : session['location'],
                        "timeIn" : today,
                        "timeOut" : "",
                        "late" : False
                    })
                return redirect('/user/') 
            if now > timeIn and now < timeOut:  
                attendance = db.attendance.insert_one({
                        "_id" : uuid.uuid4().hex,
                        "email" : session['email'],
                        "status" : "Terlambat",
                        "location" : session['location'],
                        "timeIn" : today,
                         "timeOut" : "",
                        "late" : True
                    })
                return redirect('/user/')
            return redirect('/user/')

    def getAttendance(self):
        attendance = db.attendance.find()
        return attendance

    def getReport(self):
        reports = db.attendance.find()
        return reports
