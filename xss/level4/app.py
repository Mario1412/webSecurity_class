from flask import Flask, render_template, request, after_this_request
from flask_csp.csp import csp_header, create_csp_header
import hashlib

m = hashlib.sha256("hello")

app = Flask(__name__)


# generate random nonce
def generate_nonce():
    global m
    m.update("hello world")
    return m.hexdigest()


@app.route("/")
@csp_header({
    "default-src": "'self'",
    "script-src": "https://xss-game.appspot.com/static/game-frame.js ",
    "img-src": "https://xss-game.appspot.com/static/logos/level4.png",
    "style-src": "https://xss-game.appspot.com/static/game-frame-styles.css",
    "report-uri": ""
})
def index():
    return render_template('index.html')


@app.route('/check_timer_csp1', methods=['GET'])
@csp_header({
    "default-src": "'self'",
    "script-src": "'self' https://xss-game.appspot.com/static/game-frame.js",
    "img-src": "https://xss-game.appspot.com/static/logos/level4.png https://xss-game.appspot.com/static/loading.gif",
    "style-src": "https://xss-game.appspot.com/static/game-frame-styles.css",
    "report-uri": ""
})
def check_timer_csp1():
    timer_input = request.values.get('timer1')
    if timer_input:
        if timer_input.isdigit():
            return render_template('timer_csp1.html', timer=timer_input)
        else:
            return "Your input is invaild!"
    else:
        return render_template('index.html')


@app.route('/check_timer_csp2', methods=['GET'])
def check_timer_csp2():
    nonce = generate_nonce()
    csp_json = {"default-src": "'self'",
                "script-src": "'self' https://xss-game.appspot.com/static/game-frame.js 'nonce-" + nonce + "'",
                "img-src": "https://xss-game.appspot.com/static/logos/level4.png "
                           "https://xss-game.appspot.com/static/loading.gif",
                "style-src": "https://xss-game.appspot.com/static/game-frame-styles.css",
                "report-uri": ""
                }

    @after_this_request
    def add_header(response):
        response.headers['Content-Security-Policy'] = create_csp_header(csp_json)
        return response

    timer_input = request.values.get('timer2')
    if timer_input:
        if timer_input.isdigit():
            return render_template('timer_csp2.html', timer=timer_input, nonce=nonce)
        else:
            return "Your input is invaild!"
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(port=8080)
