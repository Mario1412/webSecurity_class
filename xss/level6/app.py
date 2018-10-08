from flask import Flask, render_template, after_this_request
from flask_csp.csp import csp_header, create_csp_header
import hashlib

m = hashlib.sha256("hello")

app = Flask(__name__)


# generate random nonce
def generate_nonce():
    global m
    m.update("hello world")
    return m.hexdigest()


@app.route("/csp1", methods=['GET'])
@csp_header({
    "default-src": "'self'",
    "script-src": "'self' https://xss-game.appspot.com/static/game-frame.js",
    "img-src": "https://xss-game.appspot.com/static/level6_cube.png "
               "https://xss-game.appspot.com/static/logos/level6.png ",
    "style-src": "https://xss-game.appspot.com/static/game-frame-styles.css",
    "report-uri": ""
})
def index_csp1():
    return render_template('index_csp1.html')


@app.route("/csp2", methods=['GET'])
def index_csp2():
    nonce = generate_nonce()
    csp_json = {"default-src": "'self'",
                "script-src": "'self' https://xss-game.appspot.com/static/game-frame.js 'nonce-" + nonce + "'",
                "img-src": "https://xss-game.appspot.com/static/level6_cube.png "
                           "https://xss-game.appspot.com/static/logos/level6.png ",
                "style-src": "https://xss-game.appspot.com/static/game-frame-styles.css",
                "report-uri": ""
                }

    @after_this_request
    def add_header(response):
        response.headers['Content-Security-Policy'] = create_csp_header(csp_json)
        return response

    return render_template('index_csp2.html', nonce=nonce)


if __name__ == "__main__":
    app.run(port=8080)
