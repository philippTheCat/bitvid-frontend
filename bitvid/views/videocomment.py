# -*- coding: utf-8 -*-

from flask import flash, redirect, request, url_for, g
from flask.ext.classy import FlaskView

from bitvid import app


class VideoCommentView(FlaskView):
    def post(self):
        try:
            title = request.form["title"]
            content = request.form["content"]
            video = request.form["videoToken"]

            comment = g.api.video(video).comments.post(
                data={'title': title, 'content': content})

            if "message" in comment.keys():
                flash(comment["message"])
            else:
                flash("comment posted successfully")
        except Exception as ex:
            print ex
            flash("missing either title, description or videotoken")

        return redirect(url_for("VideoView:get", videoid=video))

VideoCommentView.register(app)
