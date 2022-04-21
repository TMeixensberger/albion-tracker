from os import kill
import discord
import asyncio
from playerDeathStorage import PlayerDeathStorage
from playerKillStorage import PlayerKillStorage


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
    time = ''.join(timeParts)
    return date + " " + time


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

                    msg = "{0} was killed by {1} at {2}!\nhttps://albiononline.com/en/killboard/kill/{3}".format(
                        victim, killer, formatTime(time), str(eventId))
                    await channel.send(msg)
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
                    msg = "{0} killed {1} at {2}!\nhttps://albiononline.com/en/killboard/kill/{3}".format(
                        killer, victim, formatTime(time), str(eventId))
                    await channel.send(msg)
        ##########################
        await asyncio.sleep(20)  # task runs every 60 seconds

client.loop.create_task(my_background_task())
###
client.run('OTY0Njg4MDk1MDMzMzAzMDcx.YloRzA.y2Ebc4Sce5SAMK08ec2j0xBUi9w')
