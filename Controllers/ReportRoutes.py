from flask import Blueprint, request, render_template, abort, session, redirect, jsonify, session, Response
from Models.Report import ReportFile, ReportBuild, ReportID, ReportDB
from Utilities.Methods import success_response, error_response
from config import appConfig
import os
from time import time

mod = Blueprint('report_routes', __name__)


@mod.route('/api/report/generate', methods=['POST'])
def retrieve_report():
	try:
		file = request.files['file']
		report_id = ReportID().generate()
		temp_file_path = "{}/misc/tmp/{}.txt".format(appConfig['ROOT_PATH'], report_id)

		file.save(temp_file_path)
		genome_file = ReportFile(file=temp_file_path).load_file()
		os.remove(temp_file_path)

		if not genome_file:
			return error_response('invalid file')

		else:
			ReportID().insert(report_id)
			report_build = ReportBuild(genome_file=genome_file)

			master_response_list = []
			tags = [{"tags":"acmg"}]
			mag = 3

			for tag in tags:
				db_base_query = report_build.base_query(collection='snps', query=tag, mag=mag)
				db_base_query['tag'] = tag
				file_to_db_comparison_result = report_build.generate_report(mag, db_base_query)
				print ('results...')
				print (file_to_db_comparison_result)
				master_response_list += file_to_db_comparison_result

			report = {}
			report['report_dict'] = master_response_list
			report['timestamp'] = time()
			report['report_id'] = report_id

			session['report_id'] = report_id

			try:
				ReportDB(collection='reports').update(query={"report_id":report_id}, updated_dict=report)
				print ('uploaded')
			except Exception as e:
				print (e)
				pass

			return success_response(report['report_id'])

	except Exception as e:
		print (e)
		return error_response(e)

@mod.route('/report/<report_id>', methods=['GET', 'DELETE'])
def return_report(report_id):
	report_db_init = ReportDB(collection='reports')

	for_who = request.args.get('for', default=None, type=str)
	query = {"report_id":report_id}

	if request.method == 'GET':
		try:
			report_dict = report_db_init.search_db_one(query)
			return render_template("report.html", report_dict=report_dict, for_who=for_who)
		except Exception as e:
			return render_template("report.html")

	if request.method == 'DELETE':
		try:
			report_db_init.delete_one(query)
			return success_response('ok')
		except Exception as e:
			return error_response(e)
