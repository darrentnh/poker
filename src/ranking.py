from collections import Counter
from enum import IntEnum
from itertools import combinations

rank_above_9 = {'T': 10,
                'J': 11,
                'Q': 12,
                'K': 13,
                'A': 14}

number_to_rank = {10: 'Ten',
                  11: 'Jack',
                  12: 'Queen',
                  13: 'King',
                  14: 'Ace'}

suit_names = {'C': 'Clubs',
              'D': 'Diamonds',
              'H': 'Hearts',
              'S': 'Spades'}


class Quality(IntEnum):
    """Quality of a poker hand. Higher values beat lower values."""
    high_card = 1
    pair = 2
    two_pairs = 3
    trips = 4
    straight = 5
    flush = 6
    full_house = 7
    quads = 8
    straight_flush = 9


def sort_by_rank(hand):
    """
    Convert TJQKA to integers according to dictionary and sort ascending
    """
    new_hand = []
    for x in hand:
        if x[0] in rank_above_9:
            new_hand.append((rank_above_9[x[0]], x[1]))
        else:
            new_hand.append((int(x[0]), x[1]))
    return sorted(new_hand, key=lambda rank: rank[0])


def assess_combination(hand):
    """
    Assess a five card combination and returns the best hand in a tuple
    First element is the quality
    Second element is a list of distinct ranks
    """
    ranks = [x[0] for x in sort_by_rank(hand)]
    if ranks == [2, 3, 4, 5, 14]:  # special case: ace-low straight
        ranks = [1, 2, 3, 4, 5]

    flush = len(set(suit for _, suit in hand)) == 1
    straight = ranks == list(range(ranks[0], ranks[0] + 5))

    count = Counter(ranks)
    counts = list(reversed(sorted(count.values())))
    distinct_ranks = sorted(count, reverse=True, key=lambda v: (count[v], v))

    if flush and straight:       q = Quality.straight_flush
    elif counts == [4, 1]:       q = Quality.quads
    elif counts == [3, 2]:       q = Quality.full_house
    elif flush:                  q = Quality.flush
    elif straight:               q = Quality.straight
    elif counts == [3, 1, 1]:    q = Quality.trips
    elif counts == [2, 2, 1]:    q = Quality.two_pairs
    elif counts == [2, 1, 1, 1]: q = Quality.pair
    else:                        q = Quality.high_card

    return q, distinct_ranks


def best_hand(hand, community_cards):
    """
    For texas hold'em, takes seven cards (two hole cards and five community cards),
    permutate and find the best possible hand.

    Returns a tuple with the best hand quality and distinct ranks.
    """
    for x in community_cards:
        hand.append(x)
    possible_hands = []
    for combination in combinations(hand, 5):
        possible_hands.append(assess_combination(combination))
    best_hand = max(possible_hands)
    return best_hand


# with open('hands.txt', 'r') as f:
#     player_1_wins = 0
#     player_2_wins = 0
#     for line in f:
#         ls = []
#         for x in line.split():
#             ls.append((x[0], x[1]))
#         hand_1, hand_2 = ls[:5], ls[5:]
#         if assess_combination(hand_1) > assess_combination(hand_2):
#             player_1_wins += 1
#         else:
#             player_2_wins += 1
#     print(player_1_wins, player_2_wins)
#
#
# # Check if 5 of the same suit for flush
# def check_flush(hand):
#     suit = hand[0][1]
#     if all([1 if card[1] == suit else 0 for card in hand]):
#         ranks = [x[0] for x in sort_by_rank(hand)]
#         res = {'flush': ranks[-1]}
#         return res
#
#
# # Check if 5 ascending values for straight
# def check_straight(hand):
#     ranks = [x[0] for x in sort_by_rank(hand)]
#     for i in range(len(ranks) - 1):
#         if ranks[i+1] != ranks[i] + 1:
#             return None
#     res = {'straight': ranks[-1]}
#     return res
#
#
# # If fulfil both flush and straight, then straight flush
# def check_straight_flush(hand):
#     res_flush = check_flush(hand)
#     res_straight = check_straight(hand)
#     if res_flush and res_straight:
#         res = {}
#         res.update(res_flush)
#         res.update(res_straight)
#         return res
#
#
# # If straight flush and highest is an Ace, then royal flush
# def check_royal_flush(hand):
#     res_straight_flush = check_straight_flush(hand)
#     if res_straight_flush and res_straight_flush['flush'] == 14:
#         res = {}
#         res.update(res_straight_flush)
#         res['royalflush'] = True
#         return res
#
#
# # Check if 4 of the same value for quads
# def check_quads(hand):
#     rank = [x[0] for x in sort_by_rank(hand)]
#     if rank[0] == rank[1] == rank[2] == rank[3]:
#         res = {'fours': rank[0],
#                'ones': rank[4]}
#         return res
#     elif rank[1] == rank[2] == rank[3] == rank[4]:
#         res = {'fours': rank[1],
#                'ones': rank[0]}
#         return res
#
#
# # Check if 3 of the same value for trips
# def check_trips(hand):
#     rank = [x[0] for x in sort_by_rank(hand)]
#     if rank[0] == rank[1] == rank[2]:
#         res = {'threes': rank[0],
#                'ones': (rank[3], rank[4])
#                }
#         return res
#     elif rank[1] == rank[2] == rank[3]:
#         res = {'threes': rank[1],
#                'ones': (rank[0], rank[4])
#                }
#         return res
#     elif rank[2] == rank[3] == rank[4]:
#         res = {'threes': rank[2],
#                'ones': (rank[0], rank[1])
#                }
#         return res
#
#
# # If the other 2 are same value, then special case full house
# def check_full_house(hand):
#     res = check_trips(hand)
#     if res is not None:
#         c1, c2 = res['ones']
#     if c1 == c2:
#         res['twos'] = c1
#         del res['ones']
#     return res
#
#
# def check_pair(hand):
#     ranks = [x[0] for x in sort_by_rank(hand)]
#     if ranks[0] == ranks[1]:
#         return {'twos': ranks[0],
#                 'ones': (ranks[2], ranks[3], ranks[4])
#                 }
#     elif ranks[1] == ranks[2]:
#         return {'twos': ranks[1],
#                 'ones': (ranks[0], ranks[3], ranks[4])
#                 }
#     elif ranks[2] == ranks[3]:
#         return {'twos': ranks[2],
#                 'ones': (ranks[0], ranks[1], ranks[4])
#                 }
#     elif ranks[3] == ranks[4]:
#         return {'twos': ranks[3],
#                 'ones': (ranks[0], ranks[1], ranks[2])
#                 }
#
# # Check if 2 of the same value for pair
#
#     # If another 2 out of the remaining 3 have same value,
#     # then special case, two pairs
