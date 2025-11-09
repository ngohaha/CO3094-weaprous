#
# Copyright (C) 2025 pdnguyen of HCMC University of Technology VNU-HCM.
# All rights reserved.
# This file is part of the CO3093/CO3094 course.
#
# WeApRous release
#
# The authors hereby grant to Licensee personal permission to use
# and modify the Licensed Source Code for the sole purpose of studying
# while attending the course
#

"""
daemon.request
~~~~~~~~~~~~~~~~~

This module provides a Request object to manage and persist 
request settings (cookies, auth, proxies).
"""
from .dictionary import CaseInsensitiveDict
from .utils import get_auth_from_url

class Request():
    """The fully mutable "class" `Request <Request>` object,
    containing the exact bytes that will be sent to the server.

    Instances are generated from a "class" `Request <Request>` object, and
    should not be instantiated manually; doing so may produce undesirable
    effects.

    Usage::

      >>> import deamon.request
      >>> req = request.Request()
      ## Incoming message obtain aka. incoming_msg
      >>> r = req.prepare(incoming_msg)
      >>> r
      <Request>
    """
    __attrs__ = [
        "method",
        "url",
        "headers",
        "body",
        "reason",
        "cookies",
        "body",
        "routes",
        "hook",
        "auth",
        "body_override",
        "content_type_override"
    ]

    def __init__(self):
        #: HTTP verb to send to the server.
        self.method = None
        #: HTTP URL to send the request to.
        self.url = None
        #: dictionary of HTTP headers.
        self.headers = None
        #: HTTP path
        self.path = None        
        # The cookies set used to create Cookie header
        self.cookies = None
        #: request body to send to the server.
        self.body = None
        #: Routes
        self.routes = {}
        #: Hook point for routed mapped-path
        self.hook = None
        
        self.auth = False

        self.body_override = None

        self.content_type_override = None

    def extract_request_line(self, request):
        try:
            lines = request.splitlines()
            first_line = lines[0]
            method, path, version = first_line.split()

            if path == '/':
                path = '/index.html'
        except Exception:
            return None, None

        return method, path, version
             
    def prepare_headers(self, request):
        """Prepares the given HTTP headers."""
        lines = request.split('\r\n')
        headers = {}
        for line in lines[1:]:
            if ': ' in line:
                key, val = line.split(': ', 1)
                headers[key.lower()] = val
        return headers

    def prepare(self, request, routes=None):
        """Prepares the entire request with the given parameters."""

        # Prepare the request line from the request header
        self.method, self.path, self.version = self.extract_request_line(request)
        print(("[Request] {} path {} version {}".format(self.method, self.path, self.version)))

        #
        # @bksysnet Preapring the webapp hook with WeApRous instance
        # The default behaviour with HTTP server is empty routed
        #
        # TODO manage the webapp hook in this mounting point
        #
        
        if not routes == {}:
            self.routes = routes
            self.hook = routes.get((self.method, self.path))

            if self.hook: 
                self.hook()
            #
            # self.hook manipulation goes here
            # ...
            #

        self.headers = self.prepare_headers(request)
        self.body = self.prepare_body(request)
        cookies = self.headers.get('cookie', '')
        # self.cookies = self.parse_cookies(cookies)
            #
            #  TODO: implement the cookie function here
            #        by parsing the header            #
        self.headers["Cookie"] = self.prepare_cookies(self.headers)
        return
    
    def parse_cookies(self, cookie_header):
        cookies = {}
        if not cookie_header:
            return cookies

        cookie_pairs = cookie_header.split('; ')
        for pair in cookie_pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                cookies[key] = value
        return cookies

    def prepare_body(self, request):
        # if json is not None:
        #     import json as jsonlib
        #     self.body = jsonlib.dumps(json)
        #     self.headers["Content-Type"] = "application/json"
        # elif data is not None:
        #     self.body = data
        #     self.headers["Content-Type"] = "application/x-www-form-urlencoded"
        # else:
        #     self.body = ''
        data_form = {}
        if self.path == '/connect':
            try: 
                first_line = request.splitlines()[0]
                _, full_path, _ = first_line.split()
                if '?' in full_path:
                    path, query = full_path.split('?', 1)
                    pairs = query.split('&')
                    for p in pairs:
                        if '=' in p:
                            key, value = p.split('=', 1)
                            data_form[key] = value
                return data_form
            except Exception as e:
                print(("[Request] Connect parse error: {}".format(e)))
        else:
            try:
                header_part, body_part = request.split('\r\n\r\n', 1)
            except ValueError:
                return None
            pairs = body_part.split('&')
            for p in pairs:
                if '=' in p:
                    key, value = p.split('=', 1)
                    data_form[key] = value
            
            return data_form

        # self.prepare_content_length(self.body)
        # self.body = body
        #
        # TODO prepare the request authentication
        #
	# self.auth = ...
        # return


    def prepare_content_length(self, body):
        # self.headers["Content-Length"] = "0"
        #
        # TODO prepare the request authentication
        #
	# self.auth = ...
        if body:
            self.headers["Content-Length"] = str(len(body))
        else:
            self.headers["Content-Length"] = "0"
        return


    def prepare_auth(self, auth, url=""):
        #
        # TODO prepare the request authentication
        #
	# self.auth = ...
        # if not auth:
        #     return
        # if isinstance(auth, tuple):
        #     username, password = auth
        #     auth_str = f"{username}:{password}"
        #     auth_bytes = auth_str.encode('utf-8')
        #     encode = base64.b64encode(auth_bytes).decode('ascii')
        #     self.headers["Authorization"] = f"Basic {encode}"
        # else:
        #     auth_header = auth.get_authorization_header(url)
        #     if auth_header:
        #         self.headers["Authorization"] = auth_header
        # self.auth = get_auth_from_url(url)
        # return
        return

    def prepare_cookies(self, cookies):
        # if not cookies:
        #     return
        # if isinstance(cookies, dict):
        #     cookies_header = '; '.join(f"{k}={v}" for k, v in cookies.items())
        # else:
        #     cookies_header = str(cookies)
        # self.headers["Cookie"] = cookies_header
        cookies = self.headers.get('cookie', '')
        print("[Request-Cookie]: " + cookies if cookies != '' else "No cookie" )
        return cookies
