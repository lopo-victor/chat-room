from pydantic import BaseModel

class Mensagem(BaseModel):
    usuario: str
    texto: str


class Chatroom(BaseModel):
    id: int
    chat: list[Mensagem]

    def adicionar_mensagem(self, mensagem: Mensagem):
        self.chat.append(mensagem)    
    
    def printChat(self):
        for mensagem in self.chat:
            linha = f"{mensagem.usuario}: {mensagem.texto}"
            print(linha)