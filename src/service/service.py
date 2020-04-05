from typing import List

import pandas as pd
from pandas import DataFrame

from src.models import Message, User
from src.service.exceptions import FailedToFetchMessagesException, FailedToFetchUsersException, FailedToReadFromCsvException, \
    UserNotValidException
from src.utils import get_file_path


def fetch_all_messages() -> List[Message]:
    print('Start to fetch messages')
    try:
        data = _fetch_data_from_csv_file('messages')
        messages = []
        for index, row in data.iterrows():
            messages.append(Message(
                id=row['id'],
                user_id=row['user_id'],
                text=row['text'],
                timestamp=row['timestamp']
            ))
        print('Received fetched data: ', messages)
        return messages
    except FailedToReadFromCsvException as e:
        raise FailedToFetchMessagesException(str(e)) from e


def fetch_messages_for_user(username: str) -> List[Message]:
    try:
        user = _validate_user(username)
        messages = []
        data = _fetch_data_from_csv_file('messages')
        filtered_data = data[data['user_id'] == user.id]
        for index, row in filtered_data.iterrows():
            messages.append(Message(
                id=row['id'],
                user_id=row['user_id'],
                text=row['text'],
                timestamp=row['timestamp']
                )
            )
        print(f'Fetched messages for {username}: ', messages)
        return messages
    except UserNotValidException as e:
        raise UserNotValidException(str(e)) from e


def _validate_user(username: str) -> User:
    print('Validating username: ', username)
    try:
        data = _fetch_data_from_csv_file('users')
        for index, row in data.iterrows():
            if row['username'] == username:
                return User(
                    id=row['id'],
                    username=row['username']
                )
        raise UserNotValidException
    except FailedToReadFromCsvException as e:
        raise FailedToFetchUsersException(str(e)) from e


def _fetch_data_from_csv_file(filename) -> DataFrame:
    try:
        file_path = get_file_path(__file__, f'../database/{filename}.csv')
        return pd.read_csv(file_path)
    except Exception as e:
        raise FailedToReadFromCsvException(str(e)) from e

