"""
Main file for IA3 Project.
"""

# Standard Library Imports
from base64 import b64decode
from os import chdir, getcwd
from typing import List
from uuid import uuid4
from logging import getLogger

# Third Party Imports
from flask import Flask, g, request, Response
from flask_injector import FlaskInjector
from injector import Binder, singleton

# Local Imports
from internals.config import Config
from internals.logging import SuppressedLoggerAdapter, createLogger
from internals.routes import *
from internals.wrapper.api import API

# Constants
EXPECTED_COOKIES: List[str] = ["theme"]

# Before we do anything, check if the working directory is correct. This is a fix for running the server from parent directory using the start script.
if not getcwd().endswith("server"):
    chdir("server")

# Constants
config: Config = Config()

# Create the logger
logger: SuppressedLoggerAdapter = createLogger(
    "endpoints",
    level=config.logging.level,
    includeRequest=True
)

# Kill the standard werkzeug logger
werkzeugLogger = getLogger("werkzeug")
werkzeugLogger.disabled = config.logging.disableWerkzeug

# Connect to the API
api: API = API(config)

# Add a workaround for a bug in FlaskInjector
Flask.url_for.__annotations__ = {}

# Create the Flask app
app: Flask = Flask(__name__, static_folder="static", template_folder="templates")

# Set static and template folders
app.static_folder = "static"
app.template_folder = "templates"

# Add routes
app.register_blueprint(infoBlueprint)
app.register_blueprint(gamesBlueprint)
app.register_blueprint(testsBlueprint)
app.register_blueprint(apiBlueprint)
app.register_blueprint(errorsBlueprint)


@app.before_request
def beforeRequest() -> Response | None:
    """
    Runs before each request. Ensures that the user is logged in.

    If the user is not logged in, respond with a 401 error code.

    Returns:
        None
    """
    # Set request uuid
    g.uuid = uuid4()
    g.completed = False
    logger.info(  # 2 spaces here to match the indentation of the response log
        f"Request  [{g.uuid}] [{request.method}] [{request.path}] from {request.remote_addr} with user agent {request.user_agent} with cookies {request.cookies}"
    )

    # Check if the request is for static
    if request.path == "/static/css/_colours.css" and request.method == "GET":
        # Return the correct colour css file based on the theme
        return app.send_static_file(f"css/{request.cookies.get("theme", config.server.defaultTheme)}_colours.css")

    # Check if the request is coming from the server or is from one of the development machines
    if request.remote_addr == config.server.host or (request.remote_addr in ["192.168.0.223"] and config.server.debug):
        # Continue to route
        return

    fail: Response = Response(
        "Unauthorized",
        headers={"WWW-Authenticate": "Basic realm='Login Required.'"},
        status=401
    )

    if "Authorization" not in request.headers:
        return fail

    # Decode the authorization header and check if it is correct

    username, password = b64decode(request.headers["Authorization"].split(" ")[1]).decode("utf-8").split(":")

    if password != config.server.password or username != config.server.username:
        return fail

    pass


@app.after_request
def afterRequest(
        response: Response
) -> Response:
    """
    Runs after each request. Logs the response and deals with cookies.

    Args:
        response (Response): The response to log.

    Returns:
        Response: The response.
    """
    g.completed = True
    g.response = response
    logger.info(f"Response [{g.uuid}] [{response.status_code}]")
    # Add a theme cookie to the response if the user doesn't have one
    if "theme" not in request.cookies:
        response.set_cookie("theme", config.server.defaultTheme)

    # Purge any cookies that are not expected
    for cookie in request.cookies:
        if cookie not in EXPECTED_COOKIES:
            response.delete_cookie(cookie)

    return response


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


def getHosts(names: List[str]) -> List[str]:
    """
    Converts a list of IP addresses and domains to valid urls.

    Args:
        names (List[str]): A list of IP addresses and domains to convert to urls.

    Returns:
        List[str]: A list of all the hostnames of the machine.
    """
    return [f"{"https" if config.server.ssl else "http"}://{name}:{config.server.port}" for name in names]


# Add dependencies
FlaskInjector(app=app, modules=[configureDependencies])

# Run the app
if __name__ == "__main__":
    # Construct a list of host addresses
    ips: List[str] = [config.server.publicHost, config.server.host]
    hostAddresses: List[str] = getHosts(ips)
    # Log the start of the server including what address and port it is running on
    logger.info(f"Server started on following addresses: {", \n".join(hostAddresses)}")

    app.run(
        host=config.server.host,
        port=config.server.port,
        debug=config.server.debug,
        ssl_context=(config.server.ssl.cert, config.server.ssl.key) if config.server.ssl.enabled else None
    )
