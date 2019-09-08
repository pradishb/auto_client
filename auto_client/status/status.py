''' Module to find the status of league client '''
from requests import get
from requests.exceptions import RequestException

def is_client_connected(connection):
    ''' Returns if client is connected '''
    if connection.url is None:
        return False
    return True

def is_lcu_connected(connection):
    ''' Returns if lcu is connected '''
    if connection.url is None:
        return False
    try:
        res = get(connection.url + '/lol-service-status/v1/lcu-status', **connection.kwargs)
    except RequestException:
        return False
    if res.status_code == 404:
        return False
    res_json = res.json()
    try:
        if res_json['status'] == 'online':
            return True
    except KeyError:
        pass
    return False

STATUS_MAPPING = {
    'client_connected': is_client_connected,
    'lcu_connected': is_lcu_connected,
}

def get_status(connection):
    ''' Returns the status of league client '''
    status = []
    for key, func in STATUS_MAPPING.items():
        if func(connection):
            status.append(key)
    return status

def display_status(stdscr, status):
    ''' Displays the status in the screen '''
    for key in STATUS_MAPPING:
        stdscr.addstr('{}: {}\n'.format(key.title(), key in status))
