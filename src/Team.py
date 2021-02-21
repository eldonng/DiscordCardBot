class Team:

    def __init__(self):
        self.partners = set()
        self.setsWon = 0
        self.setsToWin = 0

    def addPartner(self, player):
        self.partners.add(player)

    def getPartners(self):
        return self.partners

    def updateSetsWon(self):
        score = 0
        for players in self.partners:
            score += players.getScore()
        self.setsWon = score

    def getNumSetsToWin(self):
        return self.setsToWin

    def setNumSetsToWin(self, num):
        self.setsToWin = num

    def hasWon(self):
        return self.setsWon >= self.setsToWin
