from flask import Flask, render_template, session, request, flash, url_for, redirect
from flask.ext.classy import FlaskView, route

from client import HTTPClient
from pprint import pprint

app = Flask(__name__)


def buildVideoFromJson(json):
    resultset = []
    for video in json:
        #video["user"] = request.client.getUser(str(video["user_id"]))
        resultset.append(video)

    pprint(resultset,indent=4)
    return resultset


def getVideosForQuery(query):
    return buildVideoFromJson(request.client.search(query))


class IndexView(FlaskView):
    route_base = "/"

    def index(self):
        return render_template("index.html")


class AuthView(FlaskView):
    route_base = "/auth/"

    @route('/login', endpoint='AuthView:login_get', methods=["GET"])
    def login_get(self):
        return render_template("login.html")

    @route('/login', endpoint='AuthView:login_post', methods=["POST"])
    def login_post(self):
        user = request.form["username"]
        password = request.form["password"]

        try:
            success = request.client.authenticate(user, password)
        except:
            flash("could not login")
            return redirect(url_for("AuthView:login_get"))

        return redirect(url_for("IndexView:index"))

    @route('/register', endpoint='AuthView:register_get', methods=["GET"])
    def register_get(self):
        return render_template("register.html")

    @route('/register', endpoint='AuthView:register_post', methods=["POST"])
    def register_post(self):
        user = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]

        if password != password2:
            flash("passwords do not match")
            return render_template("register.html")

        try:
            success = request.client.register(user, password)
        except:
            flash("could not register")
            return redirect(url_for("AuthView:register_get"))

        return redirect(url_for("IndexView:index"))

    def logout(self):
        request.client.authtoken = None
        return redirect(url_for("IndexView:index"))


class UserView(FlaskView):
    def index(self):
        return render_template("user.html", user=request.client.getUser())

    def get(self, userid):
        return render_template("user.html", user=request.client.getUser(userid))


class VideoView(FlaskView):
    def index(self):
        videos = getVideosForQuery("*")

        return render_template("videolist.html",videos=videos)

    def get(self, videoid):
        return "video id"

    @route('/upload', endpoint='VideoView:upload_get', methods=["GET"])
    def upload_get(self):
        return render_template("video_upload.html")

    @route('/upload', endpoint='VideoView:upload_post', methods=["POST"])
    def upload_post(self):
        title = request.form["title"]
        description = request.form["description"]
        videotoken = request.client._getVideoToken(title,description)
        request.client.uploadVideo(videotoken, request.files["videofile"])
        return "uploading"

IndexView.register(app)
AuthView.register(app)
UserView.register(app)
VideoView.register(app)

@app.before_request
def before(*args, **kwargs):
    request.client = HTTPClient("http://localhost:5000")
    if "client_token" in session:
        request.client.authtoken = session["client_token"]


@app.after_request
def after(response, **kwargs):
    print response, kwargs
    session["client_token"] = request.client.authtoken

    return response
if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'  # TODO, change this
    app.run(port=8080, host="0.0.0.0", debug=True)
