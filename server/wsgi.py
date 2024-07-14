"""
WSGI entrypoint for the application.
"""

from main import app, config

if __name__ == "__main__":
    app.run(
        host=config.server.host,
        port=config.server.port,
        debug=config.server.debug,
        ssl_context=(config.server.ssl.cert, config.server.ssl.key) if config.server.ssl.enabled else None
    )
