from flask import Blueprint, request, render_template, abort, session, redirect, jsonify, session, Response
from Models.Report import ReportFile, ReportBuild, ReportID, ReportDB
from Utilities.Methods import success_response, error_response
from config import appConfig
import os
from time import time

mod = Blueprint('report_routes', __name__)

@mod.route('/api/report/generate', methods=['POST'])
def generate_report():
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
			filters = [{"tags":"acmg"}, {"tags":"noteworthy"}]
			mag = 2

			# for tag in tags:

			for tag in filters:
				db_base_query = report_build.base_query(collection='snps', query=tag, mag=mag)
				file_to_db_comparison_result = report_build.generate_report(mag, db_base_query)
				master_response_list += file_to_db_comparison_result

			report = {}
			report['report_dict'] = master_response_list
			report['timestamp'] = time()
			report['report_id'] = report_id

			session['report_id'] = report_id

			ReportDB(collection='reports').update(query={"report_id":report_id}, updated_dict=report)

			return success_response(report['report_id'])

	except Exception as e:
		print (e)
		return error_response(e)

@mod.route('/api/report/<report_id>', methods=['GET', 'DELETE'])
def handle_report(report_id):
	report_db_init = ReportDB(collection='reports')

	query = {"report_id":report_id}

	if request.method == 'GET':
		try:
			report_dict = report_db_init.search_db_one(query)
			if report_dict:
				return success_response(report_dict)
			else:
				return error_response('none')
		except Exception as e:
			return error_response(e)

	if request.method == 'DELETE':
		try:
			report_db_init.delete_one(query)
			return success_response('ok')
		except Exception as e:
			print (e)
			return error_response(e)
