from flask import Blueprint, request, render_template, abort, session, redirect, Response
import time

mod = Blueprint('file_routes', __name__)

def generate():
    for x in range(0, 10000000):
        print (x)
        time.sleep(0.1)
        yield "data:" + str(x) + "\n\n"

@mod.route('/api/file/process')
def retrieveFile():
    return Response(generate(), mimetype= 'text/event-stream')
