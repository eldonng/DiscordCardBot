import discord
from discord.ext import commands
from src import Bridge
from src.Bridge import Status
import random
import codecs

bot = commands.Bot(command_prefix='!')
game = Bridge.Bridge()
list = []
f = codecs.open('wat_list.txt', 'r', 'utf-8')
for line in f:
    list.append(line)
f.close()

@bot.command(name='join')
async def joingame(ctx):
    if game.gameStatus == Status.WAITING:
        await ctx.channel.send(game.addPlayer(ctx.author))
        if game.numOfPlayers() == 4:
            await ctx.channel.send('All players found! Starting game...')
            game.startGame()
            turn = game.getPlayersTurn()
            await ctx.channel.send(str(game.players[turn].name)+'\'s turn to bid!')
            for player in game.players:
                await player.name.send(player.displayHand())
    elif game.gameStatus == Status.NOT_PLAYING:
        await ctx.channel.send('Game has not started. Use \'!startgame\' to start a game!')
    elif game.gameStatus == Status.IN_PROGRESS:
        await ctx.channel.send('Game has already started. Please wait for the current game to end.')


@bot.command(name='startgame')
async def startgame(ctx):
    if game.gameStatus == Status.NOT_PLAYING:
        game.initializeGame(ctx.channel)
        await ctx.channel.send('Game Started!')
        await ctx.channel.send(game.addPlayer(ctx.author))
    else:
        await ctx.channel.send('Game has already started!')


@bot.command(name='endgame')
async def endgame(ctx):
    if ctx.channel == game.gameChannel:
        await ctx.channel.send('Game Ended')
        game.endGame()
    else:
        await ctx.channel.send('You can only end game in the channel that started the game')


@bot.command(name='play')
async def playcard(ctx, arg):
    if game.gameStatus == Status.BIDDING:
        await ctx.send('Game Still in Bidding Phase!')
        return
    turn = game.getPlayersTurn()
    player = game.findPlayer(ctx.author)
    if player and game.players[turn].name == ctx.author:
        try:
            index = int(arg)
            if index < 0 or index > len(player.hand):
                raise ValueError
            card = player.playACard(index)
            game.addToSet(card, player)
            if game.hasRoundEnded():
                await game.gameChannel.send('End of current round!\n' + game.announceSetWinner())
                game.startNewRound()
            await player.name.send(player.displayHand())
            await game.gameChannel.send(str(player.name) + ' plays ' + card.showCard())
            game.nextPlayersTurn()
            turn = game.getPlayersTurn()
            await game.gameChannel.send(str(game.players[turn].name) + '\'s turn to play a card!')
        except ValueError:
            await player.name.send('Enter a valid card to play! e.g. \'!play 5\' to play the 5th card.')

    else:
        await ctx.channel.send('This command is only valid for players in the game, or it is not your turn yet.')


@bot.command(name='bid')
async def bid(ctx, *args):
    if game.gameStatus == Status.BIDDING:
        turn = game.getPlayersTurn()
        player = game.findPlayer(ctx.author)
        if player and game.players[turn].name == ctx.author:
            try:
                if args[0].lower() == "pass":
                    game.addPassCount()
                    await game.gameChannel.send(str(player.name) + ' bids to pass')
                    if game.getPassCount() == 3:
                        await game.gameChannel.send('All players have passed. Automatically ending bid phase.')
                        await game.gameChannel.send(game.announceBid())
                        game.setTrumpSuit()
                        game.startTurn()
                        turn = game.getPlayersTurn()
                        await game.gameChannel.send(str(game.players[turn].name) + '\'s turn to play a card!')
                    else:
                        game.nextPlayersTurn()
                        turn = game.getPlayersTurn()
                        await ctx.channel.send(str(game.players[turn].name) + '\'s turn to bid!')
                else:
                    bidValue, bidSuit = game.parseBidArg(args)
                    if game.checkValidBid(bidValue, bidSuit):
                        game.setBid(bidValue, bidSuit, player.name)
                        game.resetPassCount()
                        await game.gameChannel.send(str(player.name) + ' bids ' + str(bidValue) + " " + bidSuit.name)
                        game.nextPlayersTurn()
                        turn = game.getPlayersTurn()
                        await ctx.channel.send(str(game.players[turn].name) + '\'s turn to bid!')
                    else:
                        await game.gameChannel.send('Invalid bid. Please bid higher than the previous bid')
                        return
            except:
                await game.gameChannel.send('Invalid bid. Either \'!bid 2 Hearts\' to bid 1 Hearts or \'!bid pass\' to pass')

    else:
        await ctx.send('Invalid Command. Game not in bidding phase.')


@bot.command(name='trump')
async def trump(ctx):
    if game.gameStatus == Status.IN_PROGRESS:
        await game.gameChannel.send('The trump suit for this game is ' + game.trumpSuit.suit.name)
    elif game.gameStatus == Status.BIDDING or game.gameStatus == Status.WAITING:
        await game.gameChannel.send('The trump suit for this game is not decided yet.')
    else:
        await ctx.channel.send('There is no game currently.')


@bot.command(name='WAT')
async def wat(ctx, *arg):
    try:
        if arg:
            index = int(arg[0])
            if index >= len(list) or index < 0:
                raise ValueError
        else:
            index = random.randint(0, len(list) - 1)
    except ValueError:
        index = random.randint(0, len(list)-1)

    await ctx.channel.send(list[index])


@bot.command(name='add')
async def add(ctx, *args):
    input = ' '.join(args)
    list.append(input)
    await ctx.channel.send(input + " has been added")
    f = codecs.open('wat_list.txt', 'a', 'utf-8')
    f.write(input + '\n')
    f.close()

