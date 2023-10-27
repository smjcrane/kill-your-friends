import random

class Player():
    def __init__(self, userid):
        self.userid = userid
        self.name = ""
        self.alive = True
        self.targetid = None
        self.reverse_targetid = None
        self.killword = ""
        self.kills = 0

    def __str__(self) -> str:
        return "<Player ID: %s, name: %s>" % (self.userid, self.name)
    

class Game():
    def __init__(self) -> None:
        self.players = {}
        with open("assassin words.txt", "r") as wordlist:
            self.all_words = list(map(lambda s: s.strip(), wordlist.readlines()))
        self.status = "INIT"

    def add_player(self, userid):
        if userid in self.players:
            return
        if not len(self.all_words):
            raise IndexError("Maximum number of players has already been reached")
        self.players[userid] = Player(userid)
        self.players[userid].killword = random.choice(self.all_words)
        self.all_words.remove(self.players[userid].killword)

    def begin(self):
        c = list(self.players.keys())
        first = random.choice(c)
        c.remove(first)
        a = first
        while(len(c)):
            b = random.choice(c)
            c.remove(b)
            self.players[a].targetid = b
            self.players[b].reverse_targetid = a
            a = b
        self.players[a].targetid = first
        self.players[first].reverse_targetid = a
        self.status = "PLAYING"

    def get_target(self, userid):
        if userid in self.players:
            return self.targets[userid]
        
    def get_killword(self, userid):
        if userid in self.players:
            return self.players[userid].killword
        
    def kill(self, userid):
        p = self.players[userid]
        if not p.alive:
            return
        p.alive = False
        self.players[p.targetid].reverse_targetid = p.reverse_targetid
        self.players[p.reverse_targetid].targetid = p.targetid
        self.players[p.reverse_targetid].kills += 1
        if len([1 for p in self.players.values() if p.alive]) == 1:
            self.status = "FINISHED"

    def reassign_word(self, userid):
        if not len(self.all_words):
            return
        p = self.players[userid]
        p.killword = random.choice(self.all_words)
        self.players[p.reverse_targetid].kills -= 1
        self.all_words.remove(p.killword)