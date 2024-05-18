# Uncomment this to pass the first stage
import socket
from dataclasses import dataclass


@dataclass
class RequestLine:
    method: str
    path: str
    http_version: str

    @classmethod
    def from_str(cls, string):
        elems = string.split(" ")
        print(elems)
        return cls(*elems)


def parse_request(request: bytes) -> RequestLine:
    request_elements = str(request).split(r"\r\n")
    request_line = RequestLine.from_str(request_elements[0])
    return request_line


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is running on port 4221")
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    request = client_socket.recv(1024)
    request_line = parse_request(request=request)

    if request_line.path == "/":
        client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    main()
