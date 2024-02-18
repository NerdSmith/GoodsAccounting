from sqlmodel import SQLModel


class TokenSchemaAccess(SQLModel):
    access_token: str


class TokenSchemaRefresh(SQLModel):
    refresh_token: str


class TokenSchema(TokenSchemaAccess, TokenSchemaRefresh):
    pass


class TokenPayload(SQLModel):
    exp: int
    sub: str
