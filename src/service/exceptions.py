class MessageException(Exception):
    error_message = 'MESSAGE EXCEPTION'


class FailedToFetchMessagesException(MessageException):
    error_message = 'FAILED_TO_FETCH_MESSAGES_EXCEPTION'
