__all__=['testing']
from gevent.wsgi import WSGIServer

def testing(app:any,host:str,port:int)->None:
    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()
