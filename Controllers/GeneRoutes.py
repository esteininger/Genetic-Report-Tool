from flask import Blueprint, request, render_template, abort, session, redirect, jsonify, session, Response
from Models.Gene import Gene
from Utilities.Methods import success_response, error_response
from urllib.parse import unquote

mod = Blueprint('gene_routes', __name__)

@mod.route('/api/genes/search', methods=['GET'])
def search_genes():
	keyword = request.args.get('keyword', default='', type=str)
	limit = request.args.get('limit', default=100, type=int)

	try:
		result = Gene().search(unquote(keyword), limit)
		return success_response(result)
	except Exception as e:
		return error_response(e)
