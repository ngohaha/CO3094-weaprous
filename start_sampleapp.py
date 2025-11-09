#
# Copyright (C) 2025 pdnguyen of HCMC University of Technology VNU-HCM.
# All rights reserved.
# This file is part of the CO3093/CO3094 course,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#
# WeApRous release
#
# The authors hereby grant to Licensee personal permission to use
# and modify the Licensed Source Code for the sole purpose of studying
# while attending the course
#


"""
start_sampleapp
~~~~~~~~~~~~~~~~~

This module provides a sample RESTful web application using the WeApRous framework.

It defines basic route handlers and launches a TCP-based backend server to serve
HTTP requests. The application includes a login endpoint and a greeting endpoint,
and can be configured via command-line arguments.
"""

import json
import socket
import argparse

from daemon.weaprous import WeApRous

PORT = 8000  # Default port

app = WeApRous()

@app.route('/login', methods=['POST', 'GET'])
def login(headers="guest", body="anonymous"):
    print("[DEBUG] Received body:", body)
    """
    Handle user login via POST request.

    This route simulates a login process and prints the provided headers and body
    to the console.

    :param headers (str): The request headers or user identifier.
    :param body (str): The request body or login payload.
    """
    try: 
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except Exception:
                kv = {}
                for item in body.split('&'):
                    if '=' in item:
                        k, v = item.split('=', 1)
                        kv[k] = v
                if kv:
                    body = kv
        username = (body or {}).get('username', '')
        password = (body or {}).get('password', '')
        print(("[SampleApp] Logging in {} to {}".format(headers, body)))

        if username == "tien" and password == "deptraiqua":
            return ('application/json', json.dumps({"status":"success","message":"Login successful"}))
        else:
            return 'Login failed'
    except Exception as e:
        print(("[SampleApp] Login error: {}".format(e)))
        return 'Login Failed'

@app.route('/hello', methods=['PUT'])
def hello(headers, body):
    """
    Handle greeting via PUT request.

    This route prints a greeting message to the console using the provided headers
    and body.

    :param headers (str): The request headers or user identifier.
    :param body (str): The request body or message payload.
    """
    try: 
        name = None
        if isinstance(body, dict):
            name = body.get('name')
        elif isinstance(body, str):
            try: 
                j = json.loads(body)
                name = j.get('name')
            except Exception:
                pass
        print(("[SampleApp] ['PUT'] Hello in {} to {}".format(headers, body)))
    except Exception as e:
        print(("[SampleApp] Hello error: {}".format(e)))
        return ('text/plain', 'Error processing hello request')
    html = f"""<html>
    <head><title>Hello</title></head>
    <body>
    <h1>Hello, {name}!</h1>
    <p>This is a sample WeApRous PUT response.</p>
    </body>
    </html>"""
    return ('text/html', html)

if __name__ == "__main__":
    # Parse command-line arguments to configure server IP and port
    parser = argparse.ArgumentParser(prog='Backend', description='', epilog='Beckend daemon')
    parser.add_argument('--server-ip', default='0.0.0.0')
    parser.add_argument('--server-port', type=int, default=PORT)
 
    args = parser.parse_args()
    ip = args.server_ip
    port = args.server_port

    # Prepare and launch the RESTful application
    app.prepare_address(ip, port)
    app.run()