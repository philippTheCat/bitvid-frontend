# -*- coding: utf-8 -*-

from pprint import pprint

from flask import g, render_template, request
from flask.ext.classy import FlaskView

from bitvid import app
from bitvid.helpers import video_query


class VideoView(FlaskView):

    def index(self):
        query = request.args.get("q", "*")
        curpage = request.args.get("page", 0)
        pages, videos = video_query(query, page= curpage)

        return render_template("videolist.html", videos=videos, pages=pages, query=query)

    def get(self, videoid):
        video = video_query("token:" + videoid)[0]
        comments = g.client.getCommentsForVideo(videoid)
        pprint(video, indent=4)
        return render_template("video.html", video=video,
                               videoMedias=video["medias"], comments=comments)

VideoView.register(app)
