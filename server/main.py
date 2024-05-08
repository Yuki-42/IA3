"""
Main file for IA3 Project.
"""

# Standard Library Imports

# Third Party Imports
from flask import Flask
from flask_injector import FlaskInjector
from injector import Binder, singleton

# Local Imports
from internals.config import Config
from internals.routes import infoBlueprint, gamesBlueprint
from internals.wrapper.api import API

# Constants
config: Config = Config()

# Connect to the API
api: API = API(config)

# Create the Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")

# Add routes
app.register_blueprint(infoBlueprint)
app.register_blueprint(gamesBlueprint)


def configureDependencies(binder: Binder):
    """
    Configures the dependencies for the app.

    Args:
        binder (Binder): The binder to use.
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
        debug=config.server.debug
    )
