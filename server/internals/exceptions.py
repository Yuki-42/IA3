"""
Contains all custom exceptions for the project
"""


class DatabaseError(Exception):
    """
    Base class for all database exceptions.
    """
    pass


class DatabaseIntegrityError(DatabaseError):
    """
    Raised when a database integrity error occurs.
    """
    pass


class ChannelError(DatabaseError):
    """
    Base class for all channel exceptions.
    """
    pass


class ChannelNotFoundError(ChannelError):
    """
    Raised when a channel is not found.
    """
    pass


class ChannelExistsError(ChannelError):
    """
    Raised when a channel already exists.
    """
    pass


class ImageError(DatabaseError):
    """
    Base class for all image exceptions.
    """
    pass


class ImageNotFoundError(ImageError):
    """
    Raised when an image is not found.
    """
    pass


class ImageExistsError(ImageError):
    """
    Raised when an image already exists.
    """
    pass


class UserError(DatabaseError):
    """
    Base class for all author exceptions.
    """
    pass


class UserNotFoundError(UserError):
    """
    Raised when a author is not found.
    """
    pass


class UserExistsError(UserError):
    """
    Raised when a author already exists.
    """
    pass


class UserNotApproved(UserError):
    """
    Raised when a author is not verified.
    """
    pass


class MessageError(DatabaseError):
    """
    Base class for all message exceptions.
    """
    pass


class MessageNotFoundError(MessageError):
    """
    Raised when a message is not found.
    """
    pass


class MessageExistsError(MessageError):
    """
    Raised when a message already exists.
    """
    pass


class EventError(DatabaseError):
    """
    Base class for all event exceptions.
    """
    pass


class EventNotFoundError(EventError):
    """
    Raised when an event is not found.
    """
    pass


class EventExistsError(EventError):
    """
    Raised when an event already exists.
    """
    pass


class ReportError(DatabaseError):
    """
    Base class for all report exceptions.
    """
    pass


class ReportNotFoundError(ReportError):
    """
    Raised when a report is not found.
    """
    pass


class ReportExistsError(ReportError):
    """
    Raised when a report already exists.
    """
    pass


class ReportInactiveError(ReportError):
    """
    Raised when a report is inactive.
    """
    pass


class ReportActiveError(ReportError):
    """
    Raised when a report is active.
    """
    pass


class OTPError(DatabaseError):
    """
    Base class for all OTP exceptions.
    """
    pass


class OTPNotFoundError(OTPError):
    """
    Raised when an OTP is not found.
    """
    pass
