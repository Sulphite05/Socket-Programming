import asyncio

clients = {}

async def broadcast(message, sender=None):
    """Broadcast the message to all connected clients except the sender."""
    for client, nickname in clients.items():
        if nickname != sender:
            client.write(message)
            await client.drain()

async def handle_client(reader, writer):
    """Handles a client connection."""
    addr = writer.get_extra_info('peername')
    print(f"New connection from {addr}")

    # Request nickname
    writer.write(b"NICK")
    await writer.drain()

    data = await reader.read(100)
    nickname = data.decode()

    clients[writer] = nickname
    broadcast_message = f"{nickname} joined the chat!".encode()

    # Broadcast to all other clients
    await broadcast(broadcast_message, nickname)

    while True:
        try:
            # Receive message
            data = await reader.read(1024)
            if not data:
                break

            message = data.decode()
            print(f"Received from {nickname}: {message}")

            # Broadcast the message to others
            message_to_send = f"{nickname}: {message}".encode()
            await broadcast(message_to_send, nickname)

        except Exception as e:
            print(f"Error handling client {nickname}: {e}")
            break

    # Remove client on disconnect
    del clients[writer]
    print(f"{nickname} disconnected.")
    await broadcast(f"{nickname} left the chat!".encode(), nickname)
    writer.close()
    await writer.wait_closed()

async def main():
    """Main entry point for server."""
    server = await asyncio.start_server(handle_client, 'localhost', 5556)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())