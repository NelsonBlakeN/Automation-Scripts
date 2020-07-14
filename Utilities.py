import logging
import os
import requests

API_BASE_URL = 'https://sleepy-fortress-77799.herokuapp.com/scripts/'


def get_exec_permission(script_name):
    endpoint = API_BASE_URL + script_name
    response = requests.get(endpoint)

    if response.status_code == 200:
        return response.json()["value"]
    elif response.status_code == 404:
        response = requests.post(endpoint + "/1")
        return response.json()["value"]




