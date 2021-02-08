from src import Card
import random

class Deck:

    def __init__(self):
        self.deck = []
        self.size = 0
        self.initializeDeck()

    def initializeDeck(self):
        self.deck.clear()
        for suit in Card.Suit:
            for rank in Card.Rank:
                self.deck.append(Card.Card(suit,rank))
        self.size = 52

    def drawCard(self):
        index = random.randint(0, self.size-1)
        drawnCard = self.deck[index]
        self.removeCardFromDeck(index)
        return drawnCard

    def drawNCards(self, count):
        cardList = []
        for i in range(0, count):
            cardList.append(self.drawCard())
        return cardList

    def removeCardFromDeck(self, index):
        self.deck.pop(index)
        self.size -= 1

    def getDeckSize(self):
        return self.size