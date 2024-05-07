"""
Main file for IA3 Project.
"""

# Standard Library Imports

# Third Party Imports
from flask import Flask

# Local Imports
from internals.config import Config
from server.internals.routes import info, games

# Constants
config: Config = Config()

# Create the Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")


# Add routes
app.register_blueprint(info)
app.register_blueprint(games)


# Run the app
if __name__ == "__main__":
    app.run(
        host=config.server.host,
        port=config.server.port,
        debug=config.server.debug
   )