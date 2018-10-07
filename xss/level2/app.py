from flask import Flask, render_template
from flask_csp.csp import csp_header

app = Flask(__name__)


@app.route("/")
@csp_header({
    "default-src": "'self'",
    "script-src": "'self' https://xss-game.appspot.com/static/post-store.js",
    "img-src": "https://xss-game.appspot.com/static/logos/level2.png "
               "https://xss-game.appspot.com/static/level2_icon.png "
               "https://ssl.gstatic.com/s2/oz/images/sprites/stream-e001443aa61c5529c1aa133a9c12bb49.png",
    "style-src": "https://xss-game.appspot.com/static/game-frame-styles.css"
})
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=8080)
