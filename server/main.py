"""
Main file for IA3 Project.
"""

# Standard Library Imports
from base64 import b64decode

# Third Party Imports
from flask import Flask, session, request, redirect, url_for as flaskUrlFor
from flask_injector import FlaskInjector
from injector import Binder, singleton
from werkzeug import Response

# Local Imports
from internals.config import Config
from internals.logging import createLogger, EndpointLoggerAdapter
from internals.routes import *
from internals.wrapper.api import API

# Constants
config: Config = Config()

# Create the logger
logger: EndpointLoggerAdapter = createLogger("endpoints", level=config.logging.level, adapterMode=EndpointLoggerAdapter)

# Connect to the API
api: API = API(config)

# Add a workaround for a bug in FlaskInjector
Flask.url_for.__annotations__ = {}

# Create the Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")

# Add routes
app.register_blueprint(infoBlueprint)
app.register_blueprint(gamesBlueprint)
app.register_blueprint(testsBlueprint)
app.register_blueprint(apiBlueprint)


@app.before_request
def beforeRequest() -> Response | None:
    """
    Runs before each request. Ensures that the user is logged in.

    If the user is not logged in, respond with a 401 error code.

    Returns:
        None
    """
    logger.logRequest(request)
    if request.remote_addr == config.server.host:
        return None

    fail: Response = Response(
        "Unauthorized",
        headers={"WWW-Authenticate": "Basic realm='Login Required. Username is ignored.'"},
        status=401
    )

    if "Authorization" not in request.headers:
        return fail

    # Decode the authorization header and check if it is correct

    username, password = b64decode(request.headers["Authorization"].split(" ")[1]).decode("utf-8").split(":")

    if password != config.server.password or username != config.server.username:
        return fail

    pass


def configureDependencies(
        binder: Binder
) -> None:
    """
    Configures the dependencies for the app.

    Args:
        binder (Binder): The binder to use.

    Returns:
        None
    """
    binder.bind(Config, config, scope=singleton)
    binder.bind(API, api, scope=singleton)


# Add dependencies
FlaskInjector(app=app, modules=[configureDependencies])

# Run the app
if __name__ == "__main__":
    app.run(
        host=config.server.host,
        port=config.server.port,
        debug=config.server.debug,
        ssl_context=(config.server.cert, config.server.key) if config.server.ssl else None
    )
