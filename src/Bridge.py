from src import Deck, Player
from enum import Enum


class Status(Enum):
    NOT_PLAYING = 0
    WAITING = 1
    IN_PROGRESS = 2


class Bridge:

    def __init__(self):
        self.players = []
        self.deck = Deck.Deck()
        self.gameChannel = ''
        self.gameStatus = Status.NOT_PLAYING
        self.turn = 0

    def getCards(self, player):
        cardList = self.deck.drawNCards(13)
        player.addToHand(cardList)
        player.sortHand()

    def endGame(self):
        self.players.clear()
        self.deck.initializeDeck()
        self.setGameStatus(Status.NOT_PLAYING)

    def addPlayer(self, name):
        if self.numOfPlayers() >= 4:
            return 'There are already 4 players in game!'
#        elif player in self.players:
#            return 'You are already in the game ' + str(player)
        else:
            newPlayer = Player.Player(name)
            self.players.append(newPlayer)
            return str(name) + 'has joined the game! Player Count: ' + str(self.numOfPlayers())

    def startGame(self):
        self.setGameStatus(Status.IN_PROGRESS)
        for player in self.players:
            self.getCards(player)

    def numOfPlayers(self):
        return len(self.players)

    def setGameChannel(self, channel):
        self.gameChannel = channel

    def setGameStatus(self, var):
        self.gameStatus = var

    def findPlayer(self, name):
        for player in self.players:
            if player.name == name:
                return player
        return None

    def nextPlayersTurn(self):
        self.turn = (self.turn + 1) % len(self.players)

    def getPlayersTurn(self):
        return self.turn
