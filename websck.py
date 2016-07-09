import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print "new connection"

    def on_message(self, message):
        print "message received: %s" % message
        print "sending back message: %s" % message[::-1]
        self.write_message(message[::-1])

    def on_close(self):
        print "Connection Closed"

    def check_origin(self, origin):
        return True

 application = tornado.web.Application([
     (r'/ws', WSHandler),
     ])

 if __name__ == "__main__":
     http_server = tornado.httpserver.HTTPServer(application)
     http_server.listen(8888)
     myIP = socket.gethostbyname(socket.gethostname())
     tornado.ioloop.IOLoop.instance().start()
     
