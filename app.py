# -*- coding: utf-8 -*-

import os

from flask import g, session

from bitvid import app
from bitvid.client import BitvidClient

env = os.environ.get('BITVID_ENV', 'Dev')
app.config.from_object('config.{env}Config'.format(env=env))


# The ``views`` package has some built-in magic to load
# all the submodules.
from bitvid.views import *


@app.before_request
def before(*args, **kwargs):
    g.client = BitvidClient(app.config["API_URL"], debug=True)
    if "client_token" in session:
        g.client.authtoken = session["client_token"]


@app.after_request
def after(response, **kwargs):
    print response, kwargs
    session["client_token"] = g.client.authtoken
    return response


if __name__ == '__main__':
    app.run(port=8080)
