from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid


class User:
    def addUser(self):
        # create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "jabatan": request.form.get('jabatan'),
        }

        #Check for existing email address
        if db.users.find_one({"email":user['email']}):
            return jsonify({"error":"Email address already in use"}),400

        if db.users.insert_one(user):
            return jsonify(user), 200

        return jsonify({"error":"Signup failed"}), 400

    def getUser(self):
        users = db.users.find()
        return users

    def deleteUser(self, _id):
        users = db.users.delete_one({ "_id": _id })
        return users

    def getReport(self):
        reports = db.absensi.find()
        return reports

   