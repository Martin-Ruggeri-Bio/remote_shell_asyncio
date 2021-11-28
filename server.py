import socket, subprocess, shlex
from threading import Thread    
import pickle
import asyncio



async def handle_connection(conexion, port):
    while True:
        try:
            comando = await conexion.read(1024)
            comand = pickle.loads(comando)
            if comand == 'exit':
                break
            args = shlex.split(comand)
            log = subprocess.Popen(args,stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf-8')
            stdout, stderr = log.communicate()
            if len(stderr) > 0:
                port.write(pickle.dumps(stdout))
            port.write(pickle.dumps(stdout))
        except FileNotFoundError as err:
            port.write(pickle.dumps(str(err)))
    print("Conexion cerrada")
    conexion.close()


async def main():
    server = await asyncio.start_server(handle_connection, 'localhost', 8000)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
