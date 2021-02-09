from src import Card


class Player:
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.setsWon = 0
        self.setsOfCardsWon = []

    def addToHand(self, cardList):
        for card in cardList:
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
        return 'Number of sets won by ' + str(self.name) + ': ' + str(self.setsWon)

    def incrementSetsWon(self):
        self.setsWon += 1

