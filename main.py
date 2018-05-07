import discord
import os

client = discord.Client()
#             0     1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20    21    22    23    24    25    26    27    28    29    30    31    32    33    34    35    36    37    38
job_list = ["ACR","ALC","ARC","ASN","BAR","BER","BLO","BUI","CIV","DAS","DEF","ENC","ENG","FAR","HAN","HEA","HUN","ICE","IMM","LUM","MAR","MIN","NIN","PYR","RIF","ROB","SCO","SCP","SNI","SPI","SPY","SUC","SWA","THO","TIN","TRA","VAM","WAR","WIZ"]

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    
    if message.content.startswith("!help"):
        if client.user != message.author:
            m = "__**～ ⑨でも分かる！  BOTの使い方！ ～**__\n\n"
            m += "**!save**   職保存用コマンド。職画像を添付して送信してね！\n"
            m += "**!list**   職が登録されている人のリストを表示するコマンドだよ！\n"
            m += "**!show**   職を表示するコマンド。続けて名前かリストの番号を入力すると表示されるよ！\n"
            m += "**!add**   持ってる職を登録する時のコマンドだよ！\n"
            m += "**!remove**    間違えて登録した時のコマンドだよ！\n"
            m += "**!search**    特定の職を持ってる人を検索できるよ！\n"
            m += "**!num**   職と番号のつながりを表示するよ！長くなるからね！！"
            await client.send_message(message.channel, m)

    elif message.content.startswith("!save"):
        if client.user != message.author:
            if len(message.attachments) == 1:
                url = message.attachments[0]['url']
                f = open( 'save_img\\' + message.author.name + '.txt', 'w')
                f.write(url)
                f.close()
                m = message.author.name + "の職を保存したよ！"
                await client.send_message(message.channel, m)
            elif("http" in message.content):
                if(message.content[6:10] == "http"):
                    url = message.content[6:]
                    f = open( 'save_img\\' + message.author.name + '.txt', 'w')
                    f.write(url)
                    f.close()
                    m = message.author.name + "の職を保存したよ！"
                else:
                    m = "URLで職を保存するときは [!save]コマンドとURLの間に半角スペースを入れて、それ以外は何も入れないでね！"
                await client.send_message(message.channel, m)
                
            else:
                m = "!saveは職保存用のコマンドだから画像を添付してね！"
                await client.send_message(message.channel, m)

    elif message.content.startswith("!list"):
        path = "./save_img"
        names = os.listdir(path)
        m = "職が登録されている人のリストを書くよ！\n\n"
        num = 0
        for name in names:
            if(name[-4:] == '.txt'):
                num += 1
                m += "+" + str(num) + "+.`" + name[:-4] + "`\n" 
        await client.send_message(message.channel, m)

    elif message.content.startswith("!show"):
        num = 0
        if client.user != message.author:
            path = "./save_img"
            files = os.listdir(path)
            for x in files:
                num += 1
                if(x[-4:] == '.txt'):
                    y = x[:-4]
                    if y in message.content:
                        m = y + "の職はこれだ！\n"
                        f = open( 'save_job\\' + y + '.txt', 'r')
                        a = f.read()
                        f.close()
                        li = a.split(',')
                        b = 0
                        for z in li:
                            if z == "1":
                                m += job_list[b] + ","
                            b += 1
                        m = m[:-1] + "\n"
                        f = open( 'save_img\\' + y + '.txt', 'r')
                        m += f.read()
                        f.close()
                        await client.send_message(message.channel, m)
                    if "+" + str(num) + "+" in message.content:
                        m = y + "の職はこれだ！\n"
                        f = open( 'save_job\\' + y + '.txt', 'r')
                        a = f.read()
                        f.close()
                        li = a.split(',')
                        b = 0
                        for z in li:
                            if z == "1":
                                m += job_list[b] + ","
                            b += 1
                        m = m[:-1] + "\n"
                        f = open( 'save_img\\' + y + '.txt', 'r')
                        m += f.read()
                        f.close()
                        await client.send_message(message.channel, m)

    elif message.content.startswith("!add"):
        if client.user != message.author:
            m = ""
            
            #ファイルを読み込んで、ファイルが存在しない場合はCIVのみ解放状態でファイルを新規作成する
            while True:
                try:
                    f = open( 'save_job\\' + message.author.name + '.txt', 'r')
                    break
                except FileNotFoundError:
                    f = open( 'save_job\\' + message.author.name + '.txt', 'w')
                    f.write("0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
                    m = message.author.name + "の職登録は初めてだね！\nCIVだけはこっちで追加するよ！あとは自分でやってね\n\n"
                    f.close()
            a = f.read()
            f.close()
            li = a.split(',')
            num = 0
            for x in job_list:
                #追加で職(アルファベット3字)が入力された場合
                if x in message.content:
                    li[num] = "1"
                    m += x + ","
                #追加で職(番号)が入力された場合
                if "&" + str(num+1) in message.content:
                    li[num] = "1"
                    m += x + ","
                num += 1
            #CIVだけ
            li[8] = "1"
            #listを文字列にしてファイルに書き込んで終わり    
            a = ','.join(li)
            f = open( 'save_job\\' + message.author.name + '.txt', 'w')
            f.write(a)
            f.close()

            m = m[:-1] + "\nを" + message.author.name + "の職に登録したよ！"
            await client.send_message(message.channel, m)

    elif message.content.startswith("!remove"):
        if client.user != message.author:
            m = ""
            Flag = 1
            
            #ファイルを読み込んで、ファイルが存在しない場合はCIVのみ解放状態でファイルを新規作成する
            while True:
                try:
                    f = open( 'save_job\\' + message.author.name + '.txt', 'r')
                    break
                except FileNotFoundError:
                    f = open( 'save_job\\' + message.author.name + '.txt', 'w')
                    f.write("0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
                    m = message.author.name + "の職登録は初めてだね！\nCIVだけはこっちで追加するよ！!addコマンドで職を登録してね！\n\n"
                    f.close()
                    Flag = 0
            a = f.read()
            f.close()
            li = a.split(',')
            num = 0
            if Flag == 1:
                for x in job_list:
                    #追加で職(アルファベット3字)が入力された場合
                    if x in message.content:
                        li[num] = "0"
                        m += x + ","
                    #追加で職(番号)が入力された場合
                    if "&" + str(num+1) in message.content:
                        li[num] = "0"
                        m += x + ","
                    num += 1
                #CIVだけ
                li[8] = "1"
                #listを文字列にしてファイルに書き込んで終わり    
                a = ','.join(li)
                f = open( 'save_job\\' + message.author.name + '.txt', 'w')
                f.write(a)
                f.close()
                m = m[:-1] + "\nを" + message.author.name + "の職から削除したよ！"
                
            await client.send_message(message.channel, m)

    elif message.content.startswith("!num"):
        if client.user != message.author:
            num = 1
            m = "```"
            for a in job_list:
                m += a + " ==> &" + str(num) + "\n"
                num += 1
            m += "```"
            await client.send_message(message.channel, m)

    elif message.content.startswith("!search"):
        if client.user != message.author:
            Flag2 = 0
            #namelistに保存されてる人の名前を列挙する
            namelist = []
            Flag = 1
            m = "職 "
            path = "./save_job"
            names = os.listdir(path)
            for name in names:
                name = name[:-4]
                namelist.append(name)
            num = 0
            for x in job_list:
                if x not in message.content and "&" + str(num+1) + "&" not in message.content:
                    Flag2 += 1
                if x in message.content:
                    m += x + ","
                    num2 = 0
                    for y in namelist:
                        Flag = 1
                        #検索された内容の職を各namelistの人がもっているかどうかを判定
                        while True:
                            try:
                                f = open( 'save_job\\' + y + ".txt", 'r')
                                break
                            except FileNotFoundError:
                                Flag = 0
                                break
                        if Flag == 1:
                            a = f.read()
                            f.close()
                            li = a.split(',')

                            if li[num] == "0":
                                namelist[num2] = "exception"
                                
                            num2 += 1
                if "&" + str(num+1) + "&" in message.content:
                    m += x + ","
                    num2 = 0
                    for y in namelist:
                        Flag = 1
                        #検索された内容の職を各namelistの人がもっているかどうかを判定
                        while True:
                            try:
                                f = open( 'save_job\\' + y + ".txt", 'r')
                                break
                            except FileNotFoundError:
                                Flag = 0
                                break
                        if Flag == 1:
                            a = f.read()
                            f.close()
                            li = a.split(',')

                            if li[num] == "0":
                                namelist[num2] = "exception"
                                
                            num2 += 1
                num += 1

            if(Flag2 <= 38):
                m = m[:-1] + "を持っている人は"
                if len(namelist) <= 0:
                    m += "見つからなかったよ…"
                else:
                    m += "\n"
                    for name in namelist:
                        if name[-9:] != "exception":
                            m += name + ","
                    m = m[:-1] + "だよ！"
            else:
                m = "それは存在しない職だよ"

            await client.send_message(message.channel, m)

client.run("NDQyNjM0NjMyNzQ0MjcxODcy.DdCs2A.2mzJJI3CApn-btM6Xbz5spAycMo")
