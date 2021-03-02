from src import Deck, Player, Round, Team
from enum import Enum
from src.Card import Suit, Rank, Card


class Status(Enum):
    NOT_PLAYING = 0
    WAITING = 1
    BIDDING = 2
    PARTNERING = 3
    IN_PROGRESS = 4


class Bridge:

    def __init__(self):
        self.players = []
        self.deck = Deck.Deck()
        self.gameChannel = ''
        self.gameStatus = Status.NOT_PLAYING
        self.turn = 0
        self.currentBid = (0, 0, None)
        self.trumpSuit = None
        self.passCount = 0
        self.round = Round.Round()
        self.team1 = Team.Team()
        self.team2 = Team.Team()
        self.partnerCard = None

    def initializeGame(self, channel):
        self.players.clear()
        self.deck.initializeDeck()
        self.team1 = Team.Team()
        self.team2 = Team.Team()
        self.gameChannel = channel
        self.gameStatus = Status.WAITING
        self.turn = 0
        self.currentBid = (0, 0, None)
        self.trumpSuit = None
        self.round = Round.Round()
        self.partnerCard = None

    def wash(self):
        self.deck.initializeDeck()
        for player in self.players:
            player.hand.clear()
        self.turn = 0
        self.currentBid = (0, 0, None)
        self.trumpSuit = None
        self.round = Round.Round()
        self.partnerCard = None

    def getCards(self, player):
        cardList = self.deck.drawNCards(13)
        player.addListToHand(cardList)
        player.sortHand()

    def startGame(self):
        self.setGameStatus(Status.BIDDING)
        for player in self.players:
            self.getCards(player)

    def endGame(self):
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

    def setGameStatus(self, status):
        self.gameStatus = status

    def findPlayer(self, name):
        for player in self.players:
            if player.name == name:
                return player
        return None

    def startTurn(self):
        player = self.currentBid[2]
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
        self.round.startRound(self.trumpSuit)

    def getTrumpSuit(self):
        return self.trumpSuit

    def checkValidBid(self, num, suit):
        if not self.currentBid:
            return True
        if 0 < num < self.currentBid[0] or num > 7:
            return False
        elif num == self.currentBid[0]:
            if suit.value <= self.currentBid[1].value:
                return False
        return True

    def getCurrentBidder(self):
        return self.currentBid[2]

    def setBid(self, num, suit, player):
        print(str(num) + " " + suit.name + " " + str(player.name))
        self.currentBid = (num, suit, player)

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
        output = "Bid has been finalised. The bid is " + str(self.currentBid[0]) + " " + self.currentBid[1].name + " by " + str(self.currentBid[2].name)
        output += '\n' + str(self.currentBid[2].name) + " please choose your partner, e.g.: \'!partner ACE HEARTS\'"
        return output

    def addToSet(self, card, player):
        self.round.addToSet(card, player)

    def hasRoundEnded(self):
        return self.round.hasRoundEnded()

    def announceSetWinner(self):
        player = self.round.getWinningPlayer()
        player.score += 1
        self.turn = self.players.index(player)
        self.team1.updateSetsWon()
        self.team2.updateSetsWon()
        output = self.round.displaySet()
        output += self.round.announceSetWinner()
        for player in self.players:
            output += player.displayNumSetsWon() + '\n'
        return output

    def startNewRound(self):
        round_set = self.round.retrieveSet()
        winning_player = self.round.getWinningPlayer()
        winning_player.setsOfCardsWon.append(round_set)
        self.round.startRound(self.trumpSuit)

    def setPartner(self, card):
        winning_bidder = self.getCurrentBidder()
        self.partnerCard = card
        #Team 1 always belongs to the winning bidder
        self.team1.addPartner(winning_bidder)
        for player in self.players:
            if player.isCardInHand(card):
                self.team1.addPartner(winning_bidder)
            elif player is not winning_bidder:
                self.team2.addPartner(player)

        #Set number of sets for each team to win
        self.team1.setNumSetsToWin(self.currentBid[0] + 6)
        self.team2.setNumSetsToWin(13 - self.team1.getNumSetsToWin() + 1)

    def parsePartnerArg(self, args):
        if args[0].lower() == "two" or args[0].lower() == '2':
            cardRank = Rank.TWO
        elif args[0].lower() == "three" or args[0].lower() == '3':
            cardRank = Rank.THREE
        elif args[0].lower() == "four" or args[0].lower() == '4':
            cardRank = Rank.FOUR
        elif args[0].lower() == "five" or args[0].lower() == '5':
            cardRank = Rank.FIVE
        elif args[0].lower() == "six" or args[0].lower() == '6':
            cardRank = Rank.SIX
        elif args[0].lower() == "seven" or args[0].lower() == '7':
            cardRank = Rank.SEVEN
        elif args[0].lower() == "eight" or args[0].lower() == '8':
            cardRank = Rank.EIGHT
        elif args[0].lower() == "nine" or args[0].lower() == '9':
            cardRank = Rank.NINE
        elif args[0].lower() == "ten" or args[0].lower() == '10':
            cardRank = Rank.KEYCAP_TEN
        elif args[0].lower() == "jack" or args[0].lower() == 'j':
            cardRank = Rank.REGIONAL_INDICATOR_J
        elif args[0].lower() == "queen" or args[0].lower() == 'q':
            cardRank = Rank.REGIONAL_INDICATOR_Q
        elif args[0].lower() == "king" or args[0].lower() == 'k':
            cardRank = Rank.REGIONAL_INDICATOR_K
        elif args[0].lower() == "ace" or args[0].lower() == 'a':
            cardRank = Rank.A
        else:
            raise ValueError

        if args[1].lower() == 'clubs' or args[1].lower() == 'club':
            cardSuit = Suit.CLUBS
        elif args[1].lower() == 'diamonds' or args[1].lower() == 'diamond':
            cardSuit = Suit.DIAMONDS
        elif args[1].lower() == 'hearts' or args[1].lower() == 'heart':
            cardSuit = Suit.HEARTS
        elif args[1].lower() == 'spades' or args[1].lower() == 'spade':
            cardSuit = Suit.SPADES
        else:
            raise ValueError
        return Card(cardSuit, cardRank)

    def announcePartner(self, card):
        self.setPartner(card)
        return str(self.getCurrentBidder().name) + ' has declared his/her partner to be ' + card.showCard()

    def hasEnded(self):
        return self.team1.hasWon() or self.team2.hasWon()

    def concludeWinner(self):
        teammates = ""
        if self.team1.hasWon():
            winning_team = self.team1
        elif self.team2.hasWon():
            winning_team = self.team2

        for player in winning_team.getPartners():
            teammates += str(player.name) + ' '

        return "Congratulations! " + teammates + ' has won the game with ' + str(winning_team.setsWon) + ' sets won!'

    def validPlay(self, card, player):
        return self.round.validPlay(card, player)