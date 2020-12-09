from discord import Game
from discord.ext.commands import Bot
from .query import Query, Queries
from .fetchcommand import fetchyoutubevideoedata, fetchyoutubesubdata
from YTDown.Drive.period import PeriodList
import asyncio
from threading import Thread

# initialization
BOT_PREFIX = ("$")
client = Bot(BOT_PREFIX)
query_list = Queries()

period_list = PeriodList()
loop = asyncio.get_event_loop()


# command lists

# get video
@client.command()
async def video(ctx, url, *flags):
    print("accepting video task")
    message = ctx.message

    def fetchvideodata(currentloop):
        # checking user in query
        query = query_list.checkuserquery(message)
        if query:
            query_list.deletequery(query)

        Query(
            message.author,
            properties={
                'period_list': period_list,
                'query_list': query_list,
                'message': message,
                'url': url,
                'flags': flags,
                'current_loop': currentloop
            },
            startfunction=fetchyoutubevideoedata
        )

    thread = Thread(target=fetchvideodata(loop), args=(loop,), daemon=True)
    thread.start()


@client.command()
async def sub(ctx, url, *flags):
    print("accepting subtitle task")
    message = ctx.message

    def fetchsubdata(currentloop):
        query = query_list.checkuserquery(message)
        if query:
            query_list.deletequery(query)

        Query(
            message.author,
            properties={
                'period_list': period_list,
                'query_list': query_list,
                'message': message,
                'url': url,
                'flags': flags,
                'current_loop': currentloop
            },
            startfunction=fetchyoutubesubdata
        )

    thread = Thread(target=fetchsubdata(loop), args=(loop,), daemon=True)
    thread.start()


# cancel previous query
@client.command()
async def cancel(ctx):
    print("canceling")
    query = query_list.checkuserquery(ctx.message)

    if query:
        query_list.deletequery(query)


# event lists

@client.event
async def on_ready():
    print("logged in as ", client.user.name)
    await client.change_presence(activity=Game(name="With Humans"))


@client.event
async def on_message(message):
    if message.content.startswith('$'):
        await client.process_commands(message)
    else:
        query = query_list.checkuserquery(message)
        if query:
            query.setproperty('message', message)
            print("running thread")

            thread = Thread(target=query.runqueryfunction, daemon=True)
            query.addthread(thread)

            thread.start()


@client.event
async def on_reaction_add(reaction, *other):
    print(reaction, other)


# main
def run_bot(token):
    client.run(token)
