from engine import *
from time import perf_counter
from random import randint

# Single hand testing
clist = [6, 24, 25, 39, 4, 29, 46]
dlist = [42, 26, 23, 46, 35, 5, 17]

hand1 = Hand([Card(c) for c in clist])
hand2 = Hand([Card(d) for d in dlist])
print(hand1, hand2)
print(hand1.pokerhand())
print(hand2.pokerhand())
print(hand1>hand2)

hands = 1000
init_time = perf_counter()
def pokertest():
    for b in range(0, hands):
        rhand = []
        rhand2 = []
        # size = randint(2, handsize+5)
        size = 9
        for a in range(0, size):
            rhand.append(Card(randint(0, 51)))
            rhand2.append(Card(randint(0, 51)))
        hand3 = Hand(rhand)
        hand4 = Hand(rhand2)
        # print('hand3', hand3, '\n', 'hand4', hand4, '\n')
        # print(list(hand3),list(hand4))
        print('three',hand3,list(hand3),'\n',hand3.pokerhand(),'\n','four',hand4,list(hand4),'\n',hand4.pokerhand())
        if hand4 > hand3:
            print('four wins ' + poker_hands[hand4.pokerhand()[0]] + '\n')
        elif hand3 > hand4:
            print('three wins ' + poker_hands[hand3.pokerhand()[0]] + '\n')
        else:
            print('split')


pokertest()
final_time = perf_counter()
interval = final_time-init_time
rate = hands
print(final_time-init_time,final_time,init_time,hands/interval)