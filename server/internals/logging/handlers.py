"""
Handlers for the logging system.
"""
# Standard Library Imports
from logging import Handler, LogRecord
from os import getcwd
from pathlib import Path
from sqlite3 import connect, Cursor
from threading import Lock
from typing import List
from uuid import uuid4

# External Imports
from flask import request, g, has_request_context, Request, Response

# Constants
databaseLock: Lock = Lock()


class DatabaseLogHandler(Handler):
    """
    A handler that logs all information to a sqlite database and periodically removes logs older than one week.
    """
    __slots__ = ("file", "connection")

    def __init__(
            self,
            file: Path | str = None
    ) -> None:
        """
        Initializes the handler.

        Args:
            file (Path | str): The file to log to.
        """
        if file is None:
            file = Path(f"{getcwd()}/Logs/logs.db")  # Default to the logs.db file in the Logs directory
        super().__init__()
        self.file = file
        self.connection = connect(
            file,
            check_same_thread=False
        )
        cursor: Cursor = self.connection.cursor()

        # Get what tables are in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables: List = cursor.fetchall()

        # Check if tables is empty
        if not tables:
            self._createSchema()

        else:
            # Extract the table names
            tables = [table[0] for table in tables]

            # Check if the tables are in the database
            expected: List[str] = ["program_logs", "requests", "responses"]

            for table in expected:
                if table not in tables:
                    self._createSchema()
                    break

        # Close the cursor
        cursor.close()

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
        # Create the cursor
        cursor: Cursor = self.connection.cursor()

        # Read the schema file
        with open(Path(f"{getcwd()}/internals/logging/schema.sql"), "r") as schemaFile:
            schema: str = schemaFile.read()

        # Execute the schema
        cursor.executescript(schema)
        self.connection.commit()
        cursor.close()

    def emit(  # TODO: Convert this to use the request object, and e object to log the request information.
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
        """
        First log the base record to the database.
        """
        try:
            databaseLock.acquire()

            # Generate a uuid for the log record as a string
            recordId: str = str(uuid4())
            self._logRecord(recordId, record)

            if not has_request_context():
                return

            # Check what state the request is in
            if not g.completed:
                self._logRequest(recordId, request)

            else:
                self._logResponse(recordId, g.response)

        finally:
            databaseLock.release()

    def _logRecord(
            self,
            recordId: str,
            record: LogRecord
    ) -> None:
        """
        Logs the record to the database.

        Args:
            recordId (str): The id of the record to log.
            record (LogRecord): The record to log.

        Returns:
            None
        """
        cursor: Cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO program_logs (
                id,
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
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                recordId,
                record.created,
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
        cursor.close()

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
        cursor: Cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO requests (
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
                authorization, 
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
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                recordId,
                str(g.uuid),
                _request.view_args.__str__() if _request.view_args is not None else None,
                _request.routing_exception.__str__() if _request.routing_exception is not None else None,
                _request.endpoint if _request.endpoint is not None else None,
                _request.blueprint if _request.blueprint is not None else None,
                _request.blueprints.__str__() if _request.blueprints is not None else None,
                _request.accept_languages.__str__() if _request.accept_languages is not None else None,
                _request.accept_mimetypes.__str__() if _request.accept_mimetypes is not None else None,
                _request.access_route.__str__() if _request.access_route is not None else None,
                _request.args.__str__() if _request.args is not None else None,
                _request.authorization.__str__() if _request.authorization is not None else None,
                _request.base_url if _request.base_url is not None else None,
                _request.cookies.__str__() if _request.cookies is not None else None,
                _request.full_path if _request.full_path is not None else None,
                _request.host if _request.host is not None else None,
                _request.host_url if _request.host_url is not None else None,
                _request.url if _request.url is not None else None,
                _request.method if _request.method is not None else None,
                _request.headers.__str__() if _request.headers is not None else None,
                _request.remote_addr  # This will always be present
            )
        )

        self.connection.commit()
        cursor.close()

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
        cursor: Cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO responses (
                id, 
                request_id, 
                expires, 
                location, 
                status, 
                status_code, 
                headers, 
                response
            ) VALUES  (
                ?, ?, ?, ?, ?, ?, ?, ?
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
