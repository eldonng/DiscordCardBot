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
            await ctx.channel.send(str(game.players[turn].name)+'\'s turn to play a card!')
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
        print(ctx.channel)
        print(ctx.author)
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
            await ctx.channel.send(str(game.players[turn].name) + '\'s turn to play a card!')
        except ValueError:
            await player.name.send('Enter a valid card to play! e.g. \'!play 5\' to play the 5th card.')

    else:
        await ctx.channel.send('This command is only valid for players in the game, or it is not your turn yet.')

bot.run('TOKEN')
