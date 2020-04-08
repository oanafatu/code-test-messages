class FailedToReadFromCsvException(Exception):
    error_message = 'FAILED_TO_READ_CSV'


class NoMessagesFoundException(Exception):
    error_message = 'NO_MESSAGES_FOUND_EXCEPTION'


class NoUsersFoundException(Exception):
    error_message = 'NO_USERS_FOUND_EXCEPTION'


class NoMessageFoundException(Exception):
    error_message = 'NO_MESSAGE_FOUND_EXCEPTION'


class UserNotValidException(Exception):
    error_message = 'USERNAME_IS_NOT_VALID_EXCEPTION'


class WrongIndexProvided(Exception):
    error_message = 'WRONG_INDEX'
