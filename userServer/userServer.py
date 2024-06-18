import json
import os
from fastapi import FastAPI, HTTPException
from us_models import Usuario
from us_models import Token
import uuid

USER_DATA_FILE = '/data/userData.json'

app = FastAPI()

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {"users": {}, "sessions": {}}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.post("/login")
async def login(user: Usuario):
    data = load_user_data()
    if data['users'].get(user.nome) == user.senha:
        session_token = str(uuid.uuid4())
        data['sessions'][session_token] = user.nome
        save_user_data(data)
        return {"token": session_token, "chatserver": "chat-room_chat_server_1:8001"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/validate_token")
async def validate_token(token: Token):
    data = load_user_data()
    if token.token in data['sessions']:
        return {"valid": True, "username": data['sessions'][token.token]}
    raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/register")
async def register(user: Usuario):
    data = load_user_data()
    if user.nome in data['users']:
        raise HTTPException(status_code=400, detail="Username already exists")
    data['users'][user.nome] = user.senha
    save_user_data(data)
    return {"message": "User registered successfully"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
