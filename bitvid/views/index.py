# -*- coding: utf-8 -*-

from flask import redirect, render_template, url_for
from flask.ext.classy import FlaskView

from bitvid import app


class IndexView(FlaskView):
    route_base = '/'

    def index(self):
        return redirect(url_for('VideoView:index'))

IndexView.register(app)
