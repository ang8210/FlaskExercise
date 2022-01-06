import requests
# import logging
# import logging.config
# logging.config.fileConfig('./logfile/logging.conf')
# logger = logging.getLogger()

URL = "http://127.0.0.1:5000/"

def list():
    path = URL+"/list"
    response = requests.get(url=path)
    body = response.json()
    # logger.debug("123")
    return body


def addItem(data):
    path = URL+"/addItem"
    response = requests.post(url=path,json=data)
    body = response.json()
    return body


def deleteItem(params):
    path = URL+"/deleteItem"
    response = requests.get(url=path,params=params)
    body = response.json()
    return body


def modifyPrice(params):
    path = URL+"/modifyPrice"
    response = requests.get(url=path,params=params)
    body = response.json()
    return body


def order(data):
    path = URL+"/order"
    response = requests.post(url=path,json=data)
    body = response.json()
    return body


def select(params):
    path = URL+"/select"
    response = requests.get(url=path,params=params)
    body = response.json()
    return body