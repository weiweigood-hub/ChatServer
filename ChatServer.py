import socket
import threading

# 設定伺服器的IP和Port
HOST = '127.0.0.1'
PORT = 12345

# 建立一個socket物件
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# 廣播訊息給所有客戶端
def broadcast(message):
    for client in clients:
        client.send(message)

# 處理客戶端訊息
def handle_client(client):
    while True:
        try:
            # 接收訊息
            message = client.recv(1024)
            broadcast(message)
        except:
            # 移除並關閉客戶端
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} 離開了聊天室!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# 接受新連接
def receive():
    while True:
        client, address = server.accept()
        print(f"連接來自 {str(address)}")

        # 請求並儲存暱稱
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # 廣播並回報新連接
        print(f'暱稱是 {nickname}')
        broadcast(f'{nickname} 加入了聊天室!'.encode('utf-8'))
        client.send('連接到伺服器!'.encode('utf-8'))

        # 開始處理客戶端訊息的執行緒
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("伺服器正在運行...")
receive()