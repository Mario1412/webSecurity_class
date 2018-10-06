from flask import render_template, Flask
from flask_csp.csp import csp_header

app = Flask(__name__)
app.debug = True


@app.route('/')
@csp_header({'script-src': "'self' http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js",
             "img-src": "https://xss-game.appspot.com/static/logos/level3.png "
                        "https://xss-game.appspot.com/static/level3/cloud1.jpg "
                        "https://xss-game.appspot.com/static/level3/cloud2.jpg "
                        "https://xss-game.appspot.com/static/level3/cloud3.jpg",
             "style-src": "https://xss-game.appspot.com/static/game-frame-styles.css",
             "report-uri": ""})
def index():
    return render_template('index.html')


# Starting up our Flask Server (helps us run the application)
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
