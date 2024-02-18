from sqlmodel import SQLModel


class TokenSchema(SQLModel):
    access_token: str
    refresh_token: str


class TokenPayload(SQLModel):
    exp: int
    sub: str
