from src import Deck, Player, Blackjack_Round
from enum import Enum


class Status(Enum):
    NOT_PLAYING = 0
    WAITING = 1
    IN_PROGRESS = 2


class Blackjack:
    def __init__(self):
        self.players = []
        self.gameChannel = ''
        self.gameStatus = Status.NOT_PLAYING
        self.round = Blackjack_Round.Round()
        self.dealer = None

    def initializeGame(self, channel):
        self.players.clear()
        self.gameChannel = channel
        self.gameStatus = Status.WAITING
        self.round = Blackjack_Round.Round()

    def addPlayer(self, name):
        # if self.findPlayer(name):
        #     return 'You are already in the game ' + str(name)
        #else:
        newPlayer = Player.Player(name)
        self.players.append(newPlayer)
        return str(name) + ' has joined the game! Player Count: ' + str(self.numOfPlayers())

    def removePlayer(self, name):
        player = self.findPlayer(name)
        self.players.remove(player)
        if self.dealer == player:
            self.dealer = None
        return str(player.name) + " has been removed from the game. Player count: " + str(self.numOfPlayers())

    def getDealer(self):
        return self.dealer

    def setDealer(self, name):
        dealer = self.findPlayer(name)
        if dealer:
            self.dealer = dealer
            return str(self.dealer.name) + ' is now the banker.'
        else:
            return str(name) + ' is not in the game.'

    def getPlayerByIndex(self, index):
        if 0 <= index < self.numOfPlayers():
            return self.players[index]
        return None

    def findPlayer(self, name):
        for player in self.players:
            if player.name == name:
                return player
        return None

    def checkRoundStart(self):
        output = ''
        for player in self.players:
            if player.getBet() <= 0 and player is not self.dealer:
                output += str(player.name) + ' please make a bet before starting the game. \n'
        if len(output) > 1:
            return output

        if self.dealer:
            return 'Valid'
        return 'There is no banker for the game. Use \'!beBanker\' to become the banker.'

    def startRound(self):
        self.round.startRound(self.players, self.dealer)

    def setGameChannel(self, channel):
        self.gameChannel = channel

    def setGameStatus(self, status):
        self.gameStatus = status

    def numOfPlayers(self):
        return len(self.players)

    def endRound(self):
        output = 'Total Winnings after this round: \n'
        for player in self.players:
            output += str(player.name) + ': $' + str(player.getWinnings()) + '\n'
        output += 'This round has ended, use \'!start\' to start the next round'
        return output



