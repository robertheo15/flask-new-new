from flask import Flask, render_template, session, redirect
from app import app
from controllers.user.models import User

# @app.route("/admin/user/")
# def adminUser():
#     users = User().getUser()
#     return render_template('admin/user.html', myUsers=users)
       
# @app.route("/admin/absensi/")
# def absensi():
#     return render_template('admin/absensi.html')

# @app.route("/admin/report/")
# def report():
#     reports = User().getReport()
#     return render_template('admin/report.html', myReports=reports)

# @app.route('/admin/signout')
# def signout():
#     return User().signOut()

# @app.route('/admin/signin', methods=['POST'])
# def signin():
#     return User().login()