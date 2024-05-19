# Uncomment this to pass the first stage
import socket
from app.request import parse_request
from app.routes import echo_route, root_route, unknown_route, user_agent_route


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is running on port 4221")
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    request = client_socket.recv(1024)
    print(f"{request=}")
    request_line, request_headers = parse_request(request=request)
    print(f"{request_line=}")
    print(f"{request_headers=}")

    if request_line.path == "/":
        response = root_route()
    elif request_line.path.startswith("/echo/"):
        response = echo_route(request_line=request_line)
    elif request_line.path.startswith("/user-agent"):
        response = user_agent_route(request_headers=request_headers)
    else:
        response = unknown_route()
    print("response: ", response)
    client_socket.sendall(response.to_bytes())


if __name__ == "__main__":
    main()
