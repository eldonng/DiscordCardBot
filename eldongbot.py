import discord
from discord.ext import commands
import os
from enum import Enum
import random

class Suit(Enum):
  CLUBS = 1
  DIAMONDS = 2
  HEARTS = 3
  SPADES = 4

class Rank(Enum):
  TWO = 1
  THREE = 2
  FOUR = 3
  FIVE = 4
  SIX = 5
  SEVEN = 6
  EIGHT = 7
  NINE = 8
  KEYCAP_TEN = 9
  REGIONAL_INDICATOR_J = 10
  REGIONAL_INDICATOR_Q = 11
  REGIONAL_INDICATOR_K = 12
  A = 13

class Card:

    def __init__(self, suit, rank):
      self.suit = suit
      self.rank = rank

    def getCardSuit(self):
      return self.suit

    def setCardSuit(self, suit):
      self.suit = suit

    def getCardRank(self):
      return self.rank

    def setCardRank(self, rank):
      self.rank = rank

    def showCard(self):
      return str(self.suit.value) + " " + str(self.rank.value)

    def __gt__(self, otherCard):
      return ((self.suit.value-1)*13 + self.rank.value) > ((otherCard.suit.value-1)*13 + otherCard.rank.value)


class Deck:

  def __init__(self):
    self.deck = []
    self.size = 0
    self.initializeDeck()

  def initializeDeck(self):
    for suit in Suit:
      for rank in Rank:
        self.deck.append(Card(suit,rank))
    self.size = 52

  def drawCard(self):
    index = random.randint(0, self.size-1)
    drawnCard = self.deck[index]
    self.removeCardFromDeck(index)
    return drawnCard

  def removeCardFromDeck(self, index):
    self.deck.pop(index)
    self.size -= 1

  def getDeckSize(self):
    return self.size


class Player:
  def __init__(self):
    self.hand = []

  def addToHand(self, card):
    self.hand.append(card)

  def getHand(self):
    return self.hand

  def sortHand(self):
    self.hand.sort()

  def displayHand(self):
    output = ""
    for card in self.hand:
      output += str(self.hand.index(card)+1) + '. :' + card.rank.name.lower() + ': ' + ' :' + card.suit.name.lower() + ':' + "\n"
    return output
      
def getCards(player):
  if deck.getDeckSize() > 13:
    for i in range(0,13):
      card = deck.drawCard()
      player.addToHand(card)
    player.sortHand()
  else:
    return False
  return True

deck = Deck()
client = discord.Client()
author = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('fak u eldon'):
        await message.channel.send('WAT')

    if message.content.startswith('!shuffle'):
      if message.author not in author:
        player = Player()
        if getCards(player):     
          author.append(message.author)
          await message.channel.send('Cards has been dealt to ' + str(message.author) + ' , please check DM')
          await message.author.send('Player\'s Cards')
          await message.author.send(player.displayHand())
        else:
          await message.channel.send('There are already 4 players in game')
      else:
        await message.channel.send('You have already drew your hand ' + str(message.author))

    if message.content.lower().startswith('!endgame'):
        await message.channel.send('Game Ended')
        gameStarted = True
        author.clear()
        deck.initializeDeck()

bot = commands.Bot(command_prefix='$')

@bot.command()
async def test(ctx, arg):
    await ctx.channel.send(arg)

client.run('ODA3OTgxNjk1NjMzODUwMzc4.YB_5lw.ZsZWqKaxpstJ-oZGT8mxtmEUuz0')

#def shuffle():