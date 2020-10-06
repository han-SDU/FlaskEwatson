from datetime import datetime
from flask_json import json_response as res
from flask import request as req
from flask import Flask
from __main__ import app
import logging
from flask import Blueprint

base_api = Blueprint('base_api', __name__)
logging.getLogger(__name__)


#Base base and misc routes
#Identifier that this is the box
@base_api.route('/identity', methods=['GET'])
def base_identity():
	logging.debug("Received request /identity")
	return res(200, identifier="HelloSensorBox785179218796217896319", timeUTC=datetime.utcnow())
	