import discord
from discord.ext import commands
from src import Bridge
from src.Bridge import Status

bot = commands.Bot(command_prefix='!')
game = Bridge.Bridge()


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
        game.setGameChannel(ctx.channel)
        game.trumpSuit = None
        game.currentBid = (0,0)
        game.setGameStatus(Status.WAITING)
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
            print(player.name)
            print(index)
            card = player.playACard(index)
            await player.name.send(player.displayHand())
            await game.gameChannel.send(str(player.name) + ' discards ' + card.showCard())
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
                        await game.gameChannel.send('All players have passed. Use \'!endbid\' to complete bidding phase.')
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


@bot.command(name='endbid')
async def endbid(ctx):
    await game.gameChannel.send(game.announceBid())
    game.setTrumpSuit()
    game.startTurn()
    turn = game.getPlayersTurn()
    await ctx.channel.send(str(game.players[turn].name) + '\'s turn to play a card!')


bot.run('TOKEN')
