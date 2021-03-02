
class Round:

    def __init__(self):
        self.trump = None
        self.set = []
        self.winningPlayer = None
        self.winningCard = None

    def startRound(self, trumpsuit):
        self.trump = trumpsuit
        self.set.clear()
        self.winningPlayer = None
        self.winningCard = None

    def addToSet(self, card, player):
        self.set.append((card, player))
        self.decideWinningPlayer(card, player)

    def retrieveSet(self):
        return self.set

    def displaySet(self):
        output = ''
        for turn in self.set:
            output += turn[0].showCard() + ' played by ' + str(turn[1].name) + '\n'
        return output

    def getWinningPlayer(self):
        return self.winningPlayer

    def getWinningCard(self):
        return self.winningCard

    def announceSetWinner(self):
        return 'Set Winner:\n ' + self.winningCard.showCard() + ' played by ' + str(self.winningPlayer.name) + '\n'

    def decideWinningPlayer(self, card, player):
        if self.winningCard:
            if card.suit == self.winningCard.suit:
                if card.rank.value > self.winningCard.rank.value:
                    self.winningCard = card
                    self.winningPlayer = player
            elif card.suit == self.trump:
                self.winningCard = card
                self.winningPlayer = player
        else:
            self.winningCard = card
            self.winningPlayer = player

    def hasRoundEnded(self):
        return len(self.set) == 4

    def validPlay(self, card, player):
        if len(self.set) > 0:
            startingSuit = self.set[0][0].getCardSuit()
            if card.getCardSuit() is not startingSuit and player.hasSuit(startingSuit):
                return False
        return True
