from random import randint
from engine import Card, Hand
decksize = 52
deck = list(range(0, decksize))
shuffled = []
numplayers = 6
handsize = 5
deal = 2
tester = []
opponent = []

def calculateodds(user, opponent, common=None):
    # number of unknown cards (denominator) calculated from number of cards user has + common cards out of 52
    # it is assumed that user and opponent have the same number of cards and user has less cards than handsize
    denominator = 52 - (len(user) + len(common))
    others = createremainderdeck(user)

def createremainderdeck(cards):
    deck = set(range(0,52))
    for j in cards:
        for k in j:
            print(k)
            if k in deck:
                deck.remove(k)
    return deck


while len(deck) > 0:
    z = randint(0,len(deck)-1)
    shuffled.append(deck[z])
    deck.pop(z)

for x in range(0,deal):
    tester.append(Card(shuffled.pop()))
    opponent.append(Card(shuffled.pop()))
u = Hand(tester)
c = Hand(opponent)
print(createremainderdeck(u))

