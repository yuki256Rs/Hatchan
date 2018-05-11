import discord
import random

dic = {"✊": "グー", "✌": "チョキ", "🖐": "パー"}


client = discord.Client()

@client.event
async def on_ready():
    print('------')
    print(client.user.name)
    print(client.user.id)
    print('Logged in us')
    print('------')

dic = {"✊": "グー", "✌": "チョキ", "🖐": "パー"}

@client.event
async def on_message(message):
    def check(msg):
        return msg.content
    if message.content.startswith("じゃんけん"):
        if client.user != message.author:
            while True:
                m = "出す手を✊か✌か🖐から選んでね"
                await client.send_message(message.channel, m)
                message = await client.wait_for_message(author=message.author, check=check)
                user = message.content.strip()
                if user == "じゃんけん":
                    m = "ちゃんとしてよ!"
                    await client.send_message(message.channel, m)
                    break
                else:
                    pass


                try:
                    user_choice = dic[user]

                    choice_list = ["✊", "✌", "🖐"]
                    bot = dic[random.choice(choice_list)]

                    draw = "引き分けだよ!"
                    win = message.author.name + "さんの勝ちだよ!"
                    lose = "やったぁ!勝った!"

                    if user_choice == bot:
                        judge = draw
                    else:
                        if user_choice == "グー":
                            if bot == "チョキ":
                                judge = win
                            else:
                                judge = lose

                        elif user_choice == "チョキ":
                            if bot == "パー":
                                judge = win
                            else:
                                judge = lose

                        else:
                            if bot == "グー":
                                judge = win
                            else:
                                judge = lose

                    m = message.author.name + "さんが選んだのは" + user_choice + "\n私が選んだのは" + bot + "\n" + judge
                    await client.send_message(message.channel, m)
                    break

                except:
                    m = "ちゃんと選んでよ!"
                    await client.send_message(message.channel, m)

client.run("token")