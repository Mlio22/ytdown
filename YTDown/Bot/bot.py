from discord import Game
from discord.ext.commands import Bot
from .query import Query, Queries
from YTDown.Drive.period import PeriodList
import asyncio
from threading import Thread

# initialization
BOT_PREFIX = ("$")
client = Bot(BOT_PREFIX)
query_list = Queries()

period_list = PeriodList()
loop = asyncio.get_event_loop()


# pre-command functions
def deleteprevquery(message):
    query = query_list.checkuserquery(message)
    if query:
        query_list.deletequery(query)


def addquery(message, url, flags, querytype):
    Query(
        message.author,
        {
            'period_list': period_list,
            'query_list': query_list,
            'message': message,
            'url': url,
            'flags': flags,
            'current_loop': loop
        },
        querytype
    )


# command lists

# get video
@client.command()
async def video(ctx, url, *flags):
    print("accepting video task")
    message = ctx.message

    deleteprevquery(message)

    thread = Thread(target=addquery(message, url, flags, 'video'), daemon=True)
    thread.start()


@client.command()
async def sub(ctx, url, *flags):
    print("accepting subtitle task")
    message = ctx.message

    deleteprevquery(message)

    thread = Thread(target=addquery(message, url, flags, 'sub'), daemon=True)
    thread.start()


@client.command()
async def alls(ctx, url, *flags):
    print("acceptiong alls task")
    message = ctx.message

    deleteprevquery(message)

    thread0 = Thread(target=addquery(message, url, flags, 'alls'), daemon=True)
    thread0.start()


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
