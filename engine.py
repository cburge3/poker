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
        if self.rank() > other.rank():
            return True

# This assumes that there are all unique cards


class Hand(object):
    def __init__(self, c):
        self.cards = c

    def __repr__(self):
        return str(self.cards)

    def __iter__(self):
        yield [int(z) for z in self.cards]

    def __gt__(self, other):
        if self.comparehands(other) == 1:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.comparehands(other) == 0:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.comparehands(other) == -1:
            return True
        else:
            return False

    def comparehands(self, other):
        sscore, scards = self.pokerhand()
        oscore, ocards = other.pokerhand()
        # format:  types of hands to compare - ordered cards to compare in those hands in case of a tie
        firstkickers = [1, 5]  # any kind of straight - 1
        fourthkickers = [3, 6]  # 3 of a kind or full house - 1,4,5
        fifthkickers = [2, 7]  # four of a kind or two pair - 1,3,5
        allcards = [4, 8, 9]  # flush, pair, high card - 1, 2, 3, 4, 5
        # there are some extra comparisons done in here to save overall space
        # win = 1, tie = 0, loss = -1 from self's perspective
        if sscore < oscore:
            return 1
        elif sscore > oscore:
            return -1
        elif sscore in firstkickers:
            # we can check the second card since the first card may be a wheel ace
            # and the cards will still be ordered Hi->Lo
            return self.comparecards(scards, ocards, [1])
        elif sscore in fifthkickers:
            return self.comparecards(scards, ocards, [0, 2, 4])
        elif sscore in fourthkickers:
            return self.comparecards(scards, ocards, [0, 3, 4])
        elif sscore in allcards:
            return self.comparecards(scards, ocards, [0, 1, 2, 3, 4])
        else:
            return 0

    def comparecards(self, sc, oc, cardstocheck):
        for k in cardstocheck:
            if sc[k] > oc[k]:
                return 1
            elif sc[k] < oc[k]:
                return -1
        return 0

    # These functions all return a value and the corresponding cards that make up the hand
    # with a minimum of <handsize> cards unless otherwise specified
    def checkxkind(self, num, cards=None):
        if cards is None:
            cards = self.cards.copy()
        mods = []
        returned_hand = []
        max_find = -1
        [mods.append(c.rank()) for c in cards]
        for c in mods:
            if mods.count(c) == num and c > max_find:
                max_find = c
        if max_find == -1:
            return False
        else:
            for z in cards:
                if z.rank() == max_find:
                    returned_hand.append(cards[cards.index(z)])
            handcopy = cards.copy()
            for z in returned_hand:
                handcopy.remove(z)
            # builds a full hand with handsize or number of cards given
            while len(returned_hand) < min(handsize,len(cards)):
                c = self.gethighcard(handcopy)
                handcopy.remove(c)
                returned_hand.append(c)
            return returned_hand

    def checkflush(self, cards=None):
        if cards is None:
            cards = self.cards.copy()
        # returns all cards with the big_flush suit
        divs = []
        return_hand = []
        big_flush = -1
        [divs.append(c.suit()) for c in cards]
        # this logic limits the search to finding only 1 flush per set of cards
        # which means that all results are unreliable for >= 10 cards
        for a in range(0, 4):
            if divs.count(a) >= handsize:
                big_flush = a
        if big_flush == -1:
            return False
        else:
            for z in cards:
                if z.suit() == big_flush:
                    return_hand.append(z)
            return return_hand

    def checkstraight(self, cards=None):
        # returns the longest straight > handsize
        if cards is None:
            cards = self.cards.copy()
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
            cards = self.cards.copy()
        mods = []
        [mods.append(c.rank()) for c in cards]
        return cards[mods.index(max(mods))]

    def getbestcards(self, cards=None, numcards=None):
        if cards is None:
            cards = self.cards.copy()
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
            cards = self.cards.copy()
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
        toadd = list(range(start, start-handsize, -1))
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
        if cards is None:
            cards = self.cards.copy()
        strt = self.checkstraight()
        flsh = self.checkflush()
        if flsh:
            strtflsh = self.checkstraight(flsh)
            if strtflsh:
                return_hand = self.getbeststraight(strtflsh)
                return 1, return_hand
        fofk = self.checkxkind(4)
        if fofk:
            return_hand = fofk
            return 2, return_hand
        thrk = self.checkxkind(3)
        twok = self.checkxkind(2)
        if thrk and twok:
            return_hand = thrk[0:3] + twok[0:2]
            return 3, return_hand
        if flsh:
            return_hand = self.getbestcards(flsh, numcards=handsize)
            return 4, return_hand
        if strt:
            return_hand = self.getbeststraight(strt)
            return 5, return_hand
        if thrk:
            return_hand = thrk[0:3]+self.getbestcards(thrk[3:], numcards=2)
            return 6, return_hand
        if twok:
            dummy = Hand(list(set(cards).difference(set(twok[0:2]))))
            twop = dummy.checkxkind(2)
            if twop:
                return_hand = twok[0:2]+twop[0:2]+self.getbestcards(twop[2:], numcards=1)
                return 7, return_hand
            else:
                return_hand = twok[0:2] + self.getbestcards(twok[2:], numcards=3)
                return 8, return_hand
        return_hand = self.getbestcards(numcards=5)
        return 9, return_hand

if __name__ == '__main__':
    pass



