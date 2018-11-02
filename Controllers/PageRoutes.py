from flask import Blueprint, request, render_template, abort, session, redirect
from Models.db.MongoModels import DB

mod = Blueprint('page_routes', __name__)

@mod.route('/')
@mod.route('/upload')
def home_page():
	return render_template("index.html")

@mod.route('/office')
def office_page():
	return render_template("office.html")

# @mod.route('/office/<id>', methods=['GET'])
# def office_report_builder_page(id):
# 	office_exists = False
# 	init_office_db = DB(collection='genes')
#
# 	query = init_genes_db.search_db_one({"gene":id.upper()})
# 	if query:
# 		gene_exists = True
#
# 	return render_template("gene.html", office_exists=office_exists, gene=query)

@mod.route('/report/<report_id>', methods=['GET'])
def report_page(report_id):
	report_exists = False
	init_report_db = DB(collection='reports')

	if init_report_db.search_db_one({"report_id":report_id}):
		report_exists = True

	return render_template("report.html", report_exists=report_exists, report_id=report_id)

@mod.route('/gene/<id>', methods=['GET'])
def gene_page(id):
	gene_exists = False
	init_genes_db = DB(collection='genes')

	query = init_genes_db.search_db_one({"gene":id.upper()})
	if query:
		gene_exists = True

	return render_template("gene.html", gene_exists=gene_exists, gene=query)
