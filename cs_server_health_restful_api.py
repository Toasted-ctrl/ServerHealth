import json

from flask import Flask, jsonify, request, Response
from cs_server_health_builtcomponents_page import display_last_ping_response, retrieve_server_identities, retrieve_server_systemload, retrieve_remote_server_credentials, retrieve_api_access_rights

app = Flask(__name__)

@app.route('/remote_server_last_ping_response', methods=['get'])
def remote_server_last_ping_response():

    hostname = request.args.get('hostname', None)
    api_key = request.args.get('api_key', None)

    try:

        if api_key == None:

            return jsonify ({'error': 'missing_api_key'})
        
        if not api_key == None:

            api_key_access_rights = retrieve_api_access_rights(api_key)

            if api_key_access_rights[0] == 200:

                if hostname == None:

                    return jsonify ({'error': 'missing_hostname'})
                
                elif not hostname == None:

                    remote_server_last_ping_response = display_last_ping_response(hostname)

                    if remote_server_last_ping_response[0] == 200:

                        ping_status = remote_server_last_ping_response[2]
                        ping_timestamp_log = remote_server_last_ping_response[1]

                        return jsonify ({'ping_timestamp_log': ping_timestamp_log, 'ping_status': ping_status})
                    
                    elif remote_server_last_ping_response[0] == 400:

                        return jsonify ({'error': 'empty_dataframe_ping_history'})
            
            elif api_key_access_rights[0] == 400: 

                return jsonify ({'error': 'nonexisting_api_key'})
            
            elif api_key_access_rights[0] == 404:

                return jsonify ({'error': 'unexpected_error_on_validating_api_key'})
    
    except:

        return jsonify ({'error': 'unknown_error'})

@app.route('/remote_server_identities', methods=['get'])
def remote_server_identities():

    api_key = request.args.get('api_key', None)

    try:
            
        if api_key == None:

            return jsonify ({'error': 'missing_api_key'})
        
        if not api_key == None:
        
            api_key_access_rights = retrieve_api_access_rights(api_key)

            if api_key_access_rights[0] == 200:

                server_identities = retrieve_server_identities()

                if server_identities[0] == 400:

                    return jsonify ({'error': 'empty_dataframe'})
                    
                elif server_identities[0] == 200:

                    dataframe_server_identities = server_identities[2]

                    return Response (dataframe_server_identities.to_json(orient="records"), mimetype='application/json')
                
            elif api_key_access_rights[0] == 400:

                return jsonify ({'error': 'nonexisting_api_key'})
            
            elif api_key_access_rights[0] == 404:

                return jsonify ({'error': 'unexpected_error_on_validating_api_key'})
                
    except:

        return jsonify ({'error': 'unknown_error'})
    
@app.route('/remote_server_systemload', methods=['get'])
def remote_server_systemload():

    hostname = request.args.get('hostname', None)
    api_key = request.args.get('api_key', None)

    try:

        if api_key == None:

            return jsonify ({'error': 'missing_api_key'})
        
        elif not api_key == None:

            api_key_access_rights = retrieve_api_access_rights(api_key)

            if api_key_access_rights[0] == 200:

                if hostname == None:

                    return jsonify ({'error': 'missing_hostname'})
                    
                elif not hostname == None:

                    remote_server_credential_request = retrieve_remote_server_credentials(hostname, 'serverhealth_logs')

                    if remote_server_credential_request[0] == 200:

                        remote_server_hostname = remote_server_credential_request[1]
                        remote_server_username = remote_server_credential_request[2]
                        remote_server_password = remote_server_credential_request[3]
                        remote_server_port = remote_server_credential_request[4]

                        result = retrieve_server_systemload(remote_server_hostname, remote_server_username, remote_server_password, 'serverhealth_logs', remote_server_port)

                        if result[0] == 400:

                            return jsonify ({'error': 'empty_dataframe_systemload'})
                        
                        elif result[0] == 200:

                            number_of_entries = result[1]
                            cpu_temp_max = result[2]
                            cpu_temp_mean = result[3]
                            system_memory_total = int(result[4])
                            system_memory_available_max = int(result[6])
                            system_memory_available_mean = int(result[7])
                            system_memory_free_max = int(result[8])
                            system_memory_free_mean = int(result[9])

                            return jsonify ({'systemload_records': number_of_entries,
                                            'systemload_cpu_temp_max': cpu_temp_max,
                                            'systemload_cup_temp_mean': cpu_temp_mean,
                                            'systemload_memory_total': system_memory_total,
                                            'systemload_memory_available_max': system_memory_available_max,
                                            'systemload_memory_available_mean': system_memory_available_mean,
                                            'systemload_memory_free_max': system_memory_free_max,
                                            'systemload_memory_free_mean': system_memory_free_mean})
                        
                        elif result[0] == 404:

                            return jsonify ({'error': 'error_on_calling_systemload'})
                        
                    elif remote_server_credential_request[0] == 400:

                        return jsonify ({'error': 'empty_dataframe_credentials'})

                    elif remote_server_credential_request[0] == 404:

                        return jsonify ({'error': 'failure_on_obtaining_remote_server_credentials'})
                
            elif api_key_access_rights[0] == 400:

                return jsonify ({'error': 'nonexisting_api_key'})
            
            elif api_key_access_rights[0] == 404:

                return jsonify ({'error': 'unexpected_error_on_validating_api_key'})

    except:

        return jsonify ({'error': 'unknown_error'})

if __name__ == '__main__':
    app.run()