from flask import Blueprint, request, render_template, abort, session, redirect
from Utilities.Methods import success_response, error_response, check_json
from Utilities.Mailer import Mailer
from Models.User import User
from werkzeug.datastructures import ImmutableMultiDict

mod = Blueprint('user_routes', __name__)

@mod.route('/api/user', methods=['POST'])
def profile_handler():
	if request.method == 'POST':
		json = request.form.to_dict(flat=True)
		result = check_json(json, ['name', 'email', 'provider_name', 'provider_email'])

		if result:
			return error_response("missing {}".format(result))

		user = User()
		user.add(json)

		return success_response('ok')
