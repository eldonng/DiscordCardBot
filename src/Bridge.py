from src import Deck, Player
from enum import Enum
from src.Card import Suit


class Status(Enum):
    NOT_PLAYING = 0
    WAITING = 1
    BIDDING = 2
    IN_PROGRESS = 3


class Bridge:

    def __init__(self):
        self.players = []
        self.deck = Deck.Deck()
        self.gameChannel = ''
        self.gameStatus = Status.NOT_PLAYING
        self.turn = 0
        self.currentBid = (0, 0)
        self.trumpSuit = None
        self.passCount = 0

    def getCards(self, player):
        cardList = self.deck.drawNCards(13)
        player.addToHand(cardList)
        player.sortHand()

    def startGame(self):
        self.setGameStatus(Status.BIDDING)
        for player in self.players:
            self.getCards(player)

    def endGame(self):
        self.players.clear()
        self.deck.initializeDeck()
        self.setGameStatus(Status.NOT_PLAYING)

    def addPlayer(self, name):
        if self.numOfPlayers() >= 4:
            return 'There are already 4 players in game!'
#        elif self.findPlayer(name):
#            return 'You are already in the game ' + str(name)
        else:
            newPlayer = Player.Player(name)
            self.players.append(newPlayer)
            return str(name) + ' has joined the game! Player Count: ' + str(self.numOfPlayers())

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

    def startTurn(self):
        player = self.findPlayer(self.currentBid[2])
        self.setGameStatus(Status.IN_PROGRESS)
        if self.trumpSuit == Suit.NO_TRUMP:
            self.turn = self.players.index(player)
        else:
            self.turn = (self.players.index(player) + 1) % len(self.players)

    def nextPlayersTurn(self):
        self.turn = (self.turn + 1) % len(self.players)

    def getPlayersTurn(self):
        return self.turn

    def setTrumpSuit(self):
        self.trumpSuit = self.currentBid[1]

    def getTrumpSuit(self):
        return self.trumpSuit

    def checkValidBid(self, num, suit):
        if not self.currentBid:
            return True
        if num < self.currentBid[0]:
            return False
        elif num == self.currentBid[0]:
            print(str(suit.value) + " " + suit.name)
            print(str(self.currentBid[1].value) + " " + self.currentBid[1].name)
            if suit.value <= self.currentBid[1].value:
                return False
        return True

    def setBid(self, num, suit, name):
        self.currentBid = (num, suit, name)

    def parseBidArg(self, args):
        bidValue = int(args[0])
        if args[1].lower() == 'clubs' or args[1].lower() == 'club':
            bidSuit = Suit.CLUBS
        elif args[1].lower() == 'diamonds' or args[1].lower() == 'diamond':
            bidSuit = Suit.DIAMONDS
        elif args[1].lower() == 'hearts' or args[1].lower() == 'heart':
            bidSuit = Suit.HEARTS
        elif args[1].lower() == 'spades' or args[1].lower() == 'spade':
            bidSuit = Suit.SPADES
        elif args[1].lower() == 'notrump':
            bidSuit = Suit.NO_TRUMP
        return bidValue, bidSuit

    def addPassCount(self):
        self.passCount += 1

    def resetPassCount(self):
        self.passCount = 0

    def getPassCount(self):
        return self.passCount

    def announceBid(self):
        return "Bid has been finalised. The bid is " + str(self.currentBid[0]) + " " + self.currentBid[1].name + " by " + str(self.currentBid[2])
