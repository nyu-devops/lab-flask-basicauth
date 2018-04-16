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

# Test cases can be run with any of the following:
# nosetests -v --rednose --with-coverage --cover-package=service
# coverage report -m --include=service.py

import unittest
from base64 import b64encode
from flask_api import status
import service

######################################################################
#  T E S T   C A S E S
######################################################################
class TestPetService(unittest.TestCase):
    """ Test Cases for Service """

    def setUp(self):
        service.app.debug = True
        self.app = service.app.test_client()
        service.API_USERNAME = "tester"
        service.API_PASSWORD = "s3cr3t"
        self.headers = {
            'Authorization': 'Basic %s' % \
            b64encode(b'{}:{}'.format(service.API_USERNAME, service.API_PASSWORD))
        }

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get("/", headers=self.headers)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('Shhh', resp.data)

    def test_not_autorized(self):
        """ Test for not authorized """
        resp = self.app.get('/hello')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_method_not_allowed(self):
        """ Test for method not allowed """
        resp = self.app.post("/hello", headers=self.headers)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_found(self):
        """ test for not found """
        resp = self.app.get("/foo", headers=self.headers)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_bad_userid(self):
        """ Test using bad headers """
        bad_headers = {
            'Authorization': 'Basic %s' % b64encode(b'hacker:s3cr3t')
        }
        resp = self.app.get("/hello", headers=bad_headers)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_pet_list(self):
        """ Test for proper authorization """
        resp = self.app.get('/hello', headers=self.headers)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        self.assertIn('Private', resp.data)

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
