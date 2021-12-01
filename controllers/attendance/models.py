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

        data = db.attendance.find_one({"email": session['email']})
        today = date.today()

        # check if data exist
        if data:
            # if data exist check data's date compare to today's, if not equal create new document 
            if today > data['datetime']:

                if now < timeIn:  
                    attendance = db.attendance.insert_one({
                        "_id": uuid.uuid4().hex,
                        "email": "test",
                        "status": "Hadir",
                        "datetime": today,
                        "late": False
                    })
                    return jsonify(attendance), 200

                if now > timeIn:  
                    attendance = db.attendance.insert_one({
                        "_id": uuid.uuid4().hex,
                        "email": "test",
                        "status": "Hadir",
                        "datetime": today,
                        "late": False
                    })
                    return jsonify(attendance), 200    

    def updateAttendance(self):
        # rule for timeIn and timeOut
        now = datetime.now()
        timeIn = now.replace(hour=8, minute=0, second=0, microsecond=0)
        timeOut = now.replace(hour=17, minute=0, second=0, microsecond=0)

        data = db.attendance.find_one({"email": session['email']})
        today = date.today()

        # check if data exist
        if data:
            # if data exist check data's date compare to today's, if not equal create new document 
            if  data['datetime'] == today:
                update = {
                    "status": "Hadir & pulang",
                    "datetime": today,
                }

                if now > timeOut: 
                    attendance = db.attendance.find_one_and_update({"email": data['email']}, { '$set': update } )
                return jsonify(attendance), 200

        return jsonify({"msg":"data doesn't exist"}), 400

    def getAttendance(self):
        attendance = db.attendance.find()
        return attendance

    def getReport(self):
        reports = db.attendance.find()
        return reports
