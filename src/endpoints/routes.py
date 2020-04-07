from flask import request

from src import app
from src.service.exceptions import (
    NoMessagesFoundException,
    NoMessageFoundException
)
from src.service.service import (
    fetch_all_messages, fetch_messages_for_user, submit_message_for_user,
    delete_messages_by_ids, fetch_message_by_id, fetch_all_not_fetched_messages
)


@app.route('/', methods=['GET'])
def home():
    return 'Welcome! Navigate to /messages to see all messages'


@app.route('/messages/', methods=['GET'])
def get_all_messages():
    print('Received request to fetch all messages')
    try:
        response = fetch_all_messages()
        if response['status_code'] != 200:
            return response['error']
        messages = _convert_to_dict(response['data'])
        print(f'Received all messages: {messages}')
        return messages
    except NoMessagesFoundException as e:
        return str(e)


@app.route('/messages/not-fetched', methods=['GET'])
def get_all_not_fetched_messages():
    print('Received request to fetch all messages that were not previously fetched')
    try:
        response = fetch_all_not_fetched_messages()
        if response['status_code'] != 200:
            return response['error']
        messages = _convert_to_dict(response['data'])
        print(f'Received all messages: {messages}')
        return messages
    except NoMessagesFoundException as e:
        return str(e)


@app.route('/messages/<string:message_id>', methods=['GET'])
def get_message_by_id(message_id):
    print(f'Received request to fetch message with id {message_id}')
    try:
        response = fetch_message_by_id(message_id)
        if response['status_code'] != 200:
            return response['error']
        message = _convert_to_dict(response['data'])
        print(f'Received message: {message}')
        return message
    except (NoMessageFoundException, NoMessagesFoundException) as e:
        return str(e)


@app.route('/messages/user/<string:username>', methods=['GET'])
def get_messages_for_user(username):
    print('Received request to fetch messages for username ', username)
    try:
        response = fetch_messages_for_user(username)
        if response['status_code'] != 200:
            return response['error']
        messages = _convert_to_dict(response['data'])
        print(f'Received all messages for {username}:', messages)
        return messages
    except (NoMessageFoundException, NoMessagesFoundException) as e:
        return str(e)


@app.route('/messages/user/<string:username>/submit-message', methods=['POST'])
def create_message_for_user(username):
    print('Received request to submit messages for username ', username)

    try:
        data = request.get_json()
        text = data['text']
    except KeyError:
        return 'The data provided is wrong, please check and try again!'

    try:
        response = submit_message_for_user(username, text)
        if response['status_code'] != 200:
            return response['error']
        return response['data']
    except Exception as e:
        return str(e)


@app.route('/messages/delete-messages', methods=['POST'])
def delete_messages():
    print('Received request to delete messages!')

    try:
        data = request.get_json()
        ids = data['ids']
    except KeyError:
        return 'The data provided is wrong, please check and try again!'

    try:
        response = delete_messages_by_ids(ids)
        if response['status_code'] != 200:
            return response['error']
        return response['data']
    except NoMessagesFoundException as e:
        return str(e)


def _convert_to_dict(array):
    final_dict = {}
    for item in array:
        final_dict[item.id] = {
            'user_id': item.user_id,
            'text': item.text,
            'timestamp': item.timestamp
        }
    return final_dict
