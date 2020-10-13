import json
import os
import signal
import sys
import requests


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
        response = requests.post(url, headers, payload)
        print('DUMP:', url, response.headers, response.text)

        self.extension_id = response.headers['Lambda-Extension-Identifier']
        print(f"[{self.name}] Registered with ID: {self.extension_id}", flush=True)
        print(f"Registration Response: {response.text}", flush=True)

    def process_events(self):
        'this listens for events from lambda'
        url = f"http://{self.lambda_api}/2020-01-01/extension/event/next"
        headers = {
            'Lambda-Extension-Identifier': self.extension_id
        }

        # set up a loop and wait for incoming requests
        while True:
            print(f"[{self.name}] Waiting for event...", flush=True)
            response = requests.get(url, headers, timeout=None)

            event = json.loads(response.text)
            if event['eventType'] == 'SHUTDOWN':
                self.exit_processing()
            else:
                self.event_processing(event)

    def event_processing(self, event):
        'do something with the event'
        print(f'[{self.name}] Received event: {json.dumps(event)}', flush=True)

    def exit_processing(self):
        'do something when the function exits'
        print(f'[{self.name}] Received SHUTDOWN event. Exiting!', flush=True)
        sys.exit(0)

    def handle_signal(self, sig, frame):
        'if needed, pass this signal down to child process'
        print(f"[{self.name}] Received signal={sig}. Exiting", flush=True)
        sys.exit(0)
