from flask import Blueprint, request, render_template, abort, session, redirect, jsonify, session, Response
from Models.Office import Office
from Utilities.Methods import success_response, error_response, check_json
from Utilities.Security import encrypt, decrypt
import json
import ast

mod = Blueprint('office_routes', __name__)

@mod.route('/api/office', methods=['POST'])
def insert_profile():
	if request.method == 'POST':
		json = request.form.to_dict(flat=True)
		result = check_json(json, ['name', 'email', 'specialty', 'password', 'keywords', 'genes'])

		if result:
			return error_response("missing {}".format(result))


		office_db = Office()

		json['office_id'] = office_db.unique_id()
		json['password'] = encrypt(json['password'])
		json['keyword_genes'] = ast.literal_eval(json['genes'])

		#remove key/value from json before insertion
		del json['genes']
		del json['keywords']

		# TODO: check if email exists

		office_db.insert(json)

		return success_response(json['office_id'])
