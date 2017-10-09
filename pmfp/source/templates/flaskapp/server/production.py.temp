__all__ = ["production"]
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

def production(app:any,host:str,port:int)->None:
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(port,host)
    IOLoop.instance().start()
