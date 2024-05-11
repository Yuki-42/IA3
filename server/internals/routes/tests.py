"""
Contains testBlueprint routes. Has urlPrefix of /tests.
"""
from flask import request
# Standard Library Imports

# Third Party Imports
from flask.blueprints import Blueprint
from flask_injector import inject

# Internal Imports
from ..helpers import renderTemplate
from ..wrapper import API, Response

# Constants
testsBlueprint: Blueprint = Blueprint("tests", __name__, url_prefix="/tests")


# Routes
@testsBlueprint.get("/")
def index() -> str:
    """
    The tests page. Displays all modules available for testing.

    Returns:
        str: The rendered tests page.
    """
    return renderTemplate("tests/index.html")


@testsBlueprint.get("/creator")
def creator() -> str:
    """
    The creator tests page.

    Returns:
        str: The rendered creator tests page.
    """
    return renderTemplate("tests/creator/index.html")


@testsBlueprint.get("/creator/<string:testType>")
@inject
def creatorClass(
        api: API,
        testType: str
) -> str:
    """
    The creator class tests page.

    Args:
        api (API): The API wrapper.
        testType (str): The type of test to run.

    Returns:
        str: The rendered creator class tests page.
    """
    if testType not in ["list", "details"]:
        return renderTemplate("tests/creator/index.html", error="Invalid test type.")

    # Get request parameters
    id: str = request.args.get("id")
    page: str = request.args.get("page")
    pageSize: str = request.args.get("pageSize")

    # If the test type is list, check if the page and pageSize are valid.
    if testType == "list":
        if page is None or pageSize is None:
            return renderTemplate(
                "tests/creator/index.html",
                error="`page` and `pageSize` are required."
            )

        # Convert the page and pageSize to integers.
        try:
            page: int = int(page)
            pageSize: int = int(pageSize)
        except ValueError:
            return renderTemplate(
                "tests/creator/index.html",
                error="`page` and `pageSize` must be integers."
            )

        if page < 1 or pageSize < 1:
            return renderTemplate(
                "tests/creator/index.html",
                error="`page` and `pageSize` must be greater than 0."
            )

        if pageSize >= 25:
            return renderTemplate(
                "tests/creator/index.html",
                error="<code>pageSize</code> must be less than or equal to 25."
            )

        # Get the creators from the API.
        response: Response = api.creator.getCreators(page=page, pageSize=pageSize)
        return renderTemplate("tests/creator/class.html", type=testType, creators=response.results)

    # Test type is details.
    if id is None:
        return renderTemplate("tests/creator/index.html", error="`id` is required.")

    # Get the creator from the API.
    response: Response = api.creator.getCreator(id=id)
    return renderTemplate("tests/creator/class.html", type=testType, creator=response)
