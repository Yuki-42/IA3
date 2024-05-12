"""
Contains miscellaneous helper functions.
"""

# Standard Library Imports
from datetime import datetime
from typing import Any, Dict

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


def addParameters(
        base: Dict[str, Any],
        parameters: Dict[str, Any | None]
) -> Dict[str, Any]:
    """
    Adds parameters to a base dictionary.

    Args:
        base (Dict[str, Any]): The base dictionary.
        parameters (Dict[str, Any | None]): The parameters to add.

    Returns:
        Dict[str, Any]: The base dictionary with the parameters added.
    """
    for key, value in parameters.items():
        if value is not None:
            base[key] = value

    return base
