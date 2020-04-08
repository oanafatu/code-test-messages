from datetime import datetime, timezone
from typing import List
from uuid import uuid4

import pandas as pd
from pandas import DataFrame

from src.models import User
from src.service.exceptions import (
    FailedToReadFromCsvException,
    UserNotValidException, NoMessagesFoundException,
    NoMessageFoundException,
    NoUsersFoundException, WrongIndexProvided)
from src.utils import get_file_path


def fetch_all_messages() -> dict:
    print('Start fetching messages ...')
    try:
        data_frame = _get_data_frame_from_csv_file('messages')
        if data_frame.empty:
            raise NoMessagesFoundException('No messages found in the database, noting to fetch!')

        new_df = data_frame.replace(to_replace=False, value=True)
        data_frame.update(new_df)
        _write_data_frame_to_csv_file(data_frame, 'messages')

        return {'status_code': 200, 'data': data_frame}
    except FailedToReadFromCsvException as e:
        return {'status_code': 400, 'error': str(e)}


def fetch_all_not_already_fetched_messages() -> dict:
    print('Start fetching messages not previously fetched...')
    try:
        data_frame = _get_data_frame_from_csv_file('messages')
        if data_frame.empty:
            raise NoMessagesFoundException('No messages found in the database, noting to fetch!')

        # pylint: disable=C0121
        filtered_df = data_frame[data_frame['fetched'] == False]
        if filtered_df.empty:
            raise NoMessagesFoundException('All messages were previously fetched!')

        # pylint: disable=C0121
        data_frame.loc[data_frame['fetched'] == False, 'fetched'] = True
        _write_data_frame_to_csv_file(data_frame, 'messages')

        print(f'Fetched all messages not previously fetched. All messages were marked as fetched.')
        return {'status_code': 200, 'data': filtered_df}
    except FailedToReadFromCsvException as e:
        return {'status_code': 400, 'error': str(e)}


def fetch_ordered_messages_in_range(start_index, stop_index) -> dict:
    print('Start fetching ordered messages ...')
    try:
        data_frame = _get_data_frame_from_csv_file('messages')
        if data_frame.empty:
            raise NoMessagesFoundException('No messages found in the database, noting to fetch!')
        try:
            filtered_df = data_frame[int(start_index):int(stop_index)+1]
        except KeyError:
            raise WrongIndexProvided(
                'One or both of the indexes provided are wrong. Please check the database and try again!')

        filtered_df = filtered_df.sort_values(by=['timestamp'])

        for i in range(int(start_index), int(stop_index) + 1):
            data_frame.at[i, 'fetched'] = True
        _write_data_frame_to_csv_file(data_frame, 'messages')

        return {'status_code': 200, 'data': filtered_df}
    except FailedToReadFromCsvException as e:
        return {'status_code': 400, 'error': str(e)}


def fetch_all_users() -> dict:
    print('Start fetching users...')
    try:
        data_frame = _get_data_frame_from_csv_file('users')
        if data_frame.empty:
            raise NoUsersFoundException('No users found in the database, noting to fetch!')

        return {'status_code': 200, 'data': data_frame}
    except FailedToReadFromCsvException as e:
        return {'status_code': 400, 'error': str(e)}


def fetch_message_by_id(message_id) -> dict:
    print('Start fetching the message ...')
    try:
        data_frame = _get_data_frame_from_csv_file('messages')
        if data_frame.empty:
            raise NoMessagesFoundException('No messages found in the database, noting to fetch!')

        filtered_df = data_frame[data_frame['id'] == message_id]
        if filtered_df.empty:
            raise NoMessageFoundException(f'No message with id {message_id} was found!')

        data_frame.loc[data_frame['id'] == message_id, 'fetched'] = True
        _write_data_frame_to_csv_file(data_frame, 'messages')

        print('Received fetched data')
        return {'status_code': 200, 'data': filtered_df}
    except FailedToReadFromCsvException as e:
        return {'status_code': 400, 'error': str(e)}


def fetch_messages_for_user(username: str) -> dict:
    print('Start fetching the messages for user ...')
    try:
        user = _validate_user(username)
        data_frame = _get_data_frame_from_csv_file('messages')
        if data_frame.empty:
            raise NoMessagesFoundException('No messages found in the database, noting to fetch!')

        filtered_df = data_frame[data_frame['user_id'] == user.id]
        if filtered_df.empty:
            raise NoMessagesFoundException(f'No messages found for user with username: {username}!')

        data_frame.loc[data_frame['user_id'] == user.id, 'fetched'] = True
        _write_data_frame_to_csv_file(data_frame, 'messages')

        print(f'Fetched messages for {username}')
        return {'status_code': 200, 'data': filtered_df}
    except (UserNotValidException, FailedToReadFromCsvException) as e:
        return {'status_code': 400, 'error': str(e)}


def submit_message_for_user(username: str, text: str):
    print('Submitting message to user ...')
    try:
        user = _validate_user(username)
        data_frame = pd.DataFrame({
            'id': uuid4(),
            'user_id': user.id,
            'text': text,
            'timestamp': datetime.now(timezone.utc),
            'fetched': False
        }, index=[0])
        _write_data_frame_to_csv_file(data_frame, 'messages', mode='a', header=False)

        response_message = f'Message was successfully submitted for {username}! ' \
            f'Navigate to http://localhost:5000/messages/user/{username} to view all user\'s messages'
        return {'status_code': 200, 'data': response_message}
    except UserNotValidException as e:
        return {'status_code': 400, 'error': str(e)}


def delete_messages_by_ids(ids: List[str]):
    print('Delete messages started ...')
    try:
        data_frame = _get_data_frame_from_csv_file('messages')
        if data_frame.empty:
            raise NoMessagesFoundException('No messages found in the database, noting to fetch!')

        deleted = 0
        for message_id in ids:
            index_names = data_frame[data_frame['id'] == message_id].index
            deleted += len(index_names)
            data_frame.drop(index_names, inplace=True)

        _write_data_frame_to_csv_file(data_frame, 'messages')
        response_message = f'Successfully deleted {deleted} out of {len(ids)} message ids!' \
            f'Navigate to http://localhost:5000/messages to view all messages'
        return {'status_code': 200, 'data': response_message}
    except FailedToReadFromCsvException as e:
        return {'status_code': 400, 'error': str(e)}


def _validate_user(username: str) -> User:
    print('Validating username: ', username)
    data_frame = _get_data_frame_from_csv_file('users')
    for _, row in data_frame.iterrows():
        if row['username'] == username:
            return User(id=row['id'], username=row['username'])
    raise UserNotValidException(f'User with username {username} is not a valid user.')


def _get_data_frame_from_csv_file(filename) -> DataFrame:
    try:
        file_path = get_file_path(__file__, f'../database/{filename}.csv')
        return pd.read_csv(file_path)
    except FileNotFoundError:
        raise FailedToReadFromCsvException('Failed to read from csv, file not found. ')


def _write_data_frame_to_csv_file(data_frame, filename, mode='w', header=True):
    try:
        file_path = get_file_path(__file__, f'../database/{filename}.csv')
        data_frame.to_csv(file_path, index=False, mode=mode, header=header)
    except FileNotFoundError:
        raise FailedToReadFromCsvException('Failed to read from csv, file not found. ')
