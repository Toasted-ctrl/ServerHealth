import json

from flask import Flask, jsonify, request
from cs_server_health_builtcomponents_page import display_last_ping_response, retrieve_server_identities, retrieve_server_systemload

app = Flask(__name__)

@app.route('/remote_server_last_ping_response', methods=['get'])
def remote_server_last_ping_response():

    hostname = request.args.get('hostname', None)

    response = display_last_ping_response(hostname)

    ping_status = response[2]
    ping_timestamp_log = response[1]

    return jsonify ({'ping_timestamp_log': ping_timestamp_log, 'ping_status': ping_status})

@app.route('/remote_server_identities', methods=['get'])
def remote_server_identities():

    response = retrieve_server_identities()

    if response[0] == 400:

        return jsonify ({'error': 'empty_dataframe'})
    
    elif response[0] == 200:

        number_of_servers = response[1]
        dataframe_server_identities = response[2]

        server_identities_list = dataframe_server_identities.apply(lambda row: (row['server_name'], row['server_ip_address']), axis=1).tolist()
        print(server_identities_list)

        return jsonify ({'number_of_servers': number_of_servers, 'server_identities': server_identities_list})
    
    else:

        return jsonify ({'error': 'unknown_error'})
    
@app.route('/remote_server_systemload', methods=['get'])
def remote_server_systemload():

    ## NEED TO IMPLEMENT API_KEY TO THIS FUNCTION. BUILD API_KEY check function in cs_server_health_builtcomponents_page

    hostname = request.args.get('hostname', None)
    api_key = request.args.get('api_key', None)

    if api_key == None:

        return jsonify ({'error': 'missing_api_key'})
    
    elif not api_key == None:

        ##requires additional details. Rebuild.

        result = retrieve_server_systemload(hostname)

        if result[0] == 400:

            return jsonify ({'error': 'empty_dataframe'})
        
        elif result[0] == 200:

            number_of_entries = result[1]
            cpu_temp_max = result[2]
            cpu_temp_mean = result[3]
            system_memory_total = result[4]
            system_memory_available_max = result[6]
            system_memory_available_mean = result[7]
            system_memory_free_max = result[8]
            system_memory_free_mean = result[9]

            return jsonify ({'number_of_entries': number_of_entries,
                            'cpu_temp_max': cpu_temp_max, 'cpu_temp_mean': cpu_temp_mean,
                            'system_memory_total': system_memory_total,
                            'system_memory_available_max': system_memory_available_max, 'system_memory_available_mean': system_memory_available_mean,
                            'system_memory_free_max': system_memory_free_max, 'system_memory_free_mean': system_memory_free_mean})

    else:

        return jsonify ({'error': 'unknown_error'})


if __name__ == '__main__':
    app.run()