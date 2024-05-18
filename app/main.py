# Uncomment this to pass the first stage
import socket
from dataclasses import dataclass
from typing import Optional


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
    user_agent: str
    accept: str

    @classmethod
    def from_list(cls, elements):
        values = [element.split(" ")[1] for element in elements]
        return cls(*values)


@dataclass
class ResponseHeaders:
    content_type: str
    content_length: int

    def to_str(self):
        return f"Content-Type: {self.content_type}\r\nContent-Length: {self.content_length}\r\n"


@dataclass
class Response:
    version: str
    status_code: int
    status_message: str

    headers: Optional[ResponseHeaders] = None

    body: Optional[str] = None

    def to_str(self) -> str:
        string = f"{self.version} {self.status_code} {self.status_message}\r\n"
        if self.headers is not None:
            string += self.headers.to_str()
        string += "\r\n"
        if self.body:
            string += self.body
        return string

    def to_bytes(self) -> bytes:
        string = self.to_str()
        return bytes(string, "utf-8")


def parse_request(request: bytes) -> tuple[RequestLine, RequestHeaders]:
    request_line_and_headers, _ = str(request).split(r"\r\n\r\n")
    request_elements = request_line_and_headers.split(r"\r\n")
    request_line = RequestLine.from_str(request_elements[0])
    headers = RequestHeaders.from_list(request_elements[1:])
    return request_line, headers


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is running on port 4221")
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    request = client_socket.recv(1024)
    request_line, request_headers = parse_request(request=request)
    print(f"{request_line=}")
    print(f"{request_headers=}")

    if request_line.path == "/":
        # Return 200
        response = Response(version="HTTP/1.1", status_code=200, status_message="OK")
    elif request_line.path.startswith("/echo/"):
        # return everything after "echo/"
        body = request_line.path.split("/", maxsplit=2)[-1]
        content_length = len(body)
        resp_headers = ResponseHeaders(
            content_length=content_length, content_type="plain/text"
        )
        response = Response(
            version="HTTP/1.1",
            status_code=200,
            status_message="OK",
            headers=resp_headers,
            body=body,
        )
    else:
        response = Response(
            version="HTTP/1.1", status_code=404, status_message="Not Found"
        )

    client_socket.sendall(response.to_bytes())


if __name__ == "__main__":
    main()
