from flask import request

from src import app
from src.service.exceptions import FailedToFetchMessagesException, FailedToFetchUsersException, UserNotValidException
from src.service.service import fetch_all_messages, fetch_messages_for_user, submit_message_for_user, \
    delete_messages_by_ids


@app.route('/', methods=['GET'])
def home():
    return 'Welcome! Navigate to /messages to see all messages'


@app.route('/messages/', methods=['GET'])
def get_all_messages():
    print('Received request to fetch all messages')
    try:
        messages = fetch_all_messages()
        result = _convert_to_dict(messages)
        print('Received all messages:', messages)
        return result
    except FailedToFetchMessagesException as e:
        print(e.error_message)
        return e.error_message


@app.route('/messages/<string:username>', methods=['GET'])
def get_messages_for_user(username):
    print('Received request to fetch messages for username ', username)
    try:
        messages = fetch_messages_for_user(username)
        result = _convert_to_dict(messages)
        print(f'Received all messages for {username}:', messages)
        if result:
            return result
        else:
            return 'No messages found for user!'
    except UserNotValidException as e:
        print(e.error_message)
        return 'User not valid!'


@app.route('/messages/<string:username>/submit-message', methods=['POST'])
def create_message_for_user(username):
    print('Received request to submit messages for username ', username)
    data = request.get_json()
    text = data['text']
    try:
        submit_message_for_user(username, text)
        return f'Message was successfully submited for {username}! ' \
               f'Navigate to http://localhost:5000/messages/{username} to view all messages'
    except UserNotValidException as e:
        print(e.error_message)
        return e.error_message


@app.route('/messages/delete-messages', methods=['POST'])
def delete_messages():
    print('Received request to delete the following messages')
    data = request.get_json()
    ids = data['ids']
    try:
        delete_messages_by_ids(ids)
        return 'Success'
    except FailedToFetchMessagesException as e:
        print(e.error_message)
        return e.error_message


def _convert_to_dict(array):
    final_dict = {}
    for item in array:
        final_dict[item.id] = {
            'user_id': item.user_id,
            'text': item.text,
            'timestamp': item.timestamp
        }
    return final_dict
