from flask import render_template, Flask, after_this_request
from flask_csp.csp import csp_header, create_csp_header
import hashlib

m = hashlib.sha256("hello")

app = Flask(__name__)
app.debug = True


# generate random nonce
def generate_nonce():
    global m
    m.update("hello world")
    return m.hexdigest()


@app.route('/csp1')
@csp_header({'script-src': "'self' http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js",
             "img-src": "https://xss-game.appspot.com/static/logos/level3.png "
                        "https://xss-game.appspot.com/static/level3/cloud1.jpg "
                        "https://xss-game.appspot.com/static/level3/cloud2.jpg "
                        "https://xss-game.appspot.com/static/level3/cloud3.jpg",
             "style-src": "https://xss-game.appspot.com/static/game-frame-styles.css",
             "report-uri": ""})
def index_csp1():
    return render_template('index_csp1.html')


@app.route('/csp2')
def index_csp2():
    nonce = generate_nonce()
    csp_json = {'script-src': "'self' http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js "
                              "'nonce-" + nonce + "'",
                "img-src": "https://xss-game.appspot.com/static/logos/level3.png "
                           "https://xss-game.appspot.com/static/level3/cloud1.jpg "
                           "https://xss-game.appspot.com/static/level3/cloud2.jpg "
                           "https://xss-game.appspot.com/static/level3/cloud3.jpg",
                "style-src": "https://xss-game.appspot.com/static/game-frame-styles.css",
                "report-uri": ""
                }

    @after_this_request
    def add_header(response):
        response.headers['Content-Security-Policy'] = create_csp_header(csp_json)
        return response

    return render_template('index_csp2.html', nonce=nonce)


# Starting up our Flask Server (helps us run the application)
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
