from flask import render_template, Flask, request, after_this_request
from flask_csp.csp import create_csp_header
import re

app = Flask(__name__)
app.debug = True

csp_json = {
    "script-src": "'self' http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js "
                  "'sha256-cN25VmyGJVDLdpkS+JoZ3jMxtke1QdPN8mucaJj/2bc='",
    "img-src": "https://xss-game.appspot.com/static/logos/level5.png ",
    "default-src": "self",
    "style-src": "https://xss-game.appspot.com/static/game-frame-styles.css",
    "report-uri": "",
}


@app.route('/')
def index():
    return render_template('welcome.html')


@app.route('/signup', methods=['GET'])
def signup():
    next = str(request.values.get('next')).lower()
    if "javascript" in next:
        return render_template('hacker_fail.html')
    httpgroup = []
    try:
        httpgroup = re.match("^(http|https|ftp|pop|soap|dns|smtp)", next).groups()
    except AttributeError:
        pass
    if httpgroup:
        return render_template('hacker_fail.html')
    return render_template('signup.html', next=next)
    # If we are sure that the next step will get into specified page, we can directly write the code which in the
    # case is "confirm.html", which allow us do nothing for handling over the vulnerability. But I think this
    # question is very tricky and the I guess professor require us to write some code to handle over the specified
    # injection vulnerability. return render_template('signup.html', next="confirm.html")


@app.route('/confirm_csp2', methods=['GET'])
def confirm():
    return render_template('confirm_csp2.html')


@app.route('/confirm_csp1', methods=['GET'])
def confirm_csp1():
    @after_this_request
    def add_header(response):
        csp_json['script-src'] = "'self' http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js "
        response.headers['Content-Security-Policy'] = create_csp_header(csp_json)
        return response
    return render_template('confirm_csp1.html')


# When using this interceptor, I set every content-security-policy. So with this method, I don't waste time write
# csp_header on every request url
@app.after_request
def after_request_interceptor(response):
    response.headers['Content-Security-Policy'] = create_csp_header(csp_json)
    return response


@app.errorhandler(Exception)
def page_not_found(e):
    return render_template('welcome.html')


# Starting up our Flask Server (helps us run the application)
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
