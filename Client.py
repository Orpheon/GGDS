import config as c

class Client():
    def __init__(self):
        self.name = ''
        self.s = None
        self.ip = ''
        self.team = None
        self.clas = None
        if len(c.password) > 0:
            self.authorized = False
        else:
            self.authorized = True
        self.passCnt = 0;
