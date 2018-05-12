import discord

client = discord.Client()

@client.event
async def on_ready():
    global listnum
    
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_member_join(member):
    server = member.server
    channel = [channel for channel in client.get_all_channels()
    if channel.id == '419780533011087371'][0]
    m = "#LBGへようこそ! " + member.mention + " 設定をするから[!register]って打ってね！"
    await client.send_message(channel, m)

client.run("NDQyNjM0NjMyNzQ0MjcxODcy.DdCs2A.2mzJJI3CApn-btM6Xbz5spAycMo")