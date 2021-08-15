from asyncio import get_event_loop, sleep
from sfp import sfp

HOST, PORT = '127.0.0.1', 9999


async def main():
    reader, writer = await sfp.connect_tcp(HOST, PORT)
    print("Connected to", HOST, PORT)
    try:
        while True:
            writer.write("PING".encode())
            await writer.drain()
            print("PING sent")
            msg = ""
            while msg != "PONG":
                data = await reader.read()
                msg = data.decode()
            print("PONG received")
            await sleep(1)
    except:
        print("Connection closed")


if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(main())
