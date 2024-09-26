import asyncio
import websockets

# 存储所有连接的客户端
clients = set()

async def chat_server(websocket, path):
    clients.add(websocket)
    async for message in websocket:
        # 接收客户端发送的消息
        print(f"Received message: {message}")

        # 将消息发送给所有连接的客户端
        await asyncio.gather(*[client.send(message) for client in clients])

async def handler(websocket, path):
    # 添加新连接客户端到列表
    print("Client handler started")
    clients.add(websocket)
    try:
        async for message in websocket:
            # 遍历客户端列表并广播消息
            for client in clients:
                print(f"Sending message to {message}")
                if client != websocket:
                    await client.send(message)
    finally:
        # 移除断开连接的客户端
        print("Client disconnected")
        clients.remove(websocket)

start_server = websockets.serve(handler, "0.0.0.0", 3000)

# 添加以下代码来执行WebSocket服务器

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()