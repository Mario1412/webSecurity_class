from flask import Flask, render_template, request, flash

app = Flask(__name__)
from flask_csp.csp import csp_header


@app.route("/")
@csp_header({
    "default-src": "'self'",
    "script-src": "https://xss-game.appspot.com/static/game-frame.js ",
    "img-src": "https://xss-game.appspot.com/static/logos/level4.png",
    "object-src": "",
    "plugin-src": "",
    "style-src": "https://xss-game.appspot.com/static/game-frame-styles.css",
    "media-src": "",
    "child-src": "",
    "connect-src": "",
    "base-uri": "",
    "report-uri": ""
})
def index():
    return render_template('index.html')


@app.route('/check_timer', methods=['GET'])
@csp_header({
    "default-src": "'self'",
    "script-src": "'self' https://xss-game.appspot.com/static/game-frame.js",
    "img-src": "https://xss-game.appspot.com/static/logos/level4.png https://xss-game.appspot.com/static/loading.gif",
    "object-src": "",
    "plugin-src": "",
    "style-src": "https://xss-game.appspot.com/static/game-frame-styles.css",
    "media-src": "",
    "child-src": "",
    "connect-src": "",
    "base-uri": "",
    "report-uri": ""
})
def check_timer():
    print(request.values.get('timer'))
    timer_input = request.values.get('timer')
    if timer_input:
        if timer_input.isdigit():
            return render_template('timer.html', timer=timer_input)
        else:
            return "Your input is invaild!"
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(port=8080)
