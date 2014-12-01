# -*- coding: utf-8 -*-

import time

from flask import flash, g, redirect, request, render_template, url_for
from flask.ext.classy import FlaskView

from bitvid import app
from bitvid.helpers import video_query


class VideoUploadView(FlaskView):
    route_base = '/video/upload'

    def get(self):
        return render_template("video_upload.html")

    def post(self):
        title = request.form["title"]
        description = request.form["description"]
        video = g.client._getVideoToken(title, description)
        if "message" in video.keys():
            flash(video["message"])
            return redirect(url_for("VideoUploadView:get"))
        uploaddata = g.client.uploadVideo(video["token"],
                                          request.files["videofile"])

        if "message" in uploaddata.keys():
            print "uploaddata", uploaddata
            flash(uploaddata["message"])
            g.api.video.delete(video['token'])
            return redirect(url_for("VideoUploadView:get"))

        count = 20
        while count > 0:
            count -= 1
            time.sleep(0.1)
            try:
                video_query("token:" + video["token"])[0]
                break
            except:
                pass
                # god is this ugly. waiting for the video to get indexed..

        return redirect(app.config["HOST"] + url_for('VideoView:get',
                                                     videoid=video["token"]))

VideoUploadView.register(app)
