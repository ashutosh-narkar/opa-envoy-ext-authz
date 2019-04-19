from flask import Flask, request
import os
import requests

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'Hello from the {} service !\n'.format(os.environ['SERVICE_NAME'])


@app.route('/the/good/path')
def the_good_path():
    url = "http://backend-service/good"
    r = requests.get(url, headers=request.headers, auth=('web', 'password'))

    if r.status_code != 200:
        return "Access to the Backend service is forbidden.\n", r.status_code

    msg = "Allowed path: WEB -> {}\n".format(r.text)
    return msg, r.status_code


@app.route('/the/bad/path')
def the_bad_path():
    url = "http://db-service/good/db"
    r = requests.get(url, headers=request.headers, auth=('web', 'password'))

    if r.status_code != 200:
        return "Forbidden path: WEB -> DB\n", r.status_code

    msg = "Allowed path: WEB -> {}\n".format(r.text)
    return msg, r.status_code


@app.route('/good')
def good():
    url = "http://db-service/good/db"
    r = requests.get(url, headers=request.headers, auth=('backend', 'password'))

    if r.status_code != 200:
        return "Access to the DB service is forbidden.\n", r.status_code

    msg = "BACKEND -> {}".format(r.text)
    return msg, r.status_code


@app.route('/good/db')
def good_db():
    return "DB"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
