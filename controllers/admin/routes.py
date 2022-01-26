from flask import Flask, render_template, session, redirect
from app import app
from controllers.admin.models import Admin
from controllers.attendance.models import Attendance
from datetime import datetime, timedelta, date

@app.route("/admin/user/")
def adminUser():
    users = Attendance().getReport()
    
    today = datetime.today().strftime("%m/%d/%Y")
    return render_template('admin/user.html', myUsers=users, today = today)
   
@app.route("/admin/absensi/")
def absensi():
    reports = Attendance().getReport()
    today = datetime.today().strftime("%m/%d/%Y")
    return render_template('admin/absensi.html', myReports = reports, today = today)

@app.route("/admin/report/")
def report():
    reports = Attendance().getReport()
    return render_template('admin/report.html', myReports = reports)

