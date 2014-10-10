# -*- coding: utf-8 -*-

from flask import g, render_template
from flask.ext.classy import FlaskView

from bitvid import app


class UserView(FlaskView):
    def index(self):
        return render_template("user.html", user=g.client.getUser())

    def get(self, userid):
        return render_template("user.html", user=g.client.getUser(userid))

UserView.register(app)
