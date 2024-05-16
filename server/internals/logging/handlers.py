"""
Handlers for the logging system.
"""
# Standard Library Imports
from datetime import datetime
from logging import Handler, LogRecord
from os import getcwd
from pathlib import Path

# External Imports
from flask import Request, Response, g, has_request_context, request
from psycopg2 import connect as pgConnect
from psycopg2.extras import RealDictConnection, RealDictCursor, Json

# Local Imports
from ..config import Config


class DatabaseLogHandler(Handler):
    """
    A handler that logs all information to a sqlite database and periodically removes logs older than one week.
    """
    __slots__ = ("file", "connection", "includeRequest")

    def __init__(
            self,
            config: Config
    ) -> None:
        """
        Initializes the handler.

        Args:
            config (Config): The config object to use.
        """
        super().__init__()
        self.connection: RealDictConnection = pgConnect(
            dbname=config.logging.db.name,
            user=config.logging.db.username,
            password=config.logging.db.password,
            host=config.logging.db.host,
            port=config.logging.db.port,
            connection_factory=RealDictConnection
        )

        # Set includeRequest to False by default
        self.includeRequest: bool = False

    def __del__(self):
        """
        This method is called when the object is deleted.

        Returns:
            None
        """
        self.connection.close()
        del self

    def _createSchema(self) -> None:
        """
        Creates the schema for the database.

        Returns:
            None
        """
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            # Read the schema file
            with open(Path(f"{getcwd()}/internals/logging/schema.sql"), "r") as schemaFile:
                schema: str = schemaFile.read()

            # Execute the schema
            cursor.executemany(schema, None)

        self.connection.commit()

    def emit(
            self,
            record: LogRecord
    ) -> None:
        """
        Emits the log record to the sqlite database.

        Planning:
            Theoretically, this should have access to the request object, so it can log the request information.

        Args:
            record (LogRecord): The log record to emit.

        Returns:
            None
        """
        # # Log where the record is coming from
        # # print(f"Logging record from {record.filename}:{record.lineno}")
        # print(has_request_context())
        # # Testing code
        # if has_request_context() and not self.includeRequest:
        #     raise ValueError("Request information was logged without a request context.")
#
        # if ("request" in record.message or "response" in record.message) and (not has_request_context() or not self.includeRequest):
        #     raise ValueError("Request or response information was logged without a request context.")

        # Add the record to the database and get the id
        recordId: str = self._logRecord(record)

        if not has_request_context() or not self.includeRequest:
            print("ignoring request")
            return

        # Check what state the request is in
        if g.completed:
            self._logResponse(recordId, g.response)
        else:
            self._logRequest(recordId, request)

        self.connection.commit()

    def _logRecord(
            self,
            record: LogRecord
    ) -> str:
        """
        Logs the record to the database.

        Args:
            record (LogRecord): The record to log.

        Returns:
            str: The id of the record.
        """
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor: RealDictCursor
            cursor.execute(
                """
                INSERT INTO ia3.program_logs (
                    timestamp,
                    level,
                    filename,
                    funcname,
                    lineno,
                    message,
                    module,
                    name,
                    pathname,
                    process,
                    process_name,
                    thread,
                    thread_name
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) RETURNING id;
                """,
                (
                    datetime.fromtimestamp(record.created),
                    record.levelno,
                    record.filename,
                    record.funcName,
                    record.lineno,
                    record.msg,
                    record.module,
                    record.name,
                    record.pathname,
                    record.process,
                    record.processName,
                    record.thread,
                    record.threadName
                )
            )
            self.connection.commit()

            return cursor.fetchone()["id"]

    def _logRequest(
            self,
            recordId: str,
            _request: Request
    ) -> None:
        """
        Logs the request information to the database.

        Args:
            recordId (str): The id of the record to log the request information to. Used to link the request information
                to the log record.
            _request (request): The request object to log.

        Returns:
            None
        """
        # Check if the X-Forwarded-For header is present
        if "X-Forwarded-For" in _request.headers:
            remoteAddr = _request.headers["X-Forwarded-For"]
        else:
            remoteAddr = _request.remote_addr

        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO ia3.requests (
                    id, 
                    log_id, 
                    view_args, 
                    routing_exception, 
                    endpoint, 
                    blueprint, 
                    blueprints,
                    accept_languages, 
                    accept_mimetypes, 
                    access_route, 
                    args, 
                    "authorization", 
                    base_url, 
                    cookies, 
                    full_path, 
                    host, 
                    host_url, 
                    url, 
                    method, 
                    headers, 
                    remote_addr
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    recordId,
                    str(g.uuid),
                    Json(_request.view_args) if _request.view_args is not None else None,
                    _request.routing_exception.__str__() if _request.routing_exception is not None else None,
                    _request.endpoint if _request.endpoint is not None else None,
                    _request.blueprint if _request.blueprint is not None else None,
                    _request.blueprints if _request.blueprints is not None else None,
                    _request.accept_languages.__str__() if _request.accept_languages is not None else None,
                    _request.accept_mimetypes.__str__() if _request.accept_mimetypes is not None else None,
                    _request.access_route if _request.access_route is not None else None,
                    Json(_request.args.to_dict()) if _request.args is not None else None,
                    _request.authorization.__str__() if _request.authorization is not None else None,
                    _request.base_url if _request.base_url is not None else None,
                    Json(_request.cookies.to_dict()) if _request.cookies is not None else None,
                    _request.full_path if _request.full_path is not None else None,
                    _request.host if _request.host is not None else None,
                    _request.host_url if _request.host_url is not None else None,
                    _request.url if _request.url is not None else None,
                    _request.method if _request.method is not None else None,
                    _request.headers.__str__() if _request.headers is not None else None,
                    remoteAddr  # This will never be None
                )
            )
            self.connection.commit()

    def _logResponse(
            self,
            recordId: str,
            response: Response
    ) -> None:
        """
        Logs the response information to the database.

        Args:
            recordId (str): The id of the record to log the response information to. Used to link the response information
                to the log record.
            response (Response): The response object to log.

        Returns:
            None
        """
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO ia3.responses (
                    id, 
                    request_id, 
                    expires, 
                    location, 
                    status, 
                    status_code, 
                    headers, 
                    response
                ) VALUES  (
                    %s, %s, %s, %s, %s, %s, %s, %s
                );
                """,
                (
                    recordId,
                    str(g.uuid),
                    response.expires if response.expires is not None else None,
                    response.location if response.location is not None else None,
                    response.status if response.status is not None else None,
                    response.status_code if response.status_code is not None else None,
                    response.headers.__str__() if response.headers is not None else None,
                    response.response.__str__() if response.response is not None else None
                )
            )
            self.connection.commit()
