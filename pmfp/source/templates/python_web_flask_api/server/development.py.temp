def development(app: any, host: str, port: int)->None:
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[25],
                                      profile_dir="profile")
    app.run(host=host, port=port)


__all__ = ["development"]
