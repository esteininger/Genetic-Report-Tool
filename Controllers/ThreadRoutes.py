# from flask import Blueprint, request, render_template, abort, session, redirect, Response
# import time
#
# @mod.route('/')
# def index():
#     global exporting_threads
#
#     thread_id = random.randint(0, 10000)
#     exporting_threads[thread_id] = ExportingThread()
#     exporting_threads[thread_id].start()
#
#     return 'task id: #%s' % thread_id
#
#
# @mod.route('/api/progress/<int:thread_id>')
# def progress(thread_id):
#     global exporting_threads
#
#     return str(exporting_threads[thread_id].progress)
