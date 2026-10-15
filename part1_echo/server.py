
import asyncio


async def handle_client(reader, writer):
    print("Co client ket noi")

    try:
        while True:
            data = await reader.readline()

            if not data:
                break

            message = data.decode("utf-8").strip()
            print("Server nhan duoc:", message)

            writer.write(data)
            await writer.drain()

    finally:
        writer.close()
        await writer.wait_closed()
        print("Client da ngat ket noi")


async def main():
    server = await asyncio.start_server(
        handle_client,
        "127.0.0.1",
        8888
    )

    print("Server dang chay tai cong 8888")

    async with server:
        await server.serve_forever()


asyncio.run(main())
