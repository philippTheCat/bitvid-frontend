from flask import Flask, render_template
from flask.ext.classy import FlaskView


app = Flask(__name__)


class IndexView(FlaskView):
    route_base = "/"

    def index(self):
        return render_template("index.html")

IndexView.register(app)

if __name__ == '__main__':
    app.run(port=8080, debug=True)