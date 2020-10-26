"""
This modules has functions to handle all the supported commands for the
codetime server's APIs.
"""
from .models import User, TimeLog
from .serializers import UserSerializer, TimeLogSerializer


def get_missing_param_response(data=None):
    """
    Returns error response for missing parameters

    :param str data: message
    :return: response
    :rtype: object
    """
    return {"status": 400, "message": "Missing query parameter.", "data": data}


def get_serializer_error_response(error):
    """
    Returns error response from serializer

    :param str error: message
    :return: error_response
    :rtype: object
    """
    error_response = {"status": 422, "data": [], "message": error}
    return error_response


def get_invalid_request_param(message):
    """
    Returns error response for invalid request parameters

    :param str error: message
    :return: error_response
    :rtype: object
    """
    error_response = {"status": 400, "data": [], "message": message}
    return error_response


def get_valid_output_response(data):
    """
    Returns success message correct processing of post/get request

    :param str data: message
    :return: response
    :rtype: object
    """
    response = {"status": 200, "message": "Success", "data": data}

    return response


def get_valid_post_response():
    """
    Returns success message correct processing of post/get request

    :param str data: message
    :return: response
    :rtype: object
    """
    response = {"status": 201, "message": "Created"}

    return response


def get_something_went_wrong_response(data=None):
    """
    Returns error response for server related error

    :param str data: message
    :return: response
    :rtype: object
    """
    response = {"status": 500, "message": "Something went wrong", "data": data}

    return response


def get_invalid_user_credentials(data=None):
    """
    Returns error response for invalid user credentials

    :param str data: message
    :return: response
    :rtype: object
    """
    response = {"status": 1, "message": "Invalid user credentials.", "data": data}

    return response


def handle_user_post(request):
    """
    Handler for post request made by a user to signup and login

    :param HTTP POST request: message
    :return: response
    :rtype: object
    """
    request_type = request.query_params.get("type", None)

    if request_type is None:
        return get_missing_param_response()

    if request_type == "login" or request_type == "signup":

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            if request_type == "signup":
                return_status = User.objects.create_user(request.data)

                if return_status == 0:
                    data = User.objects.get_user_from_username(
                        request.data["username"], request.data["password"]
                    )
                    return get_valid_output_response(data)
                elif return_status == 1:
                    return get_something_went_wrong_response(request.data)
                elif return_status == 2:
                    return {"status": 1, "message": "Username already taken.", "data": request.data}
            elif request_type == "login":

                return_status = User.objects.get_user_from_username(
                    request.data["username"], request.data["password"]
                )

                if return_status:
                    return get_valid_post_response()
                else:
                    return get_invalid_user_credentials(request.data)
        else:
            return get_serializer_error_response(serializer.errors)

    else:
        return get_invalid_request_param('Invalid value for url param "type".')


def handle_log_file_post(request):
    """
    Handler for post request made by logging files

    :param HTTP POST request: request
    :return: response
    :rtype: object
    """
    return_data = dict()
    return_data["created"] = []
    return_data["failed"] = []
    return_status = 200

    for data_point in request.data:

        serializer = TimeLogSerializer(data=data_point)

        if serializer.is_valid():
            creation_status = TimeLog.objects.create_log(serializer.data)
            if not creation_status:
                return_data["created"].append(serializer.data)
            else:
                return_status = 500
                return_data["failed"].append(data_point)
        else:
            return_status = 422
            return_data["failed"].append(data_point)

    return {"status": return_status, "message": "", "data": return_data}


def handle_get_file_logs(request):
    """
    Handler for get request to obtain all records for a user.

    :param HTTP GET request: request
    :return: response
    :rtype: object
    """
    user_api_token = request.query_params.get("api_token", None)
    if user_api_token is not None:
        response = TimeLog.objects.get_time_logs(user_api_token)
        if isinstance(response, list):
            return get_valid_output_response(response)
        else:
            return get_invalid_request_param(response)
    else:
        return get_missing_param_response("api_token")
