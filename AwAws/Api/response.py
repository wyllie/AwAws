import json

from http import HTTPStatus

# The response class is used to build well formed and
# consistent responses to API requests


class Response():
    def __init__(self):
        self.status_code = 0
        self.body = None

        # Set up CORS Headers by default
        self.headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
        }


    def ok_200(self, body=None):
        """Return a 200 status, set body if exists - can be type dict or json"""
        self.set_status_code(200)
        if type(body) == dict:
            self.set_body(json.dumps(body))
        else:
            self.set_body(body)
        return self._build_response()


    def error_4XX(self, message=None):
        """send and error code (in the 400 range) - default to 422"""
        status_code = self.status_code
        if (status_code < 400) or (status_code > 499):
            self.set_status_code(422)

        if message is not None:
            self.set_body({'message': message})

        return self._build_response()


    def error_5XX(self, message=None):
        """send a system error code (in the 500 range)"""
        status_code = self.status_code
        if (status_code < 500) or (status_code > 599):
            self.set_status_code(500)

        if message is not None:
            self.set_body({'message': message})

        return self._build_response()


    def set_status_code(self, status_code):
        """Only used if you need to override the status code"""
        try:
            HTTPStatus(status_code)
            self.status_code = status_code
        except Exception as e:
            raise Exception("Status code: %s - not supported - %s", status_code, e)

        return self.status_code


    def set_body(self, body):
        """Set the body of the response message"""
        if type(body) == dict:
            self.body = json.dumps(body)
        else:
            self.body = body

        return self.body


    def set_header(self, key, value=None):
        """Set the a header on this response"""
        if key is None:
            raise Exception('a header key is required; %s')
        self.headers[key] = value


    def _build_response(self):
        if self.status_code <= 0 or self.headers is None:
            raise Exception("Response not well formed, Status: %s, Headers: %s, Body: %s - %s",
                            self.status_code, self.headers, self.body)

        return {
            "statusCode": self.status_code,
            "headers": self.headers,
            "body": self.body
        }
