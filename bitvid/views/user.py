# -*- coding: utf-8 -*-

from flask import g, render_template, flash, redirect, url_for
from flask.ext.classy import FlaskView

from bitvid import app
from bitvid.forms.Userforms import ChangePassword

class UserView(FlaskView):
    def index(self):
        return render_template("user.html", user=g.client.get_user())

    def get(self, userid):
        return render_template("user.html", user=g.client.get_user(userid))


class UserPasswordView(FlaskView):
    route_base = "/user/password"

    def get(self):
        form = ChangePassword()

        return render_template("change_password.html", form=form)

    def post(self):
        form = ChangePassword()

        if form.validate_on_submit():
            user = g.client.get_user()

            if "message" in user.keys():
                flash(user["message"])
                return render_template("change_password.html", form=form)

            email = user ["email"]

            res = g.client.changePassword(email,form.old_password.raw_data[0], form.password.raw_data[0])

            if "message" in res.keys():
                flash(res["message"])
                return render_template("change_password.html", form=form)

            return redirect(url_for("UserView:index"))

        return render_template("change_password.html", form=form)




UserView.register(app)
UserPasswordView.register(app)