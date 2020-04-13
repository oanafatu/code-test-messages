from flask import request, Blueprint

from src.service.exceptions import (
    NoMessagesFoundException, NoMessageFoundException, NoUsersFoundException, WrongIndexProvided
)
from src.service import (
    fetch_all_messages, fetch_messages_for_user, submit_message_for_user, delete_messages_by_ids,
    fetch_message_by_id, fetch_all_not_already_fetched_messages, fetch_all_users, fetch_ordered_messages_in_range
)

MESSAGES_API = Blueprint('messages_api', __name__)


@MESSAGES_API.route('/', methods=['GET'])
def home():
    return 'Welcome! Navigate to /api/v1/messages to fetch all messages'


@MESSAGES_API.route('/api/v1/messages', methods=['GET'])
def get_all_messages():
    include_previously_fetched = request.args.get('include-previously-fetched')
    try:
        if include_previously_fetched == 'no':
            print('Received request to fetch all messages that were not previously fetched')
            response = fetch_all_not_already_fetched_messages()
        else:
            print('Received request to fetch all messages')
            response = fetch_all_messages()

        if response['status_code'] != 200:
            return response['error']
        messages = response['data']
        print(f'Received all messages: {messages}')
        return messages
    except NoMessagesFoundException as e:
        return str(e)


@MESSAGES_API.route('/api/v1/messages/ordered-by-timestamp', methods=['GET'])
def get_messages_in_range_ordered_by_timestamp():
    start_index = 0
    if request.args.get('start-index'):
        start_index = request.args.get('start-index')
    stop_index = -1
    if request.args.get('stop-index'):
        stop_index = request.args.get('stop-index')
    try:
        response = fetch_ordered_messages_in_range(start_index, stop_index)

        if response['status_code'] != 200:
            return response['error']

        messages = response['data']

        print(f'Received the messages ordered by timestamp: {messages}')
        return messages
    except (NoMessagesFoundException, WrongIndexProvided) as e:
        return str(e)


@MESSAGES_API.route('/api/v1/users', methods=['GET'])
def get_all_users():
    print('Received request to fetch all users')
    try:
        response = fetch_all_users()
        if response['status_code'] != 200:
            return response['error']
        users = response['data']
        print(f'Received all users: {users}')
        return users
    except NoUsersFoundException as e:
        return str(e)


@MESSAGES_API.route('/api/v1/messages/<string:message_id>', methods=['GET'])
def get_message_by_id(message_id):
    print(f'Received request to fetch message with id {message_id}')
    try:
        response = fetch_message_by_id(message_id)
        if response['status_code'] != 200:
            return response['error']
        message = response['data']
        print(f'Received message: {message}')
        return message
    except (NoMessageFoundException, NoMessagesFoundException) as e:
        return str(e)


@MESSAGES_API.route('/api/v1/messages/users/<string:username>', methods=['GET'])
def get_messages_for_user(username):
    print(f'Received request to fetch messages for username {username}')
    try:
        response = fetch_messages_for_user(username)
        if response['status_code'] != 200:
            return response['error']
        messages = response['data']
        print(f'Received all messages for {username}:', messages)

        return messages
    except (NoMessageFoundException, NoMessagesFoundException) as e:
        return str(e)


@MESSAGES_API.route('/api/v1/messages/user/<string:username>/submit-message', methods=['POST'])
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


@MESSAGES_API.route('/api/v1/messages/delete-messages', methods=['POST'])
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


def _convert_messages_df_to_dict(messages_df):
    messages_dict = {}
    for index, row in messages_df.iterrows():
        messages_dict[index] = {
            'id': row['id'],
            'useId': row['user_id'],
            'text': row['text'],
            'timestamp': row['timestamp']
        }
    return messages_dict


def _convert_users_df_to_dict(users_df):
    users_dict = {}
    for index, row in users_df.iterrows():
        users_dict[index] = {
            'id': row['id'],
            'username': row['username']
        }
    return users_dict
