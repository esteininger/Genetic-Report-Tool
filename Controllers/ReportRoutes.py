from flask import Blueprint, request, render_template, abort, session, redirect, jsonify, session, Response
from Models.Report import ReportFile, ReportBuild, ReportID, ReportDB
from Models.Office import Office
from Utilities.Methods import success_response, error_response
from config import appConfig
import os
from time import time

mod = Blueprint('report_routes', __name__)

@mod.route('/api/report/generate', methods=['POST'])
def generate_report():
    # get office param
    office_id = request.args.get('office', default=None, type=str)

    try:
        # load file - if error then return such
        # TODO: parser for other genome file types ( ancestry, etc. )
        file = request.files['file']
        report_id = ReportID().generate()
        temp_file_path = "{}/misc/tmp/{}.txt".format(
            appConfig['ROOT_PATH'], report_id)

        file.save(temp_file_path)
        genome_file = ReportFile(file=temp_file_path).load_file()
        os.remove(temp_file_path)

        if not genome_file:
            return error_response('invalid file')

        # insert report ID if file parsed
        ReportID().insert(report_id)
        report_build = ReportBuild(genome_file=genome_file)

        master_response_list = []
        mag = 1

        # if office param not passed use a test office_id
        if office_id is None:
            office_id = 'c4e482f6-e21f-11e8-9ada-d20785d6bfad'

        office = Office(office_id=office_id)
        office_query = office.find_one()
        filters = office.get_genes_and_keywords(query=office_query)

        for filter in filters:
            genes_list = filter['gene']
            db_base_query = report_build.return_snps_from_genes(genes_list=genes_list, mag=mag)
            master_response_list += report_build.generate_report(mag, db_base_query, keyword=filter['keyword'])

        report = {}
        report['report_dict'] = report_build.uniquify(master_response_list)
        report['timestamp'] = time()
        report['report_id'] = report_id

        report['office'] = {
            "id": office_query['office_id'],
            "name": office_query['name'],
            "email": office_query['email']
        }

        session['report_id'] = report_id

        ReportDB(collection='reports').update(query={"report_id": report_id}, updated_dict=report)

        return success_response(report['report_id'])

    except Exception as e:
        print (e)
        return error_response(e)


@mod.route('/api/report/<report_id>', methods=['GET', 'DELETE'])
def handle_report(report_id):
    report_db_init = ReportDB(collection='reports')

    query = {"report_id": report_id}

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
