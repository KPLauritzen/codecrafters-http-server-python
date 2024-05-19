import os
from app.request import RequestHeaders
from app.response import Response, ResponseHeaders


def root_route():
    return Response(version="HTTP/1.1", status_code=200, status_message="OK")


def unknown_route():
    return Response(version="HTTP/1.1", status_code=404, status_message="Not Found")


def echo_route(request_line):
    # return everything after "echo/"
    body = request_line.path.split("/", maxsplit=2)[-1]
    content_length = len(body)
    resp_headers = ResponseHeaders(
        content_length=content_length, content_type="text/plain"
    )
    return Response(
        version="HTTP/1.1",
        status_code=200,
        status_message="OK",
        headers=resp_headers,
        body=body,
    )


def user_agent_route(request_headers: RequestHeaders):
    body = request_headers.user_agent
    content_length = len(body)
    resp_headers = ResponseHeaders(
        content_length=content_length, content_type="text/plain"
    )
    return Response(
        version="HTTP/1.1",
        status_code=200,
        status_message="OK",
        headers=resp_headers,
        body=body,
    )


def files_route(directory: str, request_line):
    filename = request_line.path.split("/", maxsplit=2)[-1]
    full_path = f"{directory}/{filename}"
    if not os.path.exists(full_path):
        return unknown_route()
    with open(full_path, "r") as f:
        contents = f.read()
    content_length = len(contents)
    resp_headers = ResponseHeaders(
        content_length=content_length, content_type="application/octet-stream"
    )
    return Response(
        version="HTTP/1.1",
        status_code=200,
        status_message="OK",
        headers=resp_headers,
        body=contents,
    )
