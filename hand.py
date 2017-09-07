from random import randint
from engine import Card, Hand, shuffleddeck
from tqdm import tqdm


numplayers = 6
handsize = 5
communitycards = 5
# cards to deal
deal = 2
usr = []
opp = []
besthand = None

def calculateodds(user, opponent, common=None):
    # This evaluation is specific to games where the remainder of the cards are community cards
    # number of unknown cards (denominator) calculated from number of cards user has + common cards out of 52
    # it is assumed that user and opponent have the same number of cards and user has less cards than handsize
    wins = 0
    total = 0
    global besthand
    # Handle different types of common input
    if common is None:
        common = Hand()
    if not type(common) is Hand:
        h = []
        for z in common:
            h.append(Card(z))
        common = Hand(h)

    deck = createremainderdeck(user + common)

    if len(common) < communitycards:
        for communities in deck:
            w, t = calculateodds(user, opponent, common=(common + communities))
            wins += w
            total += t

    else:
        # debugging information:
        # print("User ", user)
        # print("common ", common)
        # print("Opponent ", opponent)
        # print(user + common)
        # print(common.cards)
        # print(opponent.cards)
        # print((user + common).pokerhand(), (opponent + common).pokerhand())

        if user + common > opponent + common:
            if besthand is None:
                besthand = (user + common)
            else:
                if (user + common) > besthand:
                    besthand = (user + common)
        else:
            if besthand is None:
                besthand = (opponent + common)
            else:
                if (user + common) > besthand:
                    besthand = (opponent + common)
        wins += 1 * ((user + common) > (opponent + common))
        total += 1
    return wins, total


def createremainderdeck(cards):
    d = set(range(0,52))
    for j in cards.cards:
        if int(j) in d:
            d.remove(int(j))
    return d


shuffled = shuffleddeck()

for x in range(0,deal):
    usr.append(Card(shuffled.pop()))
    opp.append(Card(shuffled.pop()))

u = Hand(usr)
c = Hand(opp)
# print(u + c)
# print(u, c)
# print(u > c)
# print(createremainderdeck(u))f
print("User {}".format(usr))
print("Opponent {}".format(opp))
coms = []
# coms specifies the common cards already known.  The max community cards is given by the constant communitycards
for a in range(0, 4):
    coms.append(shuffled.pop())
j = Hand([Card(d) for d in coms])
print("Community {}".format(j))
wins, total = calculateodds(u, c, coms)
print("Wins: {} out of {} ({})".format(wins, total, wins/total))
print(besthand.pokerhand())
