import requests
from flask import Flask, request, Response
import logging
import os
import json

app = Flask(__name__)
logger = None
format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger('netcompany-dynamics')

# Log to stdout
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(logging.Formatter(format_string))
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)

client_secret = os.environ.get("client_secret")
client_id = os.environ.get("client_id")
grant_type = os.environ.get("grant_type")
token_url = os.environ.get("token_url")
scope = os.environ.get("scope")
api_url = os.environ.get("api_url")

def auth():
    data = {"Content-Type": "application/x-www-form-urlencoded", "grant_type": grant_type, "scope": scope, "client_id": client_id, "client_secret": client_secret}
    req = requests.post(url = token_url, data = data)
    if req.status_code != 200:
        logger.error("Unexpected response status code: %d with response text %s" % (req.status_code, req.text))
        raise AssertionError ("Unexpected response status code: %d with response text %s"%(req.status_code, req.text))
    return req.json()["access_token"]


@app.route("/get-contacts", methods=["GET", "POST"])
def get_contacts():
    token = auth()
    if request.args.get('since') is None:
        url = api_url + "/contacts?$select=fullname,emailaddress1,modifiedon,telephone1"
    else:
        url = api_url + "/contacts?$select=fullname,emailaddress1,modifiedon,telephone1&$filter=modifiedon ge {}".format(request.args.get('since'))

    headers = {"Authorization": "Bearer {}".format(token), 
        "Accept": "application/json",
        "Content-type": "application/json",
        "If-None-Match": "null",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0"}

    req = requests.get(url = url, headers = headers)

    if req.status_code != 200:
        logger.error("Unexpected response status code: %d with response text %s" % (req.status_code, req.text))
        raise AssertionError ("Unexpected response status code: %d with response text %s"%(req.status_code, req.text))

    entities = req.json()["value"]
    for entity in entities:
        entity["_updated"] = entity["modifiedon"]

    return json.dumps(entities)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=os.environ.get('port',5000))
