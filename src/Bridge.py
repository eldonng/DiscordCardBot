from src import Deck, Player


class Bridge:

    def __init__(self):
        self.players = []
        self.deck = Deck.Deck()
        self.gameChannel = ''
        self.gameStarted = False

    def getCards(self, player):
        cardList = self.deck.drawNCards(13)
        player.addToHand(cardList)
        player.sortHand()

    def endGame(self):
        self.players.clear()
        self.deck.initializeDeck()
        self.setGameStarted(False)

    def addPlayer(self, name):
        if self.numOfPlayers() > 4:
            return 'There are already 4 players in game!'
#        elif player in self.players:
#            return 'You are already in the game ' + str(player)
        else:
            newPlayer = Player.Player(name)
            self.players.append(newPlayer)
            return str(name) + 'has joined the game!'

    def startGame(self):
        for player in self.players:
            self.getCards(player)

    def numOfPlayers(self):
        return len(self.players)

    def setGameChannel(self, channel):
        self.gameChannel = channel

    def setGameStarted(self, var):
        self.gameStarted = var
