from src import Card
from enum import Enum

class Result(Enum):
    WIN = 0
    DRAW = 1
    LOSE = 2

class Player:
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.score = 0
        self.setsOfCardsWon = []
        self.bet = 0
        self.winnings = 0
        self.outcome = None

    def addListToHand(self, cardList):
        for card in cardList:
            self.addToHand(card)

    def addToHand(self, card):
        self.hand.append(card)

    def getHand(self):
        return self.hand

    def sortHand(self):
        self.hand.sort()

    def displayHand(self):
        output = ""
        for card in self.hand:
            output += str(self.hand.index(
                card) + 1) + '. :' + card.rank.name.lower() + ': ' + ' :' + card.suit.name.lower() + ': ' + card.suit.name + "\n"
        return output

    def playACard(self, index):
        if self.hand and len(self.hand) >= index > 0:
            return self.hand.pop(index-1)

    def displayNumSetsWon(self):
        return 'Number of sets won by ' + str(self.name) + ': ' + str(self.score)

    def getScore(self):
        return self.score

    def incrementSetsWon(self):
        self.score += 1

    def setScore(self, score):
        self.score = score

    def displayScore(self):
        return ('Current Hand Score: ' + str(self.score))

    def getBet(self):
        return self.bet

    def setBet(self, betAmt):
        self.bet = betAmt

    def getWinnings(self):
        return self.winnings

    def setChangeInWinnings(self, change):
        self.winnings += change

    def getOutcome(self):
        return self.outcome

    def setOutcome(self, outcome):
        self.outcome = outcome

    def setPartner(self, player):
        self.partners.add(player)

    def getPartner(self):
        return self.partners

    def isCardInHand(self, card):
        for playerCard in self.hand:
            if playerCard == card:
                return True
        return False

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(repr(self))

