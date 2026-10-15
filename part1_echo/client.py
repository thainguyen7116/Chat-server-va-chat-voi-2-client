
import asyncio


async def main():
    reader, writer = await asyncio.open_connection(
        "127.0.0.1", 8888
    )

    print("Da ket noi den server!")
    print("Nhap exit de thoat.")

    try:
        while True:
            message = await asyncio.to_thread(
                input, "Ban: "
            )

            if message.lower() == "exit":
                break

            writer.write(
                (message + "\n").encode("utf-8")
            )
            await writer.drain()

            data = await reader.readline()
            print("Server tra loi:", data.decode("utf-8").strip())

    finally:
        writer.close()
        await writer.wait_closed()


asyncio.run(main())
