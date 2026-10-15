
import asyncio

# Luu cac client dang ket noi
clients = {}


async def broadcast(message, sender=None):
    # Gui tin nhan den cac client khac
    for writer in list(clients.keys()):
        if writer is sender:
            continue

        try:
            writer.write((message + "\n").encode("utf-8"))
            await writer.drain()
        except (ConnectionError, OSError):
            pass


async def handle_client(reader, writer):
    username = None

    try:
        # Dong dau tien la ten nguoi dung
        data = await reader.readline()

        if not data:
            return

        username = data.decode("utf-8").strip()
        if not username:
            username = "Khach"

        clients[writer] = username
        print(f"{username} da ket noi")

        await broadcast(f"[He thong] {username} da tham gia chat!")

        while True:
            data = await reader.readline()

            if not data:
                break

            message = data.decode("utf-8").strip()

            if message:
                print(f"{username}: {message}")
                await broadcast(f"{username}: {message}", sender=writer)

    except (ConnectionError, OSError) as error:
        print("Loi ket noi:", error)

    finally:
        clients.pop(writer, None)

        if username:
            print(f"{username} da roi chat")
            await broadcast(f"[He thong] {username} da roi chat.")

        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(
        handle_client,
        "127.0.0.1",
        8889
    )

    print("Chat Server dang chay tai cong 8889")

    async with server:
        await server.serve_forever()


asyncio.run(main())
