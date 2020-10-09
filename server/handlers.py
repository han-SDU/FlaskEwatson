from datetime import datetime
from flask_json import json_response as res
from flask import request as req
from flask import Flask
import traceback
import logging
from flask import Blueprint

error_handler_api = Blueprint('error_handler_api', __name__)
logging.getLogger(__name__)

@error_handler_api.app_errorhandler(403)
def handler_403(e):
	logging.debug(e)
	return res(403, error=str(e), time=datetime.utcnow())

@error_handler_api.app_errorhandler(404)
def handler_404(e):
	logging.debug(e)
	return res(404, error=str(e), time=datetime.utcnow())

@error_handler_api.app_errorhandler(405)
def handler_405(e):
	logging.debug(e)
	return res(405, error=str(e), time=datetime.utcnow())

@error_handler_api.app_errorhandler(500)
def handler_500(e):
	logging.exception(e)
	traceback.print_exc()
	return res(500, error=str(e), time=datetime.utcnow())

@error_handler_api.app_errorhandler(501)
def handler_501(e):
	logging.exception(e)
	return res(501, error=str(e), time=datetime.utcnow())

@error_handler_api.app_errorhandler(Exception)
def handler_default(e):
	logging.exception(e)
	traceback.print_exc()
	return res(500, error=str(e), time=datetime.utcnow())
