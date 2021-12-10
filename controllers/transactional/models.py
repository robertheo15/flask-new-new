from datetime import datetime, timedelta, date
from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid


class Transactional:
    def setTransactional(self):
        now = datetime.now()
        today = datetime.today()

        # create the transactional object
        transactional = {
            "_id": uuid.uuid4().hex,
            "email": session['email'],
            "location": session['location'],
            "datetime": today,
        }

        # if session['email'] == "":
        #     return redirect('/user/') 
        # else:
        #     transactional = db.transactional.insert_one({
        #                         "_id": uuid.uuid4().hex,
        #                             "email": session['email'],
        #                             "location": session['location'],
        #                             "date": today,
        #                             "time": now
        #                         })
        #     return redirect('/user/') 

        data = db.attendance.find_one({"email": session['email']})
        # check if data exist
        if data:
            # if data exist check data's date compare to today's, if not equal create new document 
            if today > data['datetime']:

                if now < data['datetime']:   
                    transactional = db.transactional.insert_one({
                        "_id": uuid.uuid4().hex,
                        "email": session['email'],
                        "location": session['location'],
                        "datetime": today,
                        }) 
                    return redirect('/user/')

                transactional = db.transactional.insert_one({
                       "_id": uuid.uuid4().hex,
                        "email": session['email'],
                        "location": session['location'],
                        "datetime": today,
                    })
                return redirect('/user/')
                
                
            transactional = db.transactional.insert_one({
                       "_id": uuid.uuid4().hex,
                        "email": session['email'],
                        "location": session['location'],
                        "datetime": today,
                    })
            return redirect('/user/')
             
   

    def updateTransactional(self):
        data = db.transactional.find_one({"email": session['email']})

        # rule for now and today
        now = datetime.now()
        today = date.today()

        # check if data exist
        if data:
            # if data exist check data's date compare to today's and data's time to now. and update
            if  data['date'] == today and now > data['time'] : 
                update = {
                    "status": "lobi",
                    "time": today,
                }
                transactional = db.transactional.find_one_and_update({"email": transactional['email']}, { '$set': update } )
                return jsonify(transactional), 200

        return jsonify({"msg":"data doesn't exist"}), 400

    def getTransactional(self):
        transactional = db.transactional.find()
        return transactional


    def getReport(self):
        reports = db.transactional.find()
        return reports

    
