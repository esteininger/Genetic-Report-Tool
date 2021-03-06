from flask import Flask
from Controllers import PageRoutes, ErrorRoutes, ReportRoutes, UserRoutes, GeneRoutes, OfficeRoutes
import os
from config import appConfig, sessionKey, getMode, sqlConfig
from Utilities.Database import sqlDB as db

app = Flask(__name__)

#app settings
app.secret_key = sessionKey
app.static_folder = appConfig['ROOT_PATH'] + '/Views/static'
app.template_folder = appConfig['ROOT_PATH'].split('Controllers')[0] + '/Views/templates'

#blueprints init
blueprints = (
    PageRoutes.mod,
    ErrorRoutes.mod,
    ReportRoutes.mod,
    GeneRoutes.mod,
    UserRoutes.mod,
    OfficeRoutes.mod
)

for bp in blueprints:
    app.register_blueprint(bp)

#sentry init
if getMode() == 'live':
    sentryLogger()

if __name__ == '__main__':
    app.run(host="localhost", port=5001, debug=True)
