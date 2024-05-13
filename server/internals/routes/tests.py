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
        response: Response = api.creator.list(page=page, pageSize=pageSize)
        return renderTemplate("tests/creator/class.html", type=testType, creators=response.results)

    # Test type is details.
    if id is None:
        return renderTemplate("tests/creator/index.html", error="`id` is required.")

    # Get the creator from the API.
    response: Response = api.creator.details(id=id)
    return renderTemplate("tests/creator/class.html", type=testType, creator=response)


@testsBlueprint.get("/developer")
def developer() -> str:
    """
    The developer tests page.

    Returns:
        str: The rendered developer tests page.
    """
    return renderTemplate("tests/developer/index.html")


@testsBlueprint.get("/developer/<string:testType>")
@inject
def developerClass(
        api: API,
        testType: str
) -> str:
    """
    The developer class tests page.

    Args:
        api (API): The API wrapper.
        testType (str): The type of test to run.

    Returns:
        str: The rendered developer class tests page.
    """
    if testType not in ["list", "details"]:
        return renderTemplate("tests/developer/index.html", error="Invalid test type.")

    # Get request parameters
    id: str = request.args.get("id")
    page: str = request.args.get("page")
    pageSize: str = request.args.get("pageSize")

    # If the test type is list, check if the page and pageSize are valid.
    if testType == "list":
        if page is None or pageSize is None:
            return renderTemplate(
                "tests/developer/index.html",
                error="`page` and `pageSize` are required."
            )

        # Convert the page and pageSize to integers.
        try:
            page: int = int(page)
            pageSize: int = int(pageSize)
        except ValueError:
            return renderTemplate(
                "tests/developer/index.html",
                error="`page` and `pageSize` must be integers."
            )

        if page < 1 or pageSize < 1:
            return renderTemplate(
                "tests/developer/index.html",
                error="`page` and `pageSize` must be greater than 0."
            )

        if pageSize >= 25:
            return renderTemplate(
                "tests/developer/index.html",
                error="<code>pageSize</code> must be less than or equal to 25."
            )

        # Get the developers from the API.
        response: Response = api.developer.list(page=page, pageSize=pageSize)
        return renderTemplate("tests/developer/class.html", type=testType, developers=response.results)

    # Test type is details.
    if id is None:
        return renderTemplate("tests/developer/index.html", error="`id` is required.")

    # Get the developer from the API.
    response: Response = api.developer.details(id=id)
    return renderTemplate("tests/developer/class.html", type=testType, developer=response)


@testsBlueprint.get("/game")
def game() -> str:
    """
    The game tests page.

    Returns:
        str: The rendered game tests page.
    """
    return renderTemplate("tests/game/index.html")


@testsBlueprint.get("/game/<string:testType>")
@inject
def gameClass(
        api: API,
        testType: str
) -> str:
    """
    The game class tests page.

    Args:
        api (API): The API wrapper.
        testType (str): The type of test to run.

    Returns:
        str: The rendered game class tests page.
    """
    raise NotImplementedError("Game tests are not implemented yet.")


@testsBlueprint.get("/genre")
def genre() -> str:
    """
    The genre tests page.

    Returns:
        str: The rendered genre tests page.
    """
    return renderTemplate("tests/genre/index.html")


@testsBlueprint.get("/genre/<string:testType>")
@inject
def genreClass(
        api: API,
        testType: str
) -> str:
    """
    The genre class tests page.

    Args:
        api (API): The API wrapper.
        testType (str): The type of test to run.

    Returns:
        str: The rendered genre class tests page.
    """
    raise NotImplementedError("Genre tests are not implemented yet.")


@testsBlueprint.get("/platform")
def platform() -> str:
    """
    The platform tests page.

    Returns:
        str: The rendered platform tests page.
    """
    return renderTemplate("tests/platform/index.html")


@testsBlueprint.get("/platform/<string:testType>")
@inject
def platformClass(
        api: API,
        testType: str
) -> str:
    """
    The platform class tests page.

    Args:
        api (API): The API wrapper.
        testType (str): The type of test to run.

    Returns:
        str: The rendered platform class tests page.
    """
    raise NotImplementedError("Platform tests are not implemented yet.")


@testsBlueprint.get("/publisher")
def publisher() -> str:
    """
    The publisher tests page.

    Returns:
        str: The rendered publisher tests page.
    """
    return renderTemplate("tests/publisher/index.html")


@testsBlueprint.get("/publisher/<string:testType>")
@inject
def publisherClass(
        api: API,
        testType: str
) -> str:
    """
    The publisher class tests page.

    Args:
        api (API): The API wrapper.
        testType (str): The type of test to run.

    Returns:
        str: The rendered publisher class tests page.
    """
    raise NotImplementedError("Publisher tests are not implemented yet.")


@testsBlueprint.get("/store")
def store() -> str:
    """
    The store tests page.

    Returns:
        str: The rendered store tests page.
    """
    return renderTemplate("tests/store/index.html")


@testsBlueprint.get("/store/<string:testType>")
@inject
def storeClass(
        api: API,
        testType: str
) -> str:
    """
    The store class tests page.

    Args:
        api (API): The API wrapper.
        testType (str): The type of test to run.

    Returns:
        str: The rendered store class tests page.
    """
    raise NotImplementedError("Store tests are not implemented yet.")


@testsBlueprint.get("/tag")
def tag() -> str:
    """
    The tag tests page.

    Returns:
        str: The rendered tag tests page.
    """
    return renderTemplate("tests/tag/index.html")


@testsBlueprint.get("/tag/<string:testType>")
@inject
def tagClass(
        api: API,
        testType: str
) -> str:
    """
    The tag class tests page.

    Args:
        api (API): The API wrapper.
        testType (str): The type of test to run.

    Returns:
        str: The rendered tag class tests page.
    """
    raise NotImplementedError("Tag tests are not implemented yet.")
