from enum import Enum


class Suit(Enum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4


class Rank(Enum):
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    KEYCAP_TEN = 9
    REGIONAL_INDICATOR_J = 10
    REGIONAL_INDICATOR_Q = 11
    REGIONAL_INDICATOR_K = 12
    A = 13


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def getCardSuit(self):
        return self.suit

    def setCardSuit(self, suit):
        self.suit = suit

    def getCardRank(self):
        return self.rank

    def setCardRank(self, rank):
        self.rank = rank

    def showCard(self):
        return str(" :" + self.suit.name.lower()) + ": : " + str(self.rank.name.lower()) + ":"

    def __gt__(self, otherCard):
        return ((self.suit.value - 1) * 13 + self.rank.value) > ((otherCard.suit.value - 1) * 13 + otherCard.rank.value)
