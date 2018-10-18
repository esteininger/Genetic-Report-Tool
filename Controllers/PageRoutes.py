from flask import Blueprint, request, render_template, abort, session, redirect
from Models.User import UserService
from Models.Report import ReportDB

mod = Blueprint('page_routes', __name__)

@mod.route('/')
def home_page():
	return render_template("index.html")

@mod.route('/report/<report_id>', methods=['GET'])
def report_page(report_id):
	report_exists = False
	init_report_db = ReportDB(collection='reports')

	if init_report_db.search_db_one({"report_id":report_id}):
		report_exists = True

	return render_template("report.html", report_exists=report_exists, report_id=report_id)

@mod.route('/privacy')
def privacy_page():
	return render_template("privacy.html")
