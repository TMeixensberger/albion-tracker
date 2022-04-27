import discord
import asyncio
from playerDeathStorage import PlayerDeathStorage
from playerKillStorage import PlayerKillStorage
from fightRender import FighRenderer


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.channel}: {0.content}'.format(message))


client = MyClient()

###


def formatTime(timestamp):
    dateTimeSep = timestamp.find('T')
    date = timestamp[:timestamp.find('T')]
    time = timestamp[int(dateTimeSep + 1): timestamp.find('.')]
    timeParts = time.split(':')
    timeParts[0] = str(int(timeParts[0]) + 2)
    time = ':'.join(timeParts)
    return date + " " + time


debug = False


async def sendMessage(channel, msg):
    if not debug:
        await channel.send(msg)
    else:
        print(msg)


async def sendImage(channel, img):
    if not debug:
        await channel.send(file=discord.File(img))
    else:
        print(img)


async def my_background_task():
    await client.wait_until_ready()
    channel = discord.utils.get(client.get_all_channels(), name="albion-kills")
    # channel = client.get_channel(id="albion-kills")  # replace with channel_id

    deathStorages = [PlayerDeathStorage(
        "MixiHD"), PlayerDeathStorage("DennisRG")]
    killStorages = [PlayerKillStorage("MixiHD"), PlayerKillStorage(
        "DennisRG"), PlayerKillStorage("ErzaScarletX765")]
    while not client.is_closed():
        ##########################
        for deathStorage in deathStorages:
            deathStorage.refresh()
            if deathStorage.unpostedDeathsAvailable():
                deathData = deathStorage.getUnpostedDeaths()
                for deathId in deathData:
                    death = deathData[deathId]["data"]
                    victim = death["Victim"]["Name"]
                    killer = death["Killer"]["Name"]
                    time = death["TimeStamp"]
                    eventId = death["EventId"]

                    msg = "{0} was killed by {1} at {2}!".format(
                        victim, killer, formatTime(time))
                    await sendMessage(channel, msg)

                    fightRender = FighRenderer(
                        death["Killer"], death["Victim"])
                    await sendImage(channel, fightRender.generate())

                    msg = "For more details about the death visit\n{0}".format(
                        "https://albiononline.com/en/killboard/kill/{0}".format(str(eventId)))
                    await sendMessage(channel, msg)

        ##########################
        for killStorage in killStorages:
            killStorage.refresh()
            if killStorage.unpostedKillsAvailable():
                deathData = killStorage.getUnpostedKills()
                for deathId in deathData:
                    death = deathData[deathId]["data"]
                    victim = death["Victim"]["Name"]
                    killer = death["Killer"]["Name"]
                    time = death["TimeStamp"]
                    eventId = death["EventId"]

                    msg = "{0} killed {1} at {2}!".format(
                        killer, victim, formatTime(time))
                    await sendMessage(channel, msg)

                    fightRender = FighRenderer(
                        death["Killer"], death["Victim"])
                    await sendImage(channel, fightRender.generate())

                    msg = "For more details about the kill visit\n{0}".format(
                        "https://albiononline.com/en/killboard/kill/{0}".format(str(eventId)))
                    await sendMessage(channel, msg)

        ##########################
        await asyncio.sleep(20)  # task runs every 60 seconds

client.loop.create_task(my_background_task())
###
client.run('token')
