# -*- coding: utf-8 -*-

from pprint import pprint

from flask import g, render_template, request
from flask.ext.classy import FlaskView

from bitvid import app
from bitvid.helpers import video_query


class VideoView(FlaskView):
    def index(self):
        query = request.args.get("q", "*")
        videos = video_query(query)

        return render_template("videolist.html", videos=videos)

    def get(self, id):
        video = video_query("token:" + id)[0]
        comments = g.client.getCommentsForVideo(id)
        pprint(video, indent=4)
        return render_template("video.html", video=video,
                               videoMedias=video["medias"], comments=comments)

VideoView.register(app)
