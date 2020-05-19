import io
import pprint
import traceback
# class for common AwAws Exceptions


class AwAwsException(Exception):
    def __init__(self, mesg, e=None):
        self.open_message()
        self.default_message(mesg)
        self.append_traceback()
        self.throw_exception()

    def open_message(self):
        self.output = io.StringIO()

    def append_message(self, message):
        self.output.write(message)
        self.output.write('\n')

    def pprint_message(self, message):
        pprint.pprint(message, stream=self.output)

    def append_traceback(self):
        self.append_message(traceback.format_exc())

    def default_message(self, mesg):
        self.append_message(' '.join(['AwAws Excetption:\n', str(mesg)]))

    def read_message(self):
        return self.output.getvalue()

    def close_message(self):
        self.output.close()

    def __str__(self):
        return self.read_message()

    def throw_exception(self):
        raise self


class AwAwsMissingParameter(AwAwsException):
    def __init__(self, message, parameters):
        self.open_message()
        self.append_message('Missing required or expected parameter')
        self.append_message(message)
        self.pprint_message(parameters)
        self.throw_exception()


class AwAwsConfigurationError(AwAwsException):
    def __init__(self, message):
        self.open_message()
        self.append_message('Invalid Configuration: Missing required or expected parameter')
        self.pprint_message(message)
        self.throw_exception()


class AwAwsInvalidEvent(AwAwsException):
    def __init__(self, message):
        self.open_message()
        self.pprint_message('Invalid Event Syntax: ' + message)
        self.throw_exception()


class AwAwsInvalidHttpMethod(AwAwsException):
    def __init__(self, method):
        self.open_message()
        self.pprint_message('Not a valid http method: ' + method)
        self.throw_exception()


class AwAwsMissingRequirement(AwAwsException):
    def __init__(self, message):
        self.open_message()
        self.pprint_message('Missing Requirement: ' + message)
        self.throw_exception()
