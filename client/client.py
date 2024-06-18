import requests
import websocket
import threading
import json
from models import Mensagem

connection_open = True

# Função para processar mensagens recebidas do servidor
def on_message(ws, message):
    if not message.strip():
        print("Mensagem vazia recebida.")
        return
    try:
        data = json.loads(message)
        print(f"Nova mensagem de {data['usuario']}: {data['texto']}")
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")

# Função para lidar com erros de conexão
def on_error(ws, error):
    print(f"Erro!!: {error}")

# Função para lidar com o fechamento da conexão 
def on_close(ws, close_status_code, close_msg):
    global connection_open
    print(f"Conexão fechada com código {close_status_code}: {close_msg}")
    connection_open = False

# Função para lidar com a abertura da conexão
def on_open(ws):
    def run():
        global connection_open
        while connection_open:
            try:
                global usuariox
                mensagem = input()
                msg = Mensagem(usuario=usuariox, texto=mensagem)
                ws.send(json.dumps(msg.dict()))

            except websocket.WebSocketConnectionClosedException:
                print("Conexão fechada durante o envio. Encerrando.")
                connection_open = False
                break
            except Exception as e:
                print(f"Erro durante o envio da mensagem: {e}")

    threading.Thread(target=run).start()

cadastro=input("Login[1]  Cadastro[2]: ")
usuariox=input("Usuario: ")
senha=input("senha: ")

if cadastro==2:
    r = requests.post('http://chat-room_user_server_1:8000/register', json={
        "nome": usuariox,
        "senha": senha
    }) 
    
response = requests.post('http://chat-room_user_server_1:8000/login', json={
    "nome": usuariox,
    "senha": senha
})

if response.status_code == 200:
    data = response.json()
    token = data['token']
    chatserver = data['chatserver']
    
    print(f"Conectando ao chatserver em {chatserver} com token {token}")
    print()

    # Conectar ao chatserver usando WebSockets
    ws = websocket.WebSocketApp(
        f"ws://{chatserver}/chat?token={token}",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )

    ws.run_forever()

else:
    print("Falha ao autenticar!")
