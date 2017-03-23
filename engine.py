from random import randint
from random import seed
# constants

handsize = 5

poker_hands = {1: 'Straight Flush', 2: 'Four of a Kind', 3: 'Full House', 4: 'Flush', 5: 'Straight',
               6: 'Three of a Kind', 7: 'Two Pair', 8: 'One Pair', 9: 'High Card'}

suits = {0: 'Hearts', 1: 'Clubs', 2: 'Diamonds', 3: 'Spades'}
ranks = {0: 'Two', 1: 'Three', 2: 'Four', 3: 'Five', 4: 'Six', 5: 'Seven', 6: 'Eight',
         7: 'Nine', 8: 'Ten', 9: 'Jack', 10: 'Queen', 11: 'King', 12: 'Ace', -1: 'Ace'}


class Card(object):
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return ranks[self.rank()] + ' of ' + suits[self.suit()]

    def __int__(self):
        return self.number

    def rank(self):
        return self.number % 13

    def suit(self):
        return self.number // 13

    def __gt__(self, other):
        if self.rank() > other.rank(): return True

# This assumes that there are all unique cards


class Hand(object):
    def __init__(self, c):
        self.cards = c

    def __repr__(self):
        return str(self.cards)

    def __iter__(self):
        yield [int(z) for z in self.cards]

    def __gt__(self, other):
        sscore, scards = self.pokerhand()
        oscore, ocards = other.pokerhand()
        firstkickers = [1, 5]
        fourthkickers = [3, 6]
        fifthkickers = [2,7]
        if sscore > oscore:
            return True
        elif sscore in firstkickers:
            if scards[0] > ocards[0]:
                return True
        elif sscore == 2:
            if scards[0] > ocards[0]:
                return True
                if scards [4] > ocards[4]:
                    return True
        elif sscore in fourthkickers:
            if scards[0] > ocards[0]:
                return True
            elif scards [0] == ocards[0] and scards[3] > ocards[3]:
                return True
            elif scards[0] == ocards[0] and scards[3] == ocards[3] and scards[4] > ocards[4]:
                return True
        elif sscore == 6:
            pass
    def comparecards(self,scards, ocards):
        for k in range(0,len(self)):
            if scards[k] > ocards[k]:
                return True


    # These functions all return a value and the corresponding cards that make up the hand
    # with a minimum of <handsize> cards
    def checkxkind(self, num, cards=None):
        if cards is None:
            cards = self.cards
        mods = []
        returned_hand = []
        max_find = -1
        [mods.append(c.rank()) for c in self.cards]
        for c in mods:
            if mods.count(c) == num and c > max_find:
                max_find = c
        if max_find == -1:
            return False
        else:
            for z in self.cards:
                if z.rank() == max_find:
                    returned_hand.append(self.cards[self.cards.index(z)])
            handcopy = self.cards.copy()
            for z in returned_hand:
                handcopy.remove(z)
            # builds a full hand with handsize or number of cards given
            while len(returned_hand) < min(handsize,len(cards)):
                c = self.gethighcard(handcopy)
                handcopy.remove(c)
                returned_hand.append(c)
            return returned_hand

    def checkflush(self):
        # returns all cards with the big_flush suit
        divs = []
        return_hand = []
        big_flush = -1
        [divs.append(c.suit()) for c in self.cards]
        # this logic limits the search to finding only 1 flush per set of cards
        # which in turn means that results are unreliable for >= 10 cards
        for a in range(0, 4):
            if divs.count(a) >= handsize:
                big_flush = a
        if big_flush == -1:
            return False
        else:
            for z in self.cards:
                if z.suit() == big_flush:
                    return_hand.append(z)
            return return_hand

    def checkstraight(self, cards=None):
        # returns the longest straight > handsize
        if cards is None:
            cards = self.cards
        rn = set([c.rank() for c in cards])
        if 12 in rn:
            rn.add(-1)
        straights = set()
        return_hand = []
        for r in rn:
            testset = set(range(r, r+handsize))
            if testset.issubset(rn):
                # found a straight
                xtra = r + handsize - 1
                # counter used to find straights longer than handsize
                while xtra != -2:
                    xtra += 1
                    if xtra in rn:
                        # found longer straight
                        testset.add(xtra)
                    else:
                        straights = testset.union(straights)
                        xtra = -2
        if -1 in straights:
            straights.remove(-1)
            straights.add(12)
        for c in cards:
            if c.rank() in straights:
                return_hand.append(c)
        if return_hand is not []:
            return return_hand
        else:
            return False

    def gethighcard(self, cards=None):
        if cards is None:
            cards = self.cards
        mods = []
        [mods.append(c.rank()) for c in cards]
        return cards[mods.index(max(mods))]

    def getbestcards(self, cards=None, numcards=None, straight=False):
        if cards is None:
            cards = self.cards
        if numcards is None:
            numcards = len(cards)
        else:
            numcards = min(len(cards),numcards)
        return_hand = []
        for a in range(0,numcards):
            return_hand.append(self.gethighcard(cards))
            cards.remove(return_hand[-1])
        return return_hand

    def getbeststraight(self, cards=None):
        return_hand = []
        if cards is None:
            cards = self.cards
        rn = set([c.rank() for c in cards])
        rn = list(rn)
        if 12 in rn:
            rn.append(-1)
        rn.sort(reverse=True)
        start = -2
        for r in rn:
            for c in range(handsize-1,1,-1):
                if r - c not in rn:
                    break
                start = r
        toadd = list(range(start,start-handsize,-1))
        if -1 in toadd:
            toadd.remove(-1)
            toadd.append(12)
        for z in cards:
            if z.rank() in toadd:
                return_hand.append(cards[cards.index(z)])
                toadd.remove(z.rank())
        return_hand.sort(reverse=True)
        return return_hand

    def pokerhand(self, cards=None):
        return_hand = []
        if cards is None:
            cards = self.cards
        strt = self.checkstraight()
        flsh = self.checkflush()
        if flsh:
            strtflsh = self.checkstraight(flsh)
            if strtflsh:
                return 1, self.getbeststraight(strtflsh)
        fofk = self.checkxkind(4)
        if fofk:
            return 2, fofk
        thrk = self.checkxkind(3)
        twok = self.checkxkind(2)
        if thrk and twok:
            return_hand.append(thrk[0:3] + twok[0:2])
            return 3, return_hand
        if flsh:
            return_hand = self.getbestcards(flsh, numcards=5)
            return 4, return_hand
        if strt:
            return_hand = self.getbeststraight(strt)
            return 5, return_hand
        if thrk:
            return_hand.append(thrk[0:3]+self.getbestcards(thrk[3:], numcards=2))
            return 6, return_hand
        if twok:
            dummy = Hand(list(set(cards).difference(set(twok[0:2]))))
            twop = dummy.checkxkind(2)
            if twop:
                return_hand.append(twok[0:2]+twop[0:2]+self.getbestcards(twop[2:], numcards=1))
                return 7, return_hand
            else:
                return_hand.append(twok[0:2] + self.getbestcards(twok[2:], numcards=3))
                return 8, return_hand
        return 9, self.getbestcards(numcards=5)



# TESTING
# hand = Hand([Card(0),Card(38),Card(21),Card(50),Card(39)])
rhand = []

clist = [7, 7, 39, 40, 38, 48, 29, 28, 38]
    # [18, 45, 17, 32, 16, 35, 41, 47, 46]
    # [16, 18, 25, 5, 8, 48, 10, 7, 6]
    # [26, 3, 18, 4, 12, 27, 14, 0, 41]
for b in range(0,1000):
    rhand = []
    # size = randint(2, handsize+5)
    size = 9
    for a in range(0,size):
        rhand.append(Card(randint(0,51)))
    hand3 = Hand(rhand)
    print(hand3,list(hand3))
    h, cards = (hand3.pokerhand())
    print(h,cards)
    if h == 5:
        print('Found Straight')
    if h == 1:
        print('STRAIGHT FLUSH')
    # print(hand3.getbeststraight())
    print('\n')


# hand1 = Hand([Card(c) for c in clist])
# print(hand1)
# print(hand1.pokerhand())
# print(hand1.getbeststraight())

