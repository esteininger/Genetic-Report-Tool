import os

appConfig = {
    'ROOT_PATH': os.path.dirname(os.path.abspath(__file__))
}

mongoConfig = {
    'IP': '67.205.137.170',
    'PORT': 27017,
    'USERNAME': 'adminMain',
    'PASSWORD': 'shJbk72bV12',
    'DATABASE': 'meports_dev'
    # 'DATABASE': 'meports'
}

sqlConfig = {
    'IP': '67.205.137.170',
    'USERNAME': 'main',
    'PASSWORD': 'j*!3j/^Vn!<dTC&',
    'DATABASE': 'Meports_dev'
    # 'DATABASE': 'Meports'
}

emailConfig = {
    'ADDRESS' : 'appinternalservice@gmail.com',
    'PASSWORD' : 'internalservice',
    'SMTP': 'smtp.gmail.com',
    'PORT': 587
}

sessionKey = 'wdjhKUYhdajsKJY2398asdgKJH'
secretKey = 'akshdjasdGHJsslkgajh'
sentryDSN = 'https://4f3fb0408670420e8a08986d353edfd2:966054ed6ba840ba99442b9db89f3c43@sentry.io/287805'


def getMode():
    server = str(os.path.realpath('.'))
    if "ethan" in server:
        return 'test'
    else:
        return 'live'
