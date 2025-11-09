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
import os
import threading
import urllib
import time
from daemon.weaprous import WeApRous

PORT = 8000  # Default port

app = WeApRous()
users_lock = threading.Lock()
active_peers = {}
peers_lock = threading.Lock()
active_connections = {}

import json



from daemon.response import Response
# users = {
#     "tien": "deptraiqua",
#     "admin": "password"
# }

@app.route('/login', methods=['POST'])
def login(headers="guest", body="anonymous"):
    
    print("[SampleApp] Handling POST /login request.")
    if isinstance(body, str):
        # thử parse JSON trước
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            # Nếu không phải JSON, parse form-urlencoded
            body = dict(urllib.parse.parse_qsl(body))

    username = body.get('username')
    password = body.get('password')

    print(f"[SampleApp] Login attempt - User: {username}, Pass: {password}")
    
    is_valid = (username == "tien" and password == "deptraiqua") or \
               (username == "admin" and password == "password")

    if is_valid:
        print(f"[SampleApp] User '{username}' authenticated successfully.")
        # ...
        return 'Login Success'
    else:
        print(f"[SampleApp] Authentication failed for user '{username}'.")
        return 'Login Fail'

# def login(headers="guest", body="anonymous"):
#     import json

#     print("[SampleApp] Handling POST /login request.")

#     try:
#         if isinstance(body, str):
#             body = json.loads(body)
#     except json.JSONDecodeError:
#         body = {}

#     username = body.get('username')
#     password = body.get('password')

#     print(f"[SampleApp] Login attempt - User: {username}, Pass: {password}")

#     is_valid = False
#     with users_lock:
#         if username == "admin" and password == "password":
#             is_valid = True

#     if is_valid:
#         html_content = """
#         <html>
#             <head>
#                 <meta http-equiv="refresh" content="0;url=/index.html">
#              </head>
#             <body></body>
#         </html>
#     """
#         cookie_to_set = "auth=true"
#         return (html_content, cookie_to_set)

#     else:
#         print(f"[SampleApp] Authentication failed for user '{username}'.")
#         html_content = "<html><body><h1>401 Unauthorized</h1><p>Invalid username or password.</p></body></html>"
#         cookie_to_set = None
#         return (html_content, cookie_to_set)




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