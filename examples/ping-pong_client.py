from asyncio import get_event_loop, sleep
from sfp import sfp

# Use tcp socket on non unix OS
URI = "tcp://localhost"
# Or use unix domain socket
if 'unix' in sfp.AVAILABLE_SCHEMES:
    URI = "unix://tmp/example.sock"


async def main():
    reader, writer = await sfp.connect_to_uri(URI)
    print("Connected to", URI)
    try:
        async with writer:
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
