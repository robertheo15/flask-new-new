from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid


class Admin:
    def addAdmin(self):
        # create the admin object
        admin = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
        }

        #Check for existing email address
        if db.users.find_one({"email":admin['email']}):
            return jsonify({"error":"Email address already in use"}),400

        if db.users.insert_one(admin):
            return jsonify(admin), 200

        return jsonify({"error":"Signup failed"}), 400

    def getAdmin(self):
        users = db.users.find()
        return users

    def deleteAdmin(self, _id):
        # myQuery = { "_id": _id }
        users = db.users.delete_one({ "_id": _id })
        return users

    def getReport(self):
        reports = db.absensi.find()
        return reports
