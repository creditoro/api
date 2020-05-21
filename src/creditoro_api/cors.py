"""
This module is used as middleware to inject CORS headers.
"""


class Cors:
    """Cors.
    """
    def __init__(self, app=None, **kwargs):
        """__init__.

        Args:
            app:
            kwargs:
        """
        self._options = kwargs
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **_):
        """init_app.

        Args:
            app:
            _:
        """
        @app.after_request
        def after_request(response):
            """after_request.

            Args:
                response:
            """
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers[
                "Access-Control-Allow-Origin"] = "https://api.creditoro.nymann.dev"
            response.headers[
                "Access-Control-Allow-Headers"] = "Authorization,Content-Type"
            response.headers[
                "Access-Control-Allow-Methods"] = "GET,POST,OPTIONS,PUT,DELETE,PATCH"
            return response
