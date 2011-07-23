from GameServer import GameServer

def run(port=8191, host='0.0.0.0'):
    server = GameServer()
    server.serve_forever(port, host)

if __name__ == '__main__':
    run()

"""from threading import Timer
import socket

class Global():
    pass

global g
g = Global()

g.host = "0.0.0.0"
g.port = 8190
g.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
g.sock.bind((g.host, g.port))
g.sock.listen(1)
g.sock.setblocking(0)
g.speed = 1 / 30

def tick(frame):
    global g
    t = Timer(g.speed, tick, [frame + 1])
    t.start()
"""
