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
            m = "出す手を✊か✌か🖐から選んでね!"
            await client.send_message(message.channel, m)
            message = await client.wait_for_message(author=message.author, check=check)
            user = message.content.strip()
            try:
                user_choice = dic[user]

                choice_list = ["✊", "✌", "🖐"]
                bot = dic[random.choice(choice_list)]

                draw = '引き分けだよ!'
                win = 'あなたの勝ちだよ!'
                lose = 'やったぁ!'

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

                m = "あなたが選んだのは" + user_choice + "\nbotが選んだのは" + bot + "\n結果は" + judge
                await client.send_message(message.channel, m)

            except:
                m = "✊か✌か🖐を入力してね!"
                await client.send_message(message.channel, m)

client.run("NDQyNTg0MjI0NzU1ODc1ODQw.DdA8NA.vvtik-pKLr24fnHMlrwfVCTHau4")