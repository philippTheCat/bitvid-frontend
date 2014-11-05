# -*- coding: utf-8 -*-

from pprint import pprint

from flask import g, render_template, request, flash, redirect, url_for
from flask.ext.classy import FlaskView

from bitvid import app
from bitvid.helpers import video_query


class VideoView(FlaskView):

    def index(self):
        query = request.args.get("q", "*")
        curpage = request.args.get("page", 0)
        query_result = video_query(query, page= curpage)

        pages, videos = 1, {}
        if len(query_result) == 2:
            pages, videos = query_result

        return render_template("videolist.html", videos=videos, pages=pages, query=query)

    def get(self, videoid):
        try:
            video = video_query("token:" + videoid)[1][0]
            comments = g.client.getCommentsForVideo(videoid)
            pprint(video, indent=4)
            return render_template("video.html", video=video,
                                   videoMedias=video["medias"], comments=comments)
        except Exception as e:
            flash("failed to load video")
            print e
            return redirect(app.config["HOST"] + url_for('VideoView:index'))

VideoView.register(app)
