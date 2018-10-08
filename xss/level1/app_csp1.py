import cgi

import webapp2
import webapp2_static
from paste import httpserver

page_header = """
<!doctype html>
<html>
  <head>
    <!-- Internal game scripts/styles, mostly boring stuff -->
    <link rel="stylesheet" href="https://xss-game.appspot.com/static/game-frame-styles.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script> 
    <script src="static/level1.js"></script>
  </head>
 
  <body id="level1">
    <img src="https://xss-game.appspot.com/static/logos/level1.png">
      <div>
"""

page_footer = """
    </div>
   
  </body>
</html>
"""

main_page_markup = """
<form action="" method="GET">
  <input id="query" name="query" value="Enter query here..." />
  <input id="button" type="submit" value="Search" />
</form>
"""


class MainPage(webapp2.RequestHandler):

    def render_string(self, s):
        self.response.out.write(s)

    def get(self):
        # csp list note: I use sha256 to valid the inline script, which is not supported in csp1.0. If we use csp1.0,
        # we should move content of script tags into external file, and replace javascript: URLs and <a ...
        # onclick="[JAVASCRIPT]"> with appropriate addEventListener calls(
        # https://www.html5rocks.com/en/tutorials/security/content-security-policy/)
        csp_json = {
            "script-src": "https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js 'self'",
            "img-src": "https://xss-game.appspot.com/static/logos/level1.png",
            "default-src": "self",
            "style-src": "https://xss-game.appspot.com/static/game-frame-styles.css",
        }

        # Disable the reflected XSS filter for demonstration purposes
        self.response.headers.add_header("X-XSS-Protection", "0")
        # add csp policy to header
        # self.response.headers.add_header("Content-Security-Policy", create_csp_header(csp_json))

        if not self.request.get('query'):
            # Show main search page
            self.render_string(page_header + main_page_markup + page_footer)
        else:
            query = self.request.get('query', '[empty]')
            query = escapeHtml(query)
            # Our search engine broke, we found no results :-(
            message = "Sorry, no results were found for <b>" + query + "</b>."
            message += " <a href='?'>Try again</a>."

            # Display the results page
            self.render_string(page_header + message + page_footer)
        return


app = webapp2.WSGIApplication([
    (r'/', MainPage),
    (r'/static/(.+)', webapp2_static.StaticFileHandler)
], config={'webapp2_static.static_file_path': './static'})


def escapeHtml(html):
    return cgi.escape(html)


def main():
    httpserver.serve(app, host='127.0.0.1', port='8080')


if __name__ == '__main__':
    main()
