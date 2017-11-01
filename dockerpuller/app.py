#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

import click
import subprocess

import logging
from flask import Flask
from flask import request
from flask import jsonify
from slack_logger import SlackHandler, SlackFormatter

__version__ = '0.0.19'


app = Flask(__name__)
config = None

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

sh = SlackHandler(username='Celery', icon_emoji=':robot_face:', url=os.environ["SLACK_API_TOKEN"])
sh.setLevel(logging.DEBUG)

f = SlackFormatter()
sh.setFormatter(f)
logger.addHandler(sh)

@app.route("/")
def main():
    return 'API Version %s' % __version__

@app.route("/<token>/<hook>", methods=['POST'])
def hook_listen(token, hook):
    print "received %s" % request.data
    logger.info('Se inicio el deploy '.format(request.data))
    if token != config['token']:
        logger.error("Error con el deploy (Token inválido)")
        return jsonify(success=False, error="Invalid token"), 403

    hook_value = config['hooks'].get(hook)

    if hook_value is None:
        return jsonify(success=False, error="Hook not found"), 404

    try:
        subprocess.call([hook_value, request.remote_addr])
        logger.info('Se ejecuto exitosamente el deploy ')
        return jsonify(success=True, version=__version__), 200

    except OSError as e:
        return jsonify(success=False, error=str(e)), 400


def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)

    
@click.option('--version', help='Print Version and exit',
              is_flag=True)
@click.option('--debug', help='Enable debug option',
              is_flag=True)

@click.command()
def cli(debug, version):
    if version:
        click.echo(__version__)
        exit()

    app.run(
        host=config.get('host', 'localhost'),
        port=config.get('port', 8000), debug=debug
    )

config = load_config()
    
if __name__ == "__main__":
    cli()
