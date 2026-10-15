
import asyncio


async def receive_messages(reader):
    while True:
        data = await reader.readline()

        if not data:
            break

        print("\n" + data.decode("utf-8").strip())


async def main():
    reader, writer = await asyncio.open_connection(
        "127.0.0.1", 8889
    )

    username = await asyncio.to_thread(
        input, "Nhap ten cua ban: "
    )

    writer.write((username + "\n").encode("utf-8"))
    await writer.drain()

    # Doc tin nhan trong mot Task rieng
    receive_task = asyncio.create_task(
        receive_messages(reader)
    )

    print("Da vao phong chat. Go /exit de thoat.")

    try:
        while True:
            message = await asyncio.to_thread(
                input, "Ban: "
            )

            if message.strip().lower() == "/exit":
                break

            if message.strip():
                writer.write(
                    (message + "\n").encode("utf-8")
                )
                await writer.drain()

    finally:
        writer.close()
        await writer.wait_closed()

        receive_task.cancel()
        await asyncio.gather(
            receive_task,
            return_exceptions=True
        )

        print("Da thoat phong chat.")


asyncio.run(main())
