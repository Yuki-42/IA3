"""
Contains testBlueprint routes. Has urlPrefix of /tests.
"""
# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
from flask import request, render_template as flaskRenderTemplate
from flask.blueprints import Blueprint
from flask_injector import inject

# Internal Imports
from ..wrapper import API, Response

# Standard Library Imports

# Constants
testsBlueprint: Blueprint = Blueprint("tests", __name__, url_prefix="/tests")


class PageException(Exception):  # TODO: Move this to custom exceptions
    """
    Raised when a page related value is invalid.
    """

    def __init__(
            self,
            message: str
    ) -> None:
        """
        Initializes the PageException.

        Args:
            message (str): The message of the exception.
        """
        self.message: str = message

    def __str__(self) -> str:
        """
        Returns the message of the exception.

        Returns:
            str: The message of the exception.
        """
        return self.message


def renderTemplate(template: str, **kwargs) -> str:
    """
    Renders a template with the given arguments.

    Args:
        template (str): The template to render.
        **kwargs: The arguments to pass to the template.

    Returns:
        str: The rendered template.
    """
    # Extract the parent folder of the template.
    path: str = template.split("/")[0] if "/" in template else None
    return flaskRenderTemplate(
        f"tests/{template}",
        testType=path,
        **kwargs
    )


def pageAndPageSizeChecks(
        page: Any,
        pageSize: Any
) -> Tuple[int, int] | PageException:
    """
    Checks if the page and pageSize are valid.

    Args:
        page (Any): The page to check.
        pageSize (Any): The pageSize to check.

    Returns:
        Tuple[bool, Tuple[int, int] | None]: A tuple containing a boolean and a tuple of integers.
    """
    if page is None or pageSize is None:
        return PageException("`page` and `pageSize` are required.")

    # Convert the page and pageSize to integers.
    try:
        page: int = int(page)
        pageSize: int = int(pageSize)
    except ValueError:
        return PageException("`page` and `pageSize` must be integers.")

    if page < 1 or pageSize < 1:
        return PageException("`page` and `pageSize` must be greater than 0.")

    if pageSize >= 25:
        return PageException("<code>pageSize</code> must be less than or equal to 25.")

    return page, pageSize


def getRequestArguments(
        keys: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Gets the request arguments from the keys and attempts to parse them into desired types.

    Args:
        keys (List[Tuple[str, Any]]): The names of the request variables and their desired types.

    Returns:
        Dict[str, Any]: The request arguments.

    Raises:
        ValueError: If the request argument is not of the desired type.
    """
    # Get the request arguments.
    requestArguments: Dict[str, Any] = {}

    for key, type_ in keys:
        value: Any = request.args.get(key)
        if value is None:
            requestArguments[key] = None

        try:
            requestArguments[key]: type_ = type_(value)
        except ValueError:
            raise ValueError(f"`{key}` must be of type {type_}.")

    return requestArguments


# Routes
@testsBlueprint.get("/")
def index() -> str:
    """
    The tests page. Displays all modules available for testing.

    Returns:
        str: The rendered tests page.
    """
    return renderTemplate("index.html")


@testsBlueprint.get("/creator")
def creator() -> str:
    """
    The creator tests page.

    Returns:
        str: The rendered creator tests page.
    """
    return renderTemplate(
        "creator/index.html",
    )


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
        return renderTemplate("creator/index.html", error="Invalid test type.")

    # Get request parameters
    id: str = request.args.get("id")
    page: str = request.args.get("page")
    pageSize: str = request.args.get("pageSize")

    # If the test type is list, check if the page and pageSize are valid.
    if testType == "list":
        # Perform page checks.
        pageAndPageSize: Tuple[int, int] | PageException = pageAndPageSizeChecks(page, pageSize)

        if isinstance(pageAndPageSize, PageException):
            return renderTemplate("creator/index.html", error=pageAndPageSize.message)

        page, pageSize = pageAndPageSize

        # Get the creators from the API.
        response: Response = api.creator.list(page=page, pageSize=pageSize)
        return renderTemplate("creator/class.html", type=testType, creators=response.results)

    # Test type is details.
    if id is None:
        return renderTemplate("creator/index.html", error="`id` is required.")

    # Get the creator from the API.
    response: Response = api.creator.details(id=id)
    return renderTemplate("creator/class.html", type=testType, creator=response)


@testsBlueprint.get("/developer")
def developer() -> str:
    """
    The developer tests page.

    Returns:
        str: The rendered developer tests page.
    """
    return renderTemplate("developer/index.html")


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
        return renderTemplate("developer/index.html", error="Invalid test type.")

    # Get request parameters
    id: str = request.args.get("id")
    page: str = request.args.get("page")
    pageSize: str = request.args.get("pageSize")

    # If the test type is list, check if the page and pageSize are valid.
    if testType == "list":
        # Perform page checks.
        pageAndPageSize: Tuple[int, int] | PageException = pageAndPageSizeChecks(page, pageSize)

        if isinstance(pageAndPageSize, PageException):
            return renderTemplate("developer/index.html", error=pageAndPageSize.message)

        page, pageSize = pageAndPageSize

        # Get the developers from the API.
        response: Response = api.developer.list(page=page, pageSize=pageSize)
        return renderTemplate("developer/class.html", type=testType, developers=response.results)

    # Test type is details.
    if id is None:
        return renderTemplate("developer/index.html", error="`id` is required.")

    # Get the developer from the API.
    response: Response = api.developer.details(id=id)
    return renderTemplate("developer/class.html", type=testType, developer=response)


@testsBlueprint.get("/game")
def game() -> str:
    """
    The game tests page.

    Returns:
        str: The rendered game tests page.
    """
    return renderTemplate("game/index.html")


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
    match testType:
        case "list":
            # Get request parameters
            page: str = request.args.get("page")
            pageSize: str = request.args.get("pageSize")

            # Perform page checks.
            pageAndPageSize: Tuple[int, int] | PageException = pageAndPageSizeChecks(page, pageSize)

            if isinstance(pageAndPageSize, PageException):
                return renderTemplate("game/index.html", error=pageAndPageSize.message)

            # Get the games from the API.
            response: Response = api.game.list(**request.args)

            return renderTemplate("game/class.html", type=testType, games=response.results)

        case "dlcs":
            page: str = request.args.get("page")
            pageSize: str = request.args.get("pageSize")

            # Perform page checks.
            pageAndPageSize: Tuple[int, int] | PageException = pageAndPageSizeChecks(page, pageSize)

            if isinstance(pageAndPageSize, PageException):
                return renderTemplate("game/index.html", error=pageAndPageSize.message)

            page, pageSize = pageAndPageSize

            # Get the other request arguments.
            requestArguments: Dict[str, Any] = getRequestArguments(
                {
                    "id": str,
                }
            )

            # Get the dlcs from the API.
            response: Response = api.game.dlcs(requestArguments["id"], page=page, pageSize=pageSize)

            return renderTemplate("game/class.html", type=testType, dlcs=response.results)

        case _:
            return renderTemplate("game/index.html", error="Invalid test type.")


@testsBlueprint.get("/genre")
def genre() -> str:
    """
    The genre tests page.

    Returns:
        str: The rendered genre tests page.
    """
    return renderTemplate("genre/index.html")


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
    return renderTemplate("platform/index.html")


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
    return renderTemplate("publisher/index.html")


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
    return renderTemplate("store/index.html")


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
    return renderTemplate("tag/index.html")


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
