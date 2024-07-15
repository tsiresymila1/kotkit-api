from dataclasses import dataclass


@dataclass
class LoginDto:
    username: str
    password: str


@dataclass
class RegisterDto(LoginDto):
    name: str
    email: str
