# lab-flask-basicauth
This repository is part of lab for the NYU DevOps class for Spring 2018, CSCI-GA.3033-013. It will show you how to use the Flask extension HTTPBasicAuth to secure your microservice

# Usage
In order to use the Flask HTTPBasicAuth extension you need to instantiate the class in your code:

```python
    from flask_httpauth import HTTPBasicAuth

    auth = HTTPBasicAuth()
```
If you are creating a microservice, you want to override the default web browser behavior of prompting for a userid and password by supplying your own authorization handler that does not return 401

```python
    @auth.error_handler
    def unauthorized():
        # return 403 instead of 401 to prevent browsers from displaying the default
        # auth dialog to api callers
        return jsonify({'error': 'Unauthorized access'}), 403
```

You must supply a function to return the password for a userid so that it can be checked by the HTTPBasicAuth class. Use the decorator `@auth.get_password` to designate this function:

```python
    @auth.get_password
    def get_password(username):
        # Make a call to LDAP here or authenticate yourself
        if username and username == API_USERNAME:
            return API_PASSWORD
        return None
```

Finally, just decorate any function that you want to protect with the `@auth.login_required` decorator:

```python
    @app.route('/', methods=['GET'])
    @auth.login_required
    def index():
        return jsonify(message='Shhh this is a top secret web site!!!'), 200
```

That's all there is to it.

# Testing
When testing you need to send the userid and password credentials in the `Authorization` header as *Basic* authorization. The userid and password should be delimited with a colon `:` and base64 encoded as 8-bit binary like this:

```python
    from base64 import b64encode

    self.headers = {
        'Authorization': 'Basic %s' % b64encode(b'<userid>:<password>')
    }

    resp = self.app.get("/", headers=self.headers)
    self.assertEqual(resp.status_code, status.HTTP_200_OK)

```
