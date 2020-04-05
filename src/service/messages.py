from typing import List

import pandas as pd

from src.models import Message
from src.service.exceptions import FailedToFetchMessagesException
from src.utils import get_file_path


def fetch_all_messages() -> List[Message]:
    print('Start to fetch messages')
    try:
        file_path = get_file_path(__file__, '../database.csv')
        data = pd.read_csv(file_path)
        messages = []
        for index, row in data.iterrows():
            messages.append(Message(
                id=row['id'],
                username=row['username'],
                text=row['username'],
                timestamp=row['timestamp']
            ))
    except Exception as e:
        raise FailedToFetchMessagesException(str(e)) from e

    if messages:
        print('Received fetched data: ', messages)
        return messages

    raise FailedToFetchMessagesException(f'Failed to fetch questions')
