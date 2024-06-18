from pydantic import BaseModel

class Mensagem(BaseModel):
    usuario: str
    texto: str


class Chatroom(BaseModel):
    id: int
    chat: list[Mensagem]
    
    def printChat(self):
        for mensagem in self.chat:
            linha = f"{mensagem.usuario}: {mensagem.texto}"
            print(linha)