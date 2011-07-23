import socket
from constants import *
from threading import Timer
import config as c
import mapRotation
from Client import Client
from MessageBuilders import *

class GameServer():
    def __init__(self):
        self.clients = []
        self.clients_kick = []
        self.tempClients = []
        self.tempClients_kick = []
        self.speed = 1 / 30
        self.setupTimer = 1800
        self.curMapID = 0
        self.curMapArea = 1
        self.balance = 0
        self.balancecnt = 0
        self.impMapChange = -1
        self.mapChanging = False
        self.syncTimer = False
        self.map = mapRotation.getMap(self.curMapID)
        self.mapURL = ""
        self.mapMD5 = ""
        self.define_commands()
    def serve_forever(self, port=8190, host="0.0.0.0"):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))
        self.s.listen(1)
        self.s.setblocking(0)
        self.tick(0)
    def tick(self, frame):
        while True:
            if self.balance != 0:
                balancecnt += 1
            if c.useLobbyServer and frame % 900 == 0:
                sendLobbyReg()
            doClientKick(self)
            doTempClientKick(self)
            acceptJoiningPlayer(self)
            for temp in self.tempClients:
                serviceJoiningPlayer(self, temp)
            for cl in self.clients:
                if not cl.authorized:
                    cl.passCnt += 1
                    if cl.passCnt >= 30 * 30:
                        cl.s.send(chr(KICK))
                        cl.s.send(chr(KICK_PASSWORDCOUNT))
                        self.kick_client(cl)
                        continue
                processClientCommands(self, cl)
            if self.syncTimer or frame % 3600 == 0 or self.setupTimer == 180:
                serializeState(self, CAPS_UPDATE)
                self.syncTimer = 0
            if frame % 7 == 0:
                serializeState(self, QUICK_UPDATE)
            else:
                serializeState(self, INPUTSTATE)
        t = Timer(self.speed, self.tick, [frame + 1])
        t.start()
    def kick_client(self, client):
        for item in self.clients_kick:
            if client == item:
                return False
        self.clients_kick.append(client)
        return True
    def define_commands(self):
        self.cb = {PLAYER_LEAVE: 0, PLAYER_CHANGECLASS: 1, PLAYER_CHANGETEAM: 1,
                   CHAT_BUBBLE: 1, BUILD_SENTRY: 0, DESTROY_SENTRY: 0,
                   DROP_INTEL: 0, OMNOM: 0, SCOPE_IN: 0,
                   SCOPE_OUT: 0, PASSWORD_SEND: -1, PLAYER_CHANGENAME: -1,
                   INPUTSTATE: 3}

def processClientCommands(self, cl):
    pass

def sendLobbyReg():
    pass

def acceptJoiningPlayer(self):
    fn = False
    try:
        sock, ip = self.s.accept()
        fn = True
    except: pass
    if fn:
        self.tempClients.append([sock, ip, 0, 0])

def serviceJoiningPlayer(self, cl):
    if cl[2] == 0:
        fn = False
        try:
            ubt = ord(cl[0].recv(1))
            fn = True
        except: pass
        if not fn:
            return
        if fn:
            fn = False
            try:
                exb = ord(cl[0].recv(1))
                fn = True
            except: pass
        if fn:
            if ubt == PLAYER_JOIN:
                cl[2] = 1
                cl[3] = exb
            else:
                kickTempClient(self, cl)
                return
    if cl[2] == 1:
        """if len(self.clients) >= c.maxPlayers:
            cl[0].send(chr(SERVER_FULL))
            kickTempClient(self, cl)
            return"""
        fn = False
        try:
            nam = str(cl[0].recv(cl[3]))
            fn = True
        except: pass
        if fn:
            if len(self.clients) >= c.maxPlayers and cl[1][0] != "127.0.0.1":
                cl[0].send(chr(SERVER_FULL))
                cl.append(nam)
                kickTempClient(self, cl)
                return
            serverJoinUpdate(self, cl[0])
            p = Client()
            p.s = cl[0]
            p.ip = cl[1][0]
            p.rport = cl[1][1]
            p.name = nam
            p.name = p.name[0:MAX_PLAYERNAME_LENGTH-1]
            p.name = p.name.replace("#", " ")
            print p.name, "connected (IP: " + p.ip + ")."
            self.clients.append(p)
            serverPlayerJoin(self, p.name)
            del self.tempClients[self.tempClients.index(cl)]
            del cl

def serializeState(self, state):
    pass

def kickTempClient(self, client):
        for item in self.tempClients_kick:
            if client == item:
                return False
        self.tempClients_kick.append(client)
        return True

def doClientKick(self):
    kl = []
    i = 0
    for cl in self.clients_kick:
        kl.append(cl)
        i += 1
    for cl in kl:
        print cl.name, "has been kicked from the server."
        cl.s.close()
        self.clients_kick.remove(cl)
        self.clients.remove(cl)

def doTempClientKick(self):
    kl = []
    i = 0
    for cl in self.tempClients_kick:
        kl.append(cl)
        i += 1
    for cl in kl:
        print cl[4], "has been kicked from the server."
        cl[0].close()
        self.tempClients_kick.remove(cl)
        self.tempClients.remove(cl)
