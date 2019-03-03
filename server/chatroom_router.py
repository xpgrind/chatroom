import flask
from flask import Flask, jsonify
from functools import wraps
from sqlalchemy.sql import text
from pprint import pprint
import traceback

from chatroom.db.session import get_session

client_address = "http://localhost:8080"


def create_response(headers, data, status):
    print("Creating response: {} {}".format(data, status))
    response = flask.jsonify(data)
    h = response.headers
    for k, v in headers.items():
        h[k] = v
    response.status_code = status
    return response


class ChatroomRouter:
    def __init__(self, app):
        self.app = app

    def route(self, rule, *args, **kwargs):
        # This has the arguments
        string_methods = ', '.join(sorted(x.upper() for x in kwargs['methods']))
        requires_login = kwargs.pop('requires_login', True)
        create_db_session = kwargs.pop('db', False)

        allowed_headers = ['Content-type']
        string_headers = ', '.join(x.upper() for x in allowed_headers)

        def function_wrapper(f):
            print("Inside Wrapper" + f.__name__)

            @wraps(f)
            def route_call(*fargs, **fkwargs):
                method = flask.request.method
                print("\n{} call on route: {}".format(method, f.__name__))

                headers = {
                    'Access-Control-Allow-Origin': client_address,
                    'Access-Control-Allow-Methods': string_methods,
                    'Access-Control-Max-Age': '21600',
                    'Access-Control-Allow-Headers': string_headers,
                    'Access-Control-Allow-Credentials': 'true',
                    'Content-type': "application/json",
                }

                # If this is an OPTIONS request, we handle it manually and never pass it to the route function.
                if method == "OPTIONS":
                    response = flask.current_app.make_default_options_response()
                    response.status_code = 200
                    h = response.headers
                    for k, v in headers.items():
                        h[k] = v
                    return response

                if requires_login or create_db_session:
                    db_session = get_session()
                else:
                    db_session = None

                # If this is a GET or POST request, f will be called.
                if requires_login:
                    ### Validate token
                    json_data = flask.request.json
                    print("Got login info: ")
                    pprint(json_data)

                    if json_data is None:
                        return create_response(headers, {"success": False, "reason": "no POST json data"}, 403)

                    user_token = json_data.get('token')
                    if user_token is None:
                        return create_response(headers, {"success": False, "reason": "no token in POST data"}, 403)

                    if not isinstance(user_token, str):
                        return create_response(headers, {"success": False, "reason": "token should be a str"}, 403)

                    user_id = json_data.get('user_id')
                    if user_id is None:
                        return create_response(headers, {"success": False, "reason": "no user_id in POST data"}, 403)

                    if not isinstance(user_id, int):
                        return create_response(headers, {"success": False, "reason": "user_id should be an int"}, 403)

                    prepared_statement = text('select token_string from token where user_id = :user_id and token_string = :user_token and expire_time > current_timestamp order by expire_time desc limit 1')
                    token_rows = db_session.execute(prepared_statement, {'user_id': user_id, 'user_token': user_token})
                    token_row = token_rows.first()
                    if not token_row:
                        return create_response(headers, {"success": False, "reason": "Invalid user_id or token"}, 403)

                    ### End Validate token

                response = None

                # Token verification succeeded, continue:
                print("Starting Call to function " + f.__name__)
                try:
                    if create_db_session:
                        # Any arguments to pass to the route function can be passed here.
                        # I am passing the database so that a new connection is not required every time.
                        res = f(db_session)
                    else:
                        res = f()
                except (KeyboardInterrupt, SystemExit):
                    print("Quitting")
                    raise
                except AssertionError as e:
                    print("Assertion Error in route: {}".format(f.__name__))
                    print("Failed Assertion: {}".format(e))
                    res = flask.jsonify({
                        "success": False,
                        "message": str(e)
                    }), 400
                except Exception as e: #pylint: disable=broad-except
                    print("Uncaught exception in route: {}".format(f.__name__))
                    print("Type: {}, Exception: {}".format(type(e), e))
                    traceback.print_exc()
                    res = flask.jsonify({
                        "success": False,
                        "message": "Unhandled exception"
                    }), 500

                # Allow returning like return response or return response, status_code
                if isinstance(res, tuple):
                    response = res[0]
                    response.status_code = res[1]
                else:
                    response = res

                h = response.headers
                for k, v in headers.items():
                    h[k] = v

                if db_session is not None:
                    db_session.close()

                # print("Final Response Headers:")
                # print(response.headers)

                print("[{}] Done Call to function: {}".format(response.status_code, f.__name__))
                return res

            # This bit right here is what is required to add the route to flask in the end.
            endpoint = kwargs.pop('endpoint', None)
            self.app.add_url_rule(rule, endpoint, route_call, **kwargs)
            return f

        return function_wrapper
