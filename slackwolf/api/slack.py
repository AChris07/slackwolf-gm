from typing import List, Dict
import requests
from flask import current_app as app


def get_users_list() -> List[Dict]:
    base_url = app.config['SLACK_URL']
    url = f"{base_url}/api/conversations.list"

    token = app.config['SLACK_BOT_TOKEN']
    params = {'token': token, 'types': 'im'}

    res = requests.get(url, params=params)

    if not res.json().get('ok'):
        raise requests.RequestException

    channels = res.json()['channels']
    users = [x for x in channels if x['is_im']]

    return users


def post_message(channel, text) -> None:
    base_url = app.config['SLACK_URL']
    url = f"{base_url}/api/chat.postMessage"

    token = app.config['SLACK_BOT_TOKEN']
    params = {'token': token, 'channel': channel, 'text': text}

    res = requests.post(url, params=params)

    if not res.json().get('ok'):
        raise requests.RequestException
