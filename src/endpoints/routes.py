from src import app
from src.service.exceptions import FailedToFetchMessagesException
from src.service.messages import fetch_all_messages


@app.route('/', methods=['GET'])
def home():
    return 'Start here'


@app.route('/messages/', methods=['GET'])
def get_all_messages():
    print('Received request to fetch all messages')
    try:
        messages = fetch_all_messages()
        result = _convert_to_dict(messages)
        print('Received all messages:', messages)
        return result
    except FailedToFetchMessagesException as e:
        print(e)
        return e.error_message


@app.route('/messages/', methods=['POST'])
def submit_message_to_user(username):
    pass


def _convert_to_dict(array):
    final_dict = {}
    for item in array:
        final_dict[item.id] = {
            'username': item.username,
            'text': item.text,
            'timestamp': item.timestamp
        }
    return final_dict
