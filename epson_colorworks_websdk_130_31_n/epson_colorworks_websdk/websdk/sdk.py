#
# Epson Label Printer Web SDK
#
# Created by Seiko Epson Corporation on 2021/9/8.
# Copyright (C) 2021 Seiko Epson Corporation. All rights reserved.
#

from flask import Flask
from flask_cors import CORS
from api import api_bp
import os
import logging
import json


if os.geteuid() == 0 and os.getuid() == 0:
    raise PermissionError(
        "From security perspective, the SDK prevents to start as a root user's process."
        " If you want to start the SDK as a root user's process, please modify the sdk.py script on your responsibility."
    )


app = Flask(__name__)
app.register_blueprint(api_bp)

CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    with open('resources/productinfo.json', 'r') as f:
        productinfo = json.loads(f.read())
        app.logger.info(productinfo)
