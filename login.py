import os
import tornado.ioloop
import tornado.web
import tornado.websocket

class BaseHandler(tornado.web.RequestHandler):
    def get_login_url(self):
        return u"/login"

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None

class LoginHandler(BaseHandler):
    def get(self):
        self.render("static/login.html", next=self.get_argument("next", "/"), message=self.get_argument("error", ""))

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        if (username == "adnan") and (password == "adnan"):
            auth = True
        else:
            auth = False
            
        if auth:
            self.set_current_user(username)
            self.redirect(self.get_argument("next", u"/"))
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect.")
            self.redirect(u"/login" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(u"/login")
        
def startwebserver(port):
    print "Starting Webserver on port: " + str(port)
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "NWmYRHeORYacNbUYsDVoUKAKLylF80XluWXnuUH7FBo=",
    }
    application = tornado.web.Application([
        (r"/", BaseHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/jquery.min.js", tornado.web.StaticFileHandler,
         dict(path=settings['static_path']))
        ], **settings)
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    startwebserver(8889)
