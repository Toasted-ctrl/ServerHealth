import json

from flask import Flask, jsonify, request
from cs_server_health_builtcomponents_page import display_last_ping_response

app = Flask(__name__)

@app.route('/remote_server_last_ping_response', methods=['get'])
def remote_server_last_ping_response():

    hostname = request.args.get('hostname', None)

    response = display_last_ping_response(hostname)

    ping_status = response[1]
    ping_timestamp_log = response[0]

    return jsonify ({'ping_timestamp_log': ping_timestamp_log, 'ping_status': ping_status})

if __name__ == '__main__':
    app.run()