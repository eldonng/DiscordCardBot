from src import Deck, Player

class Round:
    def __init__(self):
        self.players = []
        self.blackjack = []
        self.turn = 0
        self.deck = Deck.Deck()
        self.dealer = None

    def startRound(self, players, dealer):
        print('testing')
        self.players = players
        for player in self.players:
            player.hand.clear()
        self.deck.initializeDeck()
        self.dealer = dealer
        print('testing2')
        self.turn = self.players.index(self.dealer)
        self.setNextTurn()
        self.distributeCards()
        self.calculateScores()

    def distributeCards(self):
        for i in range(2 * len(self.players)):
            index = (self.turn + i) % len(self.players)
            card = self.deck.drawCard()
            self.players[index].addToHand(card)


    def hitCard(self):
        playerHand = self.players[self.turn].getHand()
        score = self.calculateScore(playerHand)
        if score < 22 and len(playerHand) < 5:
            card = self.deck.drawCard()
            self.players[self.turn].addToHand(card)
        else:
            self.setNextTurn()
        score = self.calculateScore(playerHand)
        self.players[self.turn].setScore(score)

    def setNextTurn(self):
        self.turn = (self.turn + 1) % len(self.players)

    def getTurn(self):
        return self.turn

    def calculateScore(self, hand):
        score = 0
        aceCount = 0

        for cards in hand:
            if cards.rank.value < 9: #cards TWO to NINE
                score += cards.rank.value + 1
            elif 9 <= cards.rank.value <= 12: # cards TEN, J, Q, K
                score += 10
            else: # ACES we count later
                score += 1
                aceCount += 1

        while aceCount > 0:
            if score < 12 and len(hand) == 2:
                score += 10
            elif score < 13 and len(hand) == 3:
                score += 9
            aceCount -= 1

        return score

    def calculateScores(self):
        for player in self.players:
            score = self.calculateScore(player.getHand())
            player.setScore(score)

    def announceRoundResults(self):
        output = ''
        output += 'BANKER ' + str(self.dealer.name) + ': Score: ' + str(self.dealer.score) + '\n'
        for player in self.players:
            if player is not self.dealer:
                output += str(player.name) + ': Score: ' + str(player.score)
                if self.dealer.score < 22 and player.score < 22:
                    if player.score > self.dealer.score:
                        output += " WIN\n"
                        player.setChangeInWinnings(player.getBet())
                        self.dealer.setChangeInWinnings(player.getBet() * -1)
                    elif player.score == self.dealer.score:
                        output += " DRAW\n"
                    else:
                        output += " LOSE\n"
                        player.setChangeInWinnings(player.getBet() * -1)
                        self.dealer.setChangeInWinnings(player.getBet())
                elif self.dealer.score < 22:
                        output += " LOSE\n"
                        player.setChangeInWinnings(player.getBet() * -1)
                        self.dealer.setChangeInWinnings(player.getBet())
                elif player.score < 22:
                    output += " WIN\n"
                    player.setChangeInWinnings(player.getBet())
                    self.dealer.setChangeInWinnings(player.getBet() * -1)
                else:
                    output += " DRAW\n"
        return output
