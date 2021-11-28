import socket, sys
from datetime import date
from datetime import datetime
import pickle

sockete_cliente = socket.socket()
sockete_cliente.connect(("", 8000))
i = 0
lista_args = []
lista_fechas = []
while True:
    try:
        intp = input("»")
        args = intp.replace("»", "")
        if args == "exit":
            sockete_cliente.send(pickle.dumps(args))
            break
        now = datetime.now()
        if args.startswith("-l"):
            nombre_arc = args.split(" ")
            with open(f'{nombre_arc[1]}', mode='w') as text:
                for arg, fecha in zip(lista_args, lista_fechas):
                    log_y_fecha = str('»» Comando: '+ arg + ', Fecha: ' + str(fecha))
                    text.write(log_y_fecha)
                    text.write('\n')
            sys.exit()
        sockete_cliente.send(pickle.dumps(args))
        respuesta = sockete_cliente.recv(2024)
        log = pickle.loads(respuesta)
        lista_args.insert(i, args)
        lista_fechas.insert(i, now)
        i += 1
        print(log)
    except EOFError:
        break
print('Conexion cerrada con exito')
sockete_cliente.close()