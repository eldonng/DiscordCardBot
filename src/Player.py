from src import Card


class Player:
    def __init__(self, name):
        self.hand = []
        self.name = name

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
                card) + 1) + '. :' + card.rank.name.lower() + ': ' + ' :' + card.suit.name.lower() + ':' + "\n"
        return output

    def playACard(self, index):
        if not self.hand and len(self.hand) <= index:
            self.hand.pop(index-1)
