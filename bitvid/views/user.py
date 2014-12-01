# -*- coding: utf-8 -*-

from flask import g, render_template, flash, redirect, url_for, request
from flask.ext.classy import FlaskView

from bitvid import app
from bitvid.helpers import video_query
from bitvid.forms.Userforms import ChangePassword

class UserView(FlaskView):
    def index(self):
        return self.get('current')

    def get(self, userid):
        user = g.api.user.get(userid)
        query = "user_id:{}".format(user.id)
        curpage = request.args.get("page", 0)
        query_result = video_query(query, page= curpage)

        pages, videos = 1, {}
        if len(query_result) == 2:
            pages, videos = query_result

        return render_template("user.html", user=user, videos=videos, pages=pages)


class UserPasswordView(FlaskView):
    route_base = "/user/password"

    def get(self):
        form = ChangePassword()

        return render_template("change_password.html", form=form)

    def post(self):
        form = ChangePassword()

        if form.validate_on_submit():
            user = g.api.user.get('current')

            if "message" in user.keys():
                flash(user["message"])
                return render_template("change_password.html", form=form)

            name = user ["name"]

            res = g.client.changePassword(name,form.old_password.raw_data[0], form.password.raw_data[0])

            if "message" in res.keys():
                flash(res["message"])
                return render_template("change_password.html", form=form)

            return redirect(url_for("UserView:index"))

        return render_template("change_password.html", form=form)




UserView.register(app)
UserPasswordView.register(app)
