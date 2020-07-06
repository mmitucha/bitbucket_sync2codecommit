#!/usr/bin/env python

from bitbucket_webhooks import event_schemas
from bitbucket_webhooks import hooks
from bitbucket_webhooks import router
from flask import Flask
from flask import request
import json
import logging
import shlex
import subprocess
import threading
import sys

SUBPROCESS_TIMEOUT = 60

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = application = Flask(__name__, static_folder=None)


# https://stackoverflow.com/a/4825933
class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            logging.info('Thread started')
            self.process = subprocess.Popen(self.cmd, shell=True)
            self.process.communicate()
            logging.info('Thread finished')

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            logging.info('Terminating process')
            self.process.terminate()
            thread.join()
        logging.info(self.process.returncode)

@app.route("/hooks", methods=["POST"])
def bb_webhooks_handler():
    router.route(request.headers["X-Event-Key"], request.json)
    return ("", 204)


@hooks.repo_push
def _handle_repo_push(event: event_schemas.RepoPush):
    logging.info(f"One or more commits pushed to: {event.repository.name}")
    repository_fullname = event.repository.full_name
    command = Command(f"./sync_repository_mirror.sh {repository_fullname}").run(SUBPROCESS_TIMEOUT)
