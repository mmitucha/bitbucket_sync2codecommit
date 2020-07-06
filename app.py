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
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = application = Flask(__name__, static_folder=None)


def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            logging.info(output.strip())
    rc = process.poll()
    return rc


@app.route("/hooks", methods=["POST"])
def bb_webhooks_handler():
    router.route(request.headers["X-Event-Key"], request.json)
    return ("", 204)


@hooks.repo_push
def _handle_repo_push(event: event_schemas.RepoPush):
    logging.info(f"One or more commits pushed to: {event.repository.name}")
    repository_fullname = event.repository.full_name
    run_command(f"./sync_repository_mirror.sh {repository_fullname}")
