# -*- coding: utf-8 -*-

from flask import flash, g, redirect, request, render_template, url_for
from flask.ext.classy import FlaskView

from bitvid import app
import traceback

class RegisterView(FlaskView):
    route_base = "/auth/register"

    def get(self):
        return render_template("register.html")

    def post(self):
        user = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password2 = request.form["password2"]

        if password != password2:
            flash("passwords do not match")
            return render_template("register.html")

        try:
            success = g.api.user.post(data={
                'name': user, 'password': password, 'email': email})
        except Exception as e:
            traceback.print_exc(e)
            flash("could not register")
            return redirect(url_for("RegisterView:get"))

        if "message" in success.keys():
            print "success", success
            flash(success["message"])
            return redirect(url_for("RegisterView:get"))

        return redirect(url_for("IndexView:index"))

RegisterView.register(app)
