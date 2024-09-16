#!/usr/bin/env python3

from cs_server_health_builtcomponents import ping_server, retrieve_host_machines_ip_addresses, store_ping_response

try:

    ip_address_retrieval = retrieve_host_machines_ip_addresses()

    if ip_address_retrieval[0] == 200:
        
        ip_addresses = ip_address_retrieval[1]

        for ip_address in ip_addresses:

            cleaned_ip_address = ip_address.replace("/32", "")

            server_response = ping_server(cleaned_ip_address)

            if server_response == True:

                ping_pass_fail = "PASS"

            if server_response == False:

                ping_pass_fail = "FAIL"

            try:

                store_ping_response(ip_address, ping_pass_fail)

            except Exception as e:

                print(f"Error: {e}")

    elif ip_address_retrieval[0] == 400:
        print(f"No IP addresses in table.")

except Exception as e:
    print(f"Error: {e}")