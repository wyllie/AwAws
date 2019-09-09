import os


class Env():
    def __init__(self):
        self.env = os.environ


    def get_env(self, key):
        'get an environment variable'
        try:
            ret = self.env[key]
        except Exception:
            # variable does not exist, set it to None
            ret = None

        return ret


    def set_env(self, key, value):
        'set an environment variable, value None unsets the var'

        if value is None:
            try:
                os.environ.pop(key)
            except KeyError:
                # just fail silently if setting to None
                pass
        else:
            self.env[key] = value
