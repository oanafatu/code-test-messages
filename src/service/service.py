from datetime import datetime, timezone
from typing import List
from uuid import uuid4

import pandas as pd
from pandas import DataFrame

from src.models import Message, User
from src.service.exceptions import (
    FailedToReadFromCsvException,
    UserNotValidException, NoMessagesFoundException,
    NoMessageFoundException
)
from src.utils import get_file_path


def fetch_all_messages() -> dict:
    print('Start fetching messages ...')
    try:
        df = _get_data_frame_from_csv_file('messages')
        if df.empty:
            raise NoMessagesFoundException('No messages found in the database, noting to fetch!')

        new_df = df.replace(to_replace=False, value=True)
        df.update(new_df)
        _write_data_frame_to_csv_file(df, 'messages')

        messages = _convert_df_to_list_of_messages(df)
        print('Received fetched data: ', messages)
        return {'status_code': 200, 'data': messages}
    except FailedToReadFromCsvException as e:
        return {'status_code': 400, 'error': str(e)}


def fetch_all_not_fetched_messages() -> dict:
    print('Start fetching messages not previously fetched...')
    try:
        df = _get_data_frame_from_csv_file('messages')
        if df.empty:
            raise NoMessagesFoundException('No messages found in the database, noting to fetch!')

        filtered_df = df[df['fetched'] == False]
        if filtered_df.empty:
            raise NoMessagesFoundException('All messages were previously fetched!')

        df.loc[df['fetched'] == False, 'fetched'] = True
        _write_data_frame_to_csv_file(df, 'messages')

        messages = []
        for index, row in filtered_df.iterrows():
            messages.append(Message(
                id=row['id'],
                user_id=row['user_id'],
                text=row['text'],
                timestamp=row['timestamp']
            ))
        print(f'Fetched all messages not previously fetched. All messages were marked as fetched.')
        return {'status_code': 200, 'data': messages}
    except FailedToReadFromCsvException as e:
        return {'status_code': 400, 'error': str(e)}


def fetch_message_by_id(message_id) -> dict:
    print('Start fetching the message ...')
    try:
        df = _get_data_frame_from_csv_file('messages')
        if df.empty:
            raise NoMessagesFoundException('No messages found in the database, noting to fetch!')

        filtered_df = df[df['id'] == message_id]
        if filtered_df.empty:
            raise NoMessageFoundException(f'No message with id {message_id} was found!')

        df.loc[df['id'] == message_id, 'fetched'] = True
        _write_data_frame_to_csv_file(df, 'messages')

        messages = _convert_df_to_list_of_messages(filtered_df)
        print('Received fetched data: ', messages)
        return {'status_code': 200, 'data': messages}
    except FailedToReadFromCsvException as e:
        return {'status_code': 400, 'error': str(e)}


def fetch_messages_for_user(username: str) -> dict:
    print('Start fetching the messages for user ...')
    try:
        user = _validate_user(username)
        df = _get_data_frame_from_csv_file('messages')
        if df.empty:
            raise NoMessagesFoundException('No messages found in the database, noting to fetch!')

        filtered_df = df[df['user_id'] == user.id]
        if filtered_df.empty:
            raise NoMessagesFoundException(f'No messages found for user with username: {username}!')

        df.loc[df['user_id'] == user.id, 'fetched'] = True
        _write_data_frame_to_csv_file(df, 'messages')

        messages = []
        for index, row in filtered_df.iterrows():
            messages.append(Message(
                id=row['id'],
                user_id=row['user_id'],
                text=row['text'],
                timestamp=row['timestamp']
            ))
        print(f'Fetched messages for {username}')
        return {'status_code': 200, 'data': messages}
    except (UserNotValidException, FailedToReadFromCsvException) as e:
        return {'status_code': 400, 'error': str(e)}


def submit_message_for_user(username: str, text: str):
    print('Submitting message to user ...')
    try:
        user = _validate_user(username)
        df = pd.DataFrame({
            'id': uuid4(),
            'user_id': user.id,
            'text': text,
            'timestamp': datetime.now(timezone.utc),
            'fetched': False
        }, index=[0])
        _write_data_frame_to_csv_file(df, 'messages', mode='a', header=False)

        response_message = f'Message was successfully submitted for {username}! ' \
            f'Navigate to http://localhost:5000/messages/user/{username} to view all user\'s messages'
        return {'status_code': 200, 'data': response_message}
    except UserNotValidException as e:
        return {'status_code': 400, 'error': str(e)}


def delete_messages_by_ids(ids: List[str]):
    print('Delete messages started ...')
    try:
        df = _get_data_frame_from_csv_file('messages')
        if df.empty:
            raise NoMessagesFoundException('No messages found in the database, noting to fetch!')

        deleted = 0
        for message_id in ids:
            index_names = df[df['id'] == message_id].index
            deleted += len(index_names)
            df.drop(index_names, inplace=True)

        _write_data_frame_to_csv_file(df, 'messages')
        response_message = f'Successfully deleted {deleted} out of {len(ids)} message ids!' \
                  f'Navigate to http://localhost:5000/messages to view all messages'
        return {'status_code': 200, 'data': response_message}
    except FailedToReadFromCsvException as e:
        return {'status_code': 400, 'error': str(e)}


def _validate_user(username: str) -> User:
    print('Validating username: ', username)
    df = _get_data_frame_from_csv_file('users')
    for index, row in df.iterrows():
        if row['username'] == username:
            return User(id=row['id'], username=row['username'])
    raise UserNotValidException(f'User with username {username} is not a valid user.')


def _get_data_frame_from_csv_file(filename) -> DataFrame:
    try:
        file_path = get_file_path(__file__, f'../database/{filename}.csv')
        return pd.read_csv(file_path)
    except FileNotFoundError:
        raise FailedToReadFromCsvException('Failed to read from csv, file not found. ')


def _write_data_frame_to_csv_file(df, filename, mode='w', header=True):
    try:
        file_path = get_file_path(__file__, f'../database/{filename}.csv')
        df.to_csv(file_path, index=False, mode=mode, header=header)
    except FileNotFoundError:
        raise FailedToReadFromCsvException('Failed to read from csv, file not found. ')


def _convert_df_to_list_of_messages(df) -> List[Message]:
    result_list = []
    for index, row in df.iterrows():
        result_list.append(Message(
            id=row['id'],
            user_id=row['user_id'],
            text=row['text'],
            timestamp=row['timestamp']
        ))
    return result_list
