"""
 Copyright 2016, 2018 John J. Rofrano. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import os
from flask import Flask, jsonify
from flask_api import status
from flask_httpauth import HTTPBasicAuth

# Get global variables from the environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = int(os.getenv('PORT', '5000'))
HOST = str(os.getenv('VCAP_APP_HOST', '0.0.0.0'))

# get secrets from the environment
API_USERNAME = os.getenv('API_USERNAME', None)
API_PASSWORD = os.getenv('API_PASSWORD', None)

# Create Flask application
app = Flask(__name__)
auth = HTTPBasicAuth()

######################################################################
#                   E R R O R   H A N D L E R S
######################################################################
@auth.error_handler
def unauthorized():
    """
    return 403 instead of 401 to prevent browsers from displaying the default
    auth dialog to api callers
    """
    return jsonify({'error': 'Unauthorized access'}), status.HTTP_403_FORBIDDEN

@app.errorhandler(405)
def bad_request(error):
    """ Handle Method not Allowed """
    return jsonify({'error': 'Method not allowed'}), status.HTTP_405_METHOD_NOT_ALLOWED

@app.errorhandler(404)
def not_found(error):
    """ Handle 404 Not Found """
    return jsonify({'error': 'Not found'}), status.HTTP_404_NOT_FOUND


######################################################################
# Required to provide this method to make HTTPBasicAuth work
######################################################################
@auth.get_password
def get_password(username):
    """ Very simple inplementation to be replaced with something like an LDAP lookup """
    if username and username == API_USERNAME:
        return API_PASSWORD
    return None

######################################################################
# GET Requests
######################################################################
@app.route('/', methods=['GET'])
@auth.login_required
def index():
    """ Display the Home Page """
    return jsonify(message='Shhh this is a top secret web site!!!'), status.HTTP_200_OK

@app.route('/hello', methods=['GET'])
@auth.login_required
def hello():
    """ Simulate an API that requires proper authentiction to access """
    return jsonify(message='Hello Private World!'), status.HTTP_200_OK

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
