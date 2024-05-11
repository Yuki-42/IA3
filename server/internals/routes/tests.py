"""
Contains testBlueprint routes. Has urlPrefix of /tests.
"""

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


@testsBlueprint.get("/creator/<string:type>")
@inject
def creatorClass(
        api: API,
        testType: str = None,
        id: str = None,
        page: int = None,
        pageSize: int = None
) -> str:
    """
    The creator class tests page.

    Args:
        api (API): The API wrapper.
        testType (str): The type of test to run.
        id (str): The id of the creator.
        page (int): The page number.
        pageSize (int): The number of items per page.

    Returns:
        str: The rendered creator class tests page.
    """

    if testType not in ["list", "details"]:
        return renderTemplate("tests/creator/index.html", error="Invalid test type.")

    # If the test type is list, check if the page and pageSize are valid.
    if testType == "list":
        if page is None or pageSize is None:
            return renderTemplate(
                "tests/creator/index.html",
                error="<code>page</code> and <code>pageSize</code> are required."
            )

        if page < 1 or pageSize < 1:
            return renderTemplate(
                "tests/creator/index.html",
                error="<code>page</code> and <code>pageSize</code> must be greater than 0."
            )

        if pageSize >= 25:
            return renderTemplate(
                "tests/creator/index.html",
                error="<code>pageSize</code> must be less than or equal to 25."
            )

        # Get the creators from the API.
        response: Response = api.creator.getCreators(page=page, pageSize=pageSize)
        return renderTemplate("tests/creator/list.html", creators=response.results)

    # Test type is details.
    if id is None:
        return renderTemplate("tests/creator/index.html", error="<code>id</code> is required.")

    # Get the creator from the API.
    response: Response = api.creator.getCreator(id=id)
    return renderTemplate("tests/creator/details.html", creator=response)

