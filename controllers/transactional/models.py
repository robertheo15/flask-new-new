from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid


class Transactional:
    def setTransactional(self):
        # create the transactional object
        transactional = {
            "_id": uuid.uuid4().hex,
            "email": request.form.get('name'),
            "location": request.form.get('email'),
            "datetime": request.form.get('password'),
        }

        #Check if already exist update location and time
        if db.transactional.find_one({"email":transactional['email']}):
            return jsonify({"error":"Email address already in use"}),400

        # check if not exist create new document do db
        if db.transactional.insert_one(transactional):
            return jsonify(transactional), 200

        return jsonify({"error":"Signup failed"}), 400

    def getTransactional(self):
        transactional = db.transactional.find()
        return transactional


    def getReport(self):
        reports = db.transactional.find()
        return reports

    
