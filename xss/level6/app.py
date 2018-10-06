from flask import Flask, render_template
from flask_csp.csp import csp_header
app = Flask(__name__)

@app.route("/", methods=['GET'])
@csp_header({
  "default-src": "'self'",
  "script-src": "'self' https://xss-game.appspot.com/static/game-frame.js",
  "img-src": "https://xss-game.appspot.com/static/level6_cube.png https://xss-game.appspot.com/static/logos/level6.png ",
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
 
if __name__ == "__main__":
    app.run(port=8080)