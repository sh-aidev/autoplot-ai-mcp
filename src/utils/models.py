from pydantic import BaseModel


class Logger(BaseModel):
    environment: str


class Server(BaseModel):
    name: str


class AppConfig(BaseModel):
    logger: Logger
    server: Server
