''' Moudule for league client communication '''
import logging
import time
import threading

import urllib3
import requests
import lcu_connector_python as lcu


from settings import LEAGUE_CLIENT_LOCATION, CONNECTION_READ_INTERVAL


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ClientConnectionException(Exception):
    ''' Raised when there is error when connecting to league client '''


class Connection:
    ''' Connects to league client and communicates with it '''

    def __init__(self):
        self.connection = None
        get_connection_thread = threading.Thread(
            target=self.get_connection_loop, daemon=True)
        get_connection_thread.start()

    def get_connection_loop(self):
        ''' Parses connection in a certain interval '''
        while True:
            self.get_connection()
            time.sleep(CONNECTION_READ_INTERVAL)

    def get_connection(self):
        ''' Parses connection url and port from lockfile '''
        connection = lcu.connect(LEAGUE_CLIENT_LOCATION)
        if connection == 'Ensure the client is running and that you supplied the correct path':
            self.connection = None
            return
        connection['kargs'] = {
            'verify': False,
            'auth': ('riot', connection['authorization']),
            'timeout': 30
        }
        self.connection = connection



    def request(self, path, method, json=None):
        ''' Sends a request to league client '''
        try:
            if self.connection is None:
                raise ClientConnectionException
            connection = self.connection
            url = ('https://' + connection['url'] + path)
            logging.debug(
                'request,method=%s,url=%s,json=%s', method, url, json)
            res = None
            if method == 'get':
                res = requests.get(url, params=json, **connection['kargs'])
            if method == 'post':
                res = requests.post(url, json=json, **connection['kargs'])
            if method == 'delete':
                res = requests.delete(url, json=json, **connection['kargs'])
            if method == 'patch':
                res = requests.patch(url, json=json, **connection['kargs'])
            if method == 'put':
                res = requests.put(url, json=json, **connection['kargs'])
            return res
        except requests.exceptions.RequestException:
            logging.error('Error in request: %s', path)
            time.sleep(10)
