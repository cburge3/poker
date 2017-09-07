from engine import Card, Hand, shuffleddeck
from random import randint


class PokerGame:
    def __init__(self, allplayers):
        # expects a list of class players
        self.players = allplayers
        self.numplayers = len(allplayers)
        self.ante = 0
        self.smallBlind = 20
        self.pot = 0
        self.dealer = 2
        self.deck = []
        self.toCall = 0
        self.hands = 0
#     this gametype is assumed to be no-limit Texas hold-em

    def inithand(self):
        self.numplayers = len(self.players)
        if self.numplayers == 1:
            print(self.players[0].name)
        self.pot = 0
        self.deck = shuffleddeck()
        # take bet from dealer
        if self.numplayers > 2:
            for z in self.players:
                z.bet(self.ante)
                
            sbpos = (self.dealer + 1) % self.numplayers
            bbpos = (self.dealer + 2) % self.numplayers
            self.players[sbpos].bet(self.smallBlind - self.ante)
            self.players[bbpos].bet(self.smallBlind * 2 - self.ante)
        else:
            # heads up
            self.players[self.dealer].bet(self.smallBlind)
            self.players[self.dealer + 1].bet(self.smallBlind)

        for y in range(0, 2):
            for z in self.players:
                z.takecard(self.deck.pop())
        self.toCall = self.smallBlind * 2

    def bettinground(self):
        for z in self.players:
            # 0 = check/fold otherwise this is the bet amount
            order = [((a + self.dealer + 3) % self.numplayers) for a in range(0, self.numplayers)]
            for z in order:
                tocall = self.toCall - self.players[z].inPot
                print("{} to call {}".format(self.players[z].name, tocall))
                response = self.players[z].response(tocall)
                if response < tocall:
                    self.players[z].playing = False
                else:
                    self.players[z].bet(response)

    def cleanuphand(self):
        self.dealer = (1 + self.dealer) % self.numplayers


class Player:

    def __init__(self, name, chips=500):
        self.name = name
        self.chips = chips
        self.__cards = []
        self.inPot = 0
        self.isPlaying = True
        self.isAllIn = False
        # for testing purposes only
        self.cards = []
        self.hand = None

    def takecard(self, card):
        self.__cards.append(Card(card))
        # for testing purposes only
        self.cards = self.__cards

    def bet(self, amount):
        if amount > self.chips:
            self.inPot = self.chips
            self.chips = 0
        else:
            self.inPot += amount
            self.chips -= amount

    def response(self, toCall):
        self.hand = Hand(self.__cards)
        print(self.hand.gethighcard())
        r = randint()
        return 0



if __name__ == '__main__':
    g = PokerGame([Player("TJ"), Player("Reed"), Player("Richard"), Player("Bush"), Player("Dylan"), Player("Steven")])
    g.inithand()
    for z in g.players:
        print(z.cards, z.name, z.chips)
    g.bettinground()


