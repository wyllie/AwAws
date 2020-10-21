import json
import os
import signal
import sys
import requests

'''
This is the base class for lambda extensions.  The actual extensions can be found in the top
level /extensions directory.  Extensions can be used to initialize objects and data before
the lambda starts running as well as handing logging or other types of error reporting without
affecting the code in the lambda itself
'''


class Extension:
    def __init__(self):
        self.name = os.path.basename(sys.argv[0])
        self.extension_id = None
        self.events = ['INVOKE', 'SHUTDOWN']
        self.lambda_api = os.environ['AWS_LAMBDA_RUNTIME_API']

        # catch and handle signals
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    def register_extension(self):
        'the extension needs to be registered or lambda will not run it'
        print(f"[{self.name}] Registering extension", flush=True)

        url = f"http://{self.lambda_api}/2020-01-01/extension/register"
        headers = {
            'Lambda-Extension-Name': self.name
        }
        payload = {
            'events': self.events
        }
        response = requests.post(
            url=url,
            headers=headers,
            json=payload
        )
        self.extension_id = response.headers['Lambda-Extension-Identifier']
        print(f"[{self.name}] Registered with ID: {self.extension_id}", flush=True)

    def process_events(self):
        'this listens for events from the lambda service'
        url = f"http://{self.lambda_api}/2020-01-01/extension/event/next"
        headers = {
            'Lambda-Extension-Identifier': self.extension_id
        }

        # set up a loop and wait for incoming requests
        while True:
            print(f"[{self.name}] Waiting for event...", flush=True)
            response = requests.get(
                url=url,
                headers=headers,
                timeout=None
            )
            event = json.loads(response.text)
            if event['eventType'] == 'SHUTDOWN':
                self.exit_processing()
            else:
                self.event_processing(event)

    def event_processing(self, event):
        'runs on every lambda invoke event - override function to do something more interesting'
        print(f'[{self.name}] Received event: {json.dumps(event)}', flush=True)

    def exit_processing(self):
        'do something when the function exits - override this to do something more interesting'
        print(f'[{self.name}] Received SHUTDOWN event. Exiting!', flush=True)
        sys.exit(0)

    def handle_signal(self, sig, frame):
        'if needed, pass this signal down to child process'
        print(f"[{self.name}] Received signal={sig}. Exiting", flush=True)
        sys.exit(0)
