# CHATROOM

## Descrição

O projeto implementa uma sala de chat em tempo real usando FastAPI, WebSockets e uma interface de linha de comando (CLI) para os clientes. A solução abrange tanto a autenticação de usuários quanto a comunicação em tempo real entre clientes conectados ao chat.

## Componentes Principais

### Servidor de Autenticação (User Server)
- **Endpoints**:
  - `/register`: Permite o registro de novos usuários com nome de usuário e senha.
  - `/login`: Autentica usuários existentes e fornece um token de sessão para acesso ao chat.
  - `/validate_token`: Valida os tokens de sessão para assegurar que apenas usuários autenticados possam se conectar ao servidor de chat.
- **Armazenamento de Dados**:
  - Os dados dos usuários (nomes de usuário e senhas) e sessões ativas são armazenados em um arquivo JSON.

### Servidor de Chat (Chat Server)
- Implementado usando FastAPI e WebSockets.
- Gerencia conexões WebSocket para permitir a comunicação em tempo real entre os usuários.
- **ConnectionManager**:
  - Gerencia as conexões ativas.
  - Valida os tokens de sessão recebidos dos clientes.
  - Envia e transmite mensagens entre os usuários conectados.

### Cliente CLI
- Implementado em Python.
- Permite que os usuários se registrem, façam login e participem da sala de chat via terminal.
- Utiliza a biblioteca `websocket-client` para gerenciar a conexão WebSocket com o servidor de chat.
- **Funções Principais**:
  - `on_message`: Processa e exibe mensagens recebidas do servidor de chat.
  - `on_error`: Lida com erros de conexão.
  - `on_close`: Lida com o fechamento da conexão.
  - `on_open`: Gera um thread que permite ao usuário enviar mensagens para o chat.

## Fluxo de Trabalho

1. **Registro e Login**:
   - O usuário é solicitado a escolher entre login (1) ou cadastro (2).
   - Para cadastro, uma solicitação POST é enviada ao endpoint `/register` do servidor de autenticação.
   - Para login, uma solicitação POST é enviada ao endpoint `/login`. Se bem-sucedida, o servidor retorna um token de sessão e o endereço do servidor de chat.

2. **Conexão ao Chat**:
   - O cliente CLI se conecta ao servidor de chat usando o token de sessão via WebSocket.
   - Uma vez conectado, o cliente pode enviar e receber mensagens em tempo real.
