from datetime import datetime
from flask_json import json_response as res
from flask import request as req
from flask import Flask
import traceback
from __main__ import app
import logging

logging.getLogger(__name__)

@app.errorhandler(403)
def handler_403(e):
	logging.debug(e)
	return res(403, error=str(e), time=datetime.utcnow())

@app.errorhandler(404)
def handler_404(e):
	logging.debug(e)
	return res(404, error=str(e), time=datetime.utcnow())

@app.errorhandler(405)
def handler_405(e):
	logging.debug(e)
	return res(405, error=str(e), time=datetime.utcnow())

@app.errorhandler(500)
def handler_500(e):
	logging.exception(e)
	traceback.print_exc()
	return res(500, error=str(e), time=datetime.utcnow())

@app.errorhandler(501)
def handler_501(e):
	logging.exception(e)
	return res(501, error=str(e), time=datetime.utcnow())

@app.errorhandler(Exception)
def handler_default(e):
	logging.exception(e)
	traceback.print_exc()
	return res(500, error=str(e), time=datetime.utcnow())
