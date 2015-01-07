# -*- coding: utf-8 -*-

import os

from flask import g, session
import tortilla

from bitvid import app


env = os.environ.get('BITVID_ENV', 'Dev')
app.config.from_object('config.{env}Config'.format(env=env))


# The ``views`` package has some built-in magic to load
# all the submodules.
from bitvid.views import *


@app.before_request
def before(*args, **kwargs):
    g.api = tortilla.wrap(app.config['API_URL'], debug=app.config['DEBUG'])
    if 'client_token' in session:
        g.api.headers.token = session['client_token']


@app.after_request
def after(response, **kwargs):
    session['client_token'] = g.api.headers.get('token')
    return response

application = app

if __name__ == '__main__':
    app.run(port=8080)
