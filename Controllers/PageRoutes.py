from flask import Blueprint, request, render_template, abort, session, redirect
from Models.User import UserService

mod = Blueprint('page_routes', __name__)

@mod.route('/')
def home_page():
	return render_template("index.html")

@mod.route('/privacy')
def privacy_page():
	return render_template("privacy.html")
