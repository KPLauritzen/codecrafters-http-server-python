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

    @classmethod
    def from_list(cls, elements):
        print(f"request headers: {elements}")
        values = [element.split(" ")[1] for element in elements]
        return cls(*values)


def parse_request(request: bytes) -> tuple[RequestLine, RequestHeaders]:
    request_line_and_headers, _ = str(request).split(r"\r\n\r\n")
    request_elements = request_line_and_headers.split(r"\r\n")
    request_line = RequestLine.from_str(request_elements[0])
    headers = RequestHeaders.from_list(request_elements[1:])
    return request_line, headers
