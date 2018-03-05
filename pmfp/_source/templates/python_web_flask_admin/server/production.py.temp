from gevent.wsgi import WSGIServer


def production(app: any, host: str, port: int)->None:
    from gevent import monkey; monkey.patch_all()
    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()


__all__ = ["production"]
