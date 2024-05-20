from dataclasses import dataclass


@dataclass
class RequestLine:
    method: str
    path: str
    http_version: str

    @classmethod
    def from_str(cls, string):
        return cls(*string.split(" "))


@dataclass
class RequestHeaders:
    host: str
    user_agent: str = None
    accept: str = None
    content_lenght: int = None
    content_type: str = None

    @classmethod
    def from_list(cls, elements):
        values = [element.split(" ")[1] for element in elements]
        return cls(*values)


def parse_request(request: bytes) -> tuple[RequestLine, RequestHeaders, str]:
    string_request = request.decode(encoding="utf-8")
    print(f"Decoded request: {string_request}")
    try:
        request_line_and_headers, body = string_request.split("\r\n\r\n")
    except ValueError:
        print("WARNING: Did not find any body")
        request_line_and_headers = string_request.split("\r\n\r\n")
    print(f"Split request: {request_line_and_headers=}")
    request_elements = request_line_and_headers.split("\r\n")
    print(f"{request_elements=}")
    request_line = RequestLine.from_str(request_elements[0])
    headers = RequestHeaders.from_list(request_elements[1:])
    return request_line, headers, body
