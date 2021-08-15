from asyncio import get_event_loop
from sfp import sfp

# Use tcp socket on non unix OS
URI = "tcp://localhost"

# Or use unix domain socket
if 'unix' in sfp.AVAILABLE_SCHEMES:
    URI = "unix://tmp/example.sock"


async def handle(reader: sfp.Reader, writer: sfp.Writer):
    print("Connection accepted")
    try:
        async with writer:
            while True:
                msg = ""
                while msg != "PING":
                    data = await reader.read()
                    msg = data.decode()
                print("PING received")
                writer.write("PONG".encode())
                await writer.drain()
                print("PONG sent")
    except:
        print("Connection closed")


async def main():
    server = sfp.get_server_from_uri(URI, handle)
    await server.run()

if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(main())
