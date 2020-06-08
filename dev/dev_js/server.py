# https://opensource.com/article/18/6/tornado-framework
# https://stackoverflow.com/questions/6131915/web-sockets-tornado-notify-client-on-database-update

# __init__.py
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application

define('port', default=9000, help='port to listen on')

def main():
    """Construct and serve the tornado application."""
    app = Application()
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()