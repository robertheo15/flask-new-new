from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid


class Attendance:
    def setAttendance(self):
        # create the admin object
        attendance = {
            "_id": uuid.uuid4().hex,
            "email": request.form.get('name'),
            "status": request.form.get('email'),
            "datetime": request.form.get('password'),
        }

        # Check for existing email address
        if db.attendance.find_one({"email": attendance['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        if db.attendance.insert_one(admin):
            return jsonify(admin), 200

        return jsonify({"error": "Signup failed"}), 400

    def getAttendance(self):
        attendance = db.attendance.find()
        return attendance

    def getReport(self):
        reports = db.attendance.find()
        return reports
