import asyncio
import cowsay

clients = {}

async def chat(reader, writer):
    me = None
    send = asyncio.create_task(reader.readline())
    receive = None
    while not reader.at_eof():
        tasks = [send]
        if me is not None:
            if receive is None:
                receive = asyncio.create_task(clients[me].get())
            tasks.append(receive)
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                line = q.result().decode().strip()
                if me is None:
                    cmd = line.split(maxsplit=1)
                    if len(cmd) == 2 and cmd[0] == "login":
                        cow = cmd[1]
                        if cow in cowsay.list_cows() and cow not in clients:
                            me = cow
                            clients[me] = asyncio.Queue()
                else:
                    for out in clients.values():
                        if out is not clients[me]:
                            await out.put(cowsay.cowsay(line, cow=me))
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    if receive is not None:
        receive.cancel()
    if me is not None:
        del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())