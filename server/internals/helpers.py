"""
Contains miscellaneous helper functions.
"""

# Standard Library Imports
from datetime import datetime
from typing import Any, Dict

# Third Party Imports
from flask import render_template as flaskRenderTemplate
from pydantic import BaseModel

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


def convertIfNeeded(
        value: Any
) -> str | int | float | bool | None:
    """
    Converts a pydantic model to a standard Python value. If a value is not a pydantic model, it is returned as is.

    Args:
        value (Any): The value to convert.

    Returns:
        str | int | float | bool | None: The converted value.
    """
    if not isinstance(value, BaseModel):
        return value

    # Get either the id or slug of the model.
    if hasattr(value, "id"):
        return value.id
    elif hasattr(value, "slug"):
        return value.slug

    return None


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
    # Iterate through the parameters and add them to the base dictionary if they are not None.
    for key, value in parameters.items():
        if value is None:
            continue

        # If the value is a list, join it with commas.
        if isinstance(value, list):
            value = ",".join(convertIfNeeded(item) for item in value)

        base[key] = convertIfNeeded(value)

    return base
