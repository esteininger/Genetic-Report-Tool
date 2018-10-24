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
		result = check_json(json, ['name', 'email', 'provider_name', 'provider_email', 'url'])

		if result:
			return error_response("missing {}".format(result))

		User().add(json)
		mailer = Mailer()

		html = 'Name: {} \n Email: {} \n Provider: {} \n Provider Email: {}'.format(json['name'], json['email'], json['provider_name'], json['provider_email'])
		mailer.sendMail(html=html, toaddr="ethan@meports.com", subject="Meports: User provider request")

		mailer.sendProviderEmail(provider_name=json['provider_name'], provider_email=json['provider_email'], client_name=json['name'], url=json['url'], client_email=json['email'])

		return success_response('ok')
