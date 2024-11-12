import asyncio


async def receive_messages(reader):
    """Receive and print messages from the server."""
    while True:
        data = await reader.read(1024)
        if data:
            print(data.decode())


async def send_message(writer, message):
    """Send a message to the server."""
    writer.write(message.encode())
    await writer.drain()


async def main():
    nickname = input("Choose a nickname: ")

    reader, writer = await asyncio.open_connection('localhost', 5556)

    # Wait for the NICK prompt from the server
    data = await reader.read(100)
    if data == b'NICK':
        writer.write(nickname.encode())
        await writer.drain()

    # Start receiving messages
    asyncio.create_task(receive_messages(reader))

    while True:
        message = input(f"{nickname}: ")
        await send_message(writer, message)


if __name__ == '__main__':
    asyncio.run(main())
