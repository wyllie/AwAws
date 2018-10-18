import os


class Env():
    def __init__(self):
        self.env = os.environ

    def get_env(self, key):
        ret = None
        try:
            ret = self.env[key]
        except Exception as e:
            # variable does not exist, set it to None
            ret = None

        return ret
