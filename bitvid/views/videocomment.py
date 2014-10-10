# -*- coding: utf-8 -*-

from flask import flash, redirect, request, url_for
from flask.ext.classy import FlaskView

from bitvid import app


class VideoCommentView(FlaskView):
    def post(self):
        try:
            title = request.form["title"]
            content = request.form["content"]
            videotoken = request.form["videoToken"]
        except Exception as ex:
            print ex
            flash("missing either title, description or videotoken")

        comment = g.client.comment(title, content, videotoken)

        if "message" in comment.keys():
            flash(comment["message"])
        else:
            flash("comment posted successfully")

        return redirect(url_for("VideoView:get", videoid=videotoken))

VideoCommentView.register(app)
