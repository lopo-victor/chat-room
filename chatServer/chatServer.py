import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from models import Mensagem, Chatroom
import httpx
from typing import Dict

app = FastAPI()

USERSERVER_URL = 'http://chat-room_user_server_1:8000/validate_token'

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.chatroom = Chatroom(id=1, chat=[])

    async def connect(self, token: str, websocket: WebSocket):
        async with httpx.AsyncClient() as client:
            response = await client.post(USERSERVER_URL, json={"token": token})
            response_data = response.json()
        
        if response.status_code != 200 or not response_data.get('valid'):
            raise HTTPException(status_code=401, detail="Invalid token")

        username = response_data.get('username')
        await websocket.accept()
        self.active_connections[username] = websocket
        return username

    def disconnect(self, username: str):
        if username in self.active_connections:
            del self.active_connections[username]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)
            


manager = ConnectionManager()

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, token: str):
    username = None
    try:
        username = await manager.connect(token, websocket)
        while True:
            mensagem_json = await websocket.receive_text()
            mensagem_dict = json.loads(mensagem_json)
            mensagem = Mensagem(usuario=mensagem_dict['usuario'], texto=mensagem_dict['texto'])
            manager.chatroom.adicionar_mensagem(mensagem)
            await manager.broadcast(mensagem_json)

    except WebSocketDisconnect:
        if username:
            manager.disconnect(username)
    except HTTPException as e:
        await websocket.close(code=e.status_code)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8001)
