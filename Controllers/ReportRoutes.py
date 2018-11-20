from flask import Blueprint, request, render_template, abort, session, redirect, jsonify, session, Response
from Models.Report import *
from Models.Office import Office
from Models.db.MongoModels import DB
from Utilities.Methods import success_response, error_response, threaded
from config import appConfig
import os
from time import time

mod = Blueprint('report_routes', __name__)

@threaded
@mod.route('/api/report/generate', methods=['POST'])
def generate_report():
    # get office param
    office_id = request.args.get('office', default=None, type=str)
    source = request.args.get('source', default=None, type=str)

    mag = 3

    # if office param not passed use a test office_id
    if office_id is None:
        office_id = 'c4e482f6-e21f-11e8-9ada-d20785d6bfad'

    if source is None:
        return error_response('no source supplied')

    # load file - if error then return such
    # TODO: parser for other genome file types ( ancestry, etc. )
    file = request.files['file']
    report_id = REPORT_ID().generate()

    temp_file_path = "{}/misc/tmp/{}".format(appConfig['ROOT_PATH'], report_id)
    file.save(temp_file_path)
    genome_file = REPORT_FILE(file=temp_file_path, source=source).load()

    if not genome_file:
        return error_response('invalid file')

    # insert report ID if file parsed
    REPORT_ID().insert(report_id)
    report_build = REPORT_BUILD(genome_file=genome_file, mag=mag)

    master_response_list = []

    office = Office(office_id=office_id)
    office_query = office.find_one()
    filters = office.get_genes_and_keywords(query=office_query)

    for filter in filters:
        genes_list = filter['gene']
        db_base_query = report_build.return_snps_from_genes(
            genes_list=genes_list)
        master_response_list += report_build.generate_report(
            db_base_query, keyword=filter['keyword'])

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

    os.remove(temp_file_path)

    DB(collection='reports').update(query={"report_id": report_id}, updated_dict=report)

    return success_response(report['report_id'])


@mod.route('/api/report/<report_id>', methods=['GET', 'DELETE'])
def handle_report(report_id):
    report_db_init = DB(collection='reports')

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
