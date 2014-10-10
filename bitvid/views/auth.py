# -*- coding: utf-8 -*-

from flask import flash, g, redirect, request, render_template, url_for
from flask.ext.classy import FlaskView, route

from bitvid import app


class AuthView(FlaskView):
    route_base = "/auth/"

    def get(self):
        return render_template("login.html")

    def post(self):
        user = request.form["username"]
        password = request.form["password"]

        try:
            success = g.client.authenticate(user, password)
        except:
            flash("could not login")
            return redirect(url_for("AuthView:get"))

        if "message" in success.keys():
            print "success", success
            flash(success["message"])
            return redirect(url_for("AuthView:get"))

        return redirect(url_for("IndexView:index"))

    @route("/logout", methods=["GET"])  # TODO, make this POST
    def logout(self):
        g.client.authtoken = None
        return redirect(url_for("IndexView:index"))

AuthView.register(app)
