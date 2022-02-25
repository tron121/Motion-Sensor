import discord.ext
import discord
import time
import MQTTListener
import CameraListener
import config

disc_client = discord.ext.commands.Bot(command_prefix = "?")
myKey = 'INSERT KEY HERE'

@disc_client.command
async def ping(message):
    await message.channel.send('Pong! {0}'.format(round(disc_client.latency, 1)))

@disc_client.event
async def on_ready():
    print('Welcome back Pilot, I have initialized as {0.user}'.format(disc_client))
    config.general_channel = disc_client.get_channel(695346443703287849)
    config.info_channel = disc_client.get_channel(695346605364346960)
    config.guild_id = disc_client.get_guild(695346443275468893)
    config.is_ready = True
    config.alert_role = discord.utils.get(config.guild_id.roles, name="DoorStatus")
    print(config.guild_id)
    print(config.general_channel)
    print(config.info_channel)
    print(disc_client.latency)

@disc_client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 702993733091852308:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, disc_client.guilds)
        if payload.emoji.name ==':white_check_mark:':
            config.alert_role= discord.utils.get(guild.roles, name='DoorStatus')
        if config.alert_role is not None:
            member= discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(config.alert_role)
            else:
                print("Member not found")
        else:
            print("Role not found")

@disc_client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 702993733091852308:
        guild_id=payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, disc_client.guilds)
        if payload.emoji.name == ':white_check_mark:':
        config.alert_role = discord.utils.get(guild.roles, name='DoorStatus')
       if config.alert_role is not None:
           member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
           if member is not None:
               await member.remove_roles(config.alert_role)
           else:
               print("Member not found")
       else:
           print("Role not found")

@disc_client.event
async def on_message(message):
   if message.author == disc_client.user:
       return
   if message.content.startswith('$hello'):
       await message.channel.send('Hello!')
   if message.content.startswith('$doorstatus'):
       await message.channel.send('The door is currently: ' + str(config.door_status))
   if message.content.startswith('$statusrole'):
       await message.author.add_roles(config.alert_role)
   if message.content.startswith('$removestatusrole'):
       await message.author.remove_roles(config.alert_role)
   if message.content.startswith('$ping'):
       await message.channel.send('Pong! {0}'.format(round(disc_client.latency, 3)))
   if message.content.startswith('$mentionme'):
       await message.channel.send(f"{config.alert_role.mention} the door is opened")
   if message.content.startswith('$statustime'):
       await message.channel.send('The door was: ' + str(config.door_status) + ' for: '+ str(round(config.hours, 2)) +' Hours ' +
                                  str(round(config.minutes, 2)) + ' Minutes ' + str(round(config.seconds, 2)) + ' Seconds')


if __name__ == "__main__":
   MQTTListener = MQTTListener.MQTTListenerCog()
   #CameraListener = CameraListener.CameraListenerCog()
   disc_client.add_cog(MQTTListener)
   #disc_client.add_cog(CameraListener)
   disc_client.run(myKey)
