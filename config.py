import os

appConfig = {
    'ROOT_PATH': os.path.dirname(os.path.abspath(__file__))
}

mongoConfig = {
    'IP': '',
    'PORT': ,
    'USERNAME': '',
    'PASSWORD': '',
    'DATABASE': ''
}

sqlConfig = {
    'IP': '',
    'USERNAME': '',
    'PASSWORD': '',
    'DATABASE': ''
}

emailConfig = {
    'ADDRESS' : '',
    'PASSWORD' : 'internalservice',
    'SMTP': 'smtp.gmail.com',
    'PORT': 587
}

sessionKey = ''
secretKey = ''
sentryDSN = ''


def getMode():
    server = str(os.path.realpath('.'))
    if "ethan" in server:
        return 'test'
    else:
        return 'live'
