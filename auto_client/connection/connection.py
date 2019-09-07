''' Moudule for league client communication '''
import logging
import time

import requests
import lcu_connector_python as lcu

import urllib3

from settings import LEAGUE_CLIENT_LOCATION


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class LeagueConnectionException(Exception):
    ''' Raised when there is error when connecting to league client '''


class Connection:
    ''' Connects to league client and communicates with it '''

    def __init__(self):
        self.connection = None

    def get_connection(self):
        ''' Parses connection url and port from lockfile '''
        if self.connection is not None:
            return self.connection
        connection = lcu.connect(LEAGUE_CLIENT_LOCATION)
        if connection == 'Ensure the client is running and that you supplied the correct path':
            raise LeagueConnectionException
        connection['kargs'] = {
            'verify': False,
            'auth': ('riot', connection['authorization']),
            'timeout': 30
        }
        return connection



    def request(self, path, method, json=None):
        ''' Sends a request to league client '''
        try:
            connection = self.get_connection()
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
