from pydantic import BaseModel

class Usuario(BaseModel):
    nome: str
    senha: str

class Token(BaseModel):
    token: str