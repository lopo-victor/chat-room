from pydantic import BaseModel

class Mesnsagem(BaseModel):
    usuario: str
    texto: str


class Chatroom(BaseModel):
    id: int
    chat: list[Mesnsagem]
    
    def printChat(self):
        for mensagem in self.chat:
            linha = f"{mensagem.usuario}: {mensagem.texto}"
            print(linha)