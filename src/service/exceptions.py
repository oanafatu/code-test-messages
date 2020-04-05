class FailedToFetchMessagesException(Exception):
    error_message = 'FAILED_TO_FETCH_MESSAGES_EXCEPTION'


class FailedToFetchUsersException(Exception):
    error_message = 'FAILED_TO_FETCH_USERS_EXCEPTION'


class FailedToReadFromCsvException(Exception):
    error_message = 'FAILED_TO_READ_FROM_CSV_EXCEPTION'


class UserNotValidException(Exception):
    error_message = 'USERNAME_IS_NOT_VALID_EXCEPTION'


class FailedToDeleteMessagesException(Exception):
    error_message = 'FAILED_TO_DELETE_MESSAGES_EXCEPTION'
