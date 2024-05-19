from dataclasses import dataclass
from typing import Optional

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

