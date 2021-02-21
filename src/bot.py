import discord
from discord.ext import commands
from src import Bridge, Blackjack
from src.Bridge import Status
import random
import codecs

bot = commands.Bot(command_prefix='!')
game = Bridge.Bridge()
blackjack = Blackjack.Blackjack()
list = []
f = codecs.open('wat_list.txt', 'r', 'utf-8')
for line in f:
    list.append(line)
f.close()

@bot.command(name='join')
async def joingame(ctx):
    if blackjack.gameStatus == Blackjack.Status.WAITING:
        output = blackjack.addPlayer(ctx.author)
        for player in blackjack.players:
            await player.name.send(output)
        return
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
            await player.name.send(player.displayHand())
            await game.gameChannel.send(str(player.name) + ' plays ' + card.showCard())
            if game.hasRoundEnded():
                await game.gameChannel.send('End of current round!\n' + game.announceSetWinner())
                game.startNewRound()
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
        await game.gameChannel.send('The trump suit for this game is ' + game.trumpSuit.name)
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
    if input.find('@') >= 0:
        await ctx.channel.send('@ detected. No tags allowed.')
    else:
        list.append(input)
        await ctx.channel.send(input + " has been added")
        f = codecs.open('wat_list.txt', 'a', 'utf-8')
        f.write(input + '\n')
        f.close()


@bot.command(name='blackjack')
async def playBlackjack(ctx):
    print(blackjack.gameStatus)
    if blackjack.gameStatus == Blackjack.Status.NOT_PLAYING:
        blackjack.initializeGame(ctx.channel)
        await ctx.channel.send('Game Started!')
        await ctx.channel.send(blackjack.addPlayer(ctx.author))
    else:
        await ctx.channel.send('Game has already started!')


@bot.command(name='start')
async def start(ctx):
    if blackjack.gameStatus == Blackjack.Status.WAITING and blackjack.numOfPlayers() >= 2:
        output = blackjack.checkRoundStart()
        if output == 'Valid':
            blackjack.setGameStatus(Blackjack.Status.IN_PROGRESS)
            blackjack.startRound()
            for player in blackjack.players:
                await player.name.send(player.displayHand())
                await player.name.send(player.displayScore())
                turn = blackjack.round.getTurn()
                await player.name.send(str(blackjack.players[turn].name) + '\'s turn to draw!')
        else:
            for player in blackjack.players:
                await player.name.send(output)


@bot.command(name='banker')
async def getbanker(ctx):
    banker = blackjack.getDealer()
    await ctx.channel.send('Banker of the game is: ' + str(banker.name))


@bot.command(name='beBanker')
async def setbanker(ctx):
    output = blackjack.setDealer(ctx.author)
    for player in blackjack.players:
        await player.name.send(output)


@bot.command(name='bet')
async def bet(ctx, arg):
    player = blackjack.findPlayer(ctx.author)
    if player:
        if blackjack.gameStatus == Blackjack.Status.WAITING:
            try:
                betValue = int(arg)
                player.setBet(betValue)
                for all_player in blackjack.players:
                    await all_player.name.send(str(player.name) + ' has bet ' + str(betValue))
            except ValueError:
                await player.name.send('Invalid Bet Amount')
        elif blackjack.gameStatus == Blackjack.Status.IN_PROGRESS:
            await ctx.channel.send('You cannot change your bet while it is being played!')
    else:
        await ctx.channel.send('Either there are no games currently, or you are not in the game.')


@bot.command(name='hit')
async def hit(ctx):
    currentTurn = blackjack.round.getTurn()
    currentPlayer = blackjack.getPlayerByIndex(currentTurn)
    if currentPlayer.name == ctx.author:
        blackjack.round.hitCard()
        await currentPlayer.name.send(currentPlayer.displayHand())
        await currentPlayer.name.send(currentPlayer.displayScore())
    else:
        await ctx.channel.send('This command is only valid for players in the game, or it is not your turn yet.')

    # if currentTurn is not blackjack.round.getTurn():
    #     turn = blackjack.round.getTurn()
    #     if blackjack.players[turn] == blackjack.dealer:
    #         for player in blackjack.players:
    #             await player.name.send(blackjack.round.announceRoundResults())
    #             await player.name.send(blackjack.endRound())
    #         blackjack.setGameStatus(Blackjack.Status.WAITING)
    #     else:
    #         for player in blackjack.players:
    #             await player.name.send(str(blackjack.players[turn].name) + '\'s turn to draw!')
    #         await blackjack.players[turn].name.send(blackjack.players[turn].displayHand())
    #         await blackjack.players[turn].name.send(blackjack.players[turn].displayScore())


@bot.command(name='pass')
async def stand(ctx):
    currentTurn = blackjack.round.getTurn()
    if blackjack.getPlayerByIndex(currentTurn).name == ctx.author:
        if blackjack.players[currentTurn] == blackjack.dealer:
            output = blackjack.round.announceRoundResults()
            for player in blackjack.players:
                await player.name.send(output)
                await player.name.send(blackjack.endRound())
            blackjack.setGameStatus(Blackjack.Status.WAITING)
        else:
            blackjack.round.setNextTurn()
            turn = blackjack.round.getTurn()
            for player in blackjack.players:
                await player.name.send(str(blackjack.players[turn].name) + '\'s turn to draw!')
            await blackjack.players[turn].name.send(blackjack.players[turn].displayHand())
            await blackjack.players[turn].name.send(blackjack.players[turn].displayScore())
    else:
        await ctx.channel.send('This command is only valid for players in the game, or it is not your turn yet.')


@bot.command(name='leave')
async def leaveGame(ctx):
    if blackjack.findPlayer(ctx.author):
        if blackjack.gameStatus == Blackjack.Status.WAITING:
            output = blackjack.removePlayer(ctx.author)
            for player in blackjack.players:
                await player.name.send(output)
        elif blackjack.gameStatus == Blackjack.Status.IN_PROGRESS:
            await ctx.channel.send('You cannot leave the game while it is being played!')
    else:
        await ctx.channel.send('Either there are no games currently, or you are not in the game.')


@bot.command(name='end')
async def endBlackjack(ctx):
    if blackjack.gameStatus == Blackjack.Status.WAITING:
        blackjack.setGameStatus(Blackjack.Status.NOT_PLAYING)


bot.run('ODA3OTgxNjk1NjMzODUwMzc4.YB_5lw.RRis0kx47k1ATPuSukw_c-p4-AE')

