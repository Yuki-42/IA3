"""
Contains miscellaneous helper functions.
"""

# Standard Library Imports
from datetime import datetime

# Third Party Imports
from flask import render_template as flaskRenderTemplate

# Internal Imports
from .config import Config


def renderTemplate(template: str, **kwargs) -> str:
    """
    Renders a template using Flask's render_template function while injecting items needed for `_base.html`.

    Args:
        template (str): The template to render.
        **kwargs: The keyword arguments to pass to the template.

    Returns:
        str: The rendered template.
    """
    return flaskRenderTemplate(
        template,
        year=datetime.now().year,
        **kwargs
    )
