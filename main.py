import discord
import os
import random
import sys
from PIL import Image, ImageDraw, ImageFilter

client = discord.Client()

#             0     1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20    21    22    23    24    25    26    27    28    29    30    31    32    33    34    35    36    37    38
job_list = ['ACR','ALC','ARC','ASN','BAR','BER','BLO','BUI','CIV','DAS','DEF','ENC','ENG','FAR','HAN','HEA','HUN','ICE','IMM','LUM','MAR','MIN','NIN','PYR','RIF','ROB','SCP','SCO','SNI','SPI','SPY','SUC','SWA','THO','TIN','TRA','VAM','WAR','WIZ']
rank_list = [['UnRanked','UnRanked','UnRanked'],['Novice-Ⅰ','Novice-Ⅱ','Novice-Ⅲ'],['Silver-Ⅰ','Silver-Ⅱ','Silver-Ⅲ'],['Gold-Ⅰ','Gold-Ⅱ','Gold-Ⅲ'],['Master-Ⅰ','Master-Ⅱ','Master-Ⅲ'],['Grand Master-Ⅰ','Grand Master-Ⅱ','Grand Master-Ⅲ'],['Annihilator','Annihilator','Annihilator']]
yes_list = ['はい','うん','そうだよ','大丈夫','yes','ok','ああ']
ang_list = ['もー！ちゃんとしてよ！',':angry:']
listnum = 0

#ユーザデータを取得する関数,sで情報を指定。不正なときはNickNameを返す
#返り値の型は基本stringだが、jobを指定した場合のみlist(str)型で返す
def get_userdata(userid,s):
    
    try:
        f = open( 'saves\\' + userid + '.txt', 'r')
    except FileNotFoundError:
        return False
    
    x = 0
    
    if s == "MCID":
        x = 1
    elif s == "rank":
        x = 2
    elif s == "job":
        x = 3
    elif s == "listNum":
        x = 4
    elif s == "ALL":
        x = -1
    
    txt = f.readlines()
    f.close()
    data = []
    for y in txt:
        data.append(y[:-1])
    if((x >= 0) and (x <= 4)):
        if x == 3:
            a = data[3]
            return a.split(',')
        else:
            return data[x]
    else:
        return data


#ユーザidから職画像を生成して保存する関数
def create_pic(userid):
    username = get_userdata(userid,'NickName')
    joblist = get_userdata(userid,'job')
    #img読み込み
    imbase = Image.open('img\\job\\list_base.png')
    img = []
    for n in range(39):
        im = Image.open('img\\job\\' + str(n) + '.png')
        img.append(im)
    #画像処理
    back_im = imbase.copy()
    count = 0
    num = 0
    x = 10
    y = 30
    for a in joblist:
        if a == '1':
            back_im.paste(img[num], (x, y))
            count += 1
            if (count >= 0)and(count <= 8):
                x = 10 + (36 * count)
                y = 30
            elif (count >= 9)and(count <= 17):
                x = 10 + (36 * (count - 9))
                y = 66
            elif (count >= 18)and(count <= 26):
                x = 10 + (36 * (count - 18))
                y = 102
            elif (count >= 27)and(count <= 35):
                x = 10 + (36 * (count - 27))
                y = 138
            elif (count >= 36)and(count <= 44):
                x = 10 + (36 * (count - 36))
                y = 174
        num += 1
    
    back_im.save('img\\userimg\\' + userid + '.png', quality=95)
    print(username + "の職画像を保存しました")
        
#ユーザidから解放済みの職をアルファベット3字で[,]を区切りとしてstringとして返す関数
def get_jobs(userid):
    joblist = get_userdata(userid,'job')
    count = 0
    s = ""
    for n in joblist:
        if n == '1':
            s += job_list[count] + ","
        count += 1
    return s[:-1]

@client.event
async def on_ready():
    global listnum
    
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    f = open( 'hatchandata\\listnum.txt', 'r')
    listnum = int(f.read())
    f.close()

@client.event
async def on_message(message):
    global listnum
    def check(msg):
        return msg.content
    
    Flag = 1
    #送信者が初めてかどうかをファイルで判別する
    try:
        f = open( 'saves\\' + message.author.id + '.txt', 'r')
    except FileNotFoundError:
        Flag = 0
    if Flag == 1:
        f.close()
    
    if message.content.startswith('!register'):
        if client.user != message.author:
            if Flag == 1:
                m = "もう！" + str(get_userdata(message.author.id, 'NickName')) + "！これは初めての人だけのコマンドだよ！！"
                await client.send_message(message.channel, m)
            else:
                data = []
                m = "初めまして！" + message.author.name + "さん！"
                await client.send_message(message.channel, m)
                count = 0
                while True:
                    m = "何て呼べばいいかな?"
                    await client.send_message(message.channel, m)
                    message = await client.wait_for_message(author=message.author, check=check)
                    nickname = message.content.strip()
                    m = "[" + nickname + "] って呼べばいいのかな?"
                    if count == 1:
                        m += "\n良かったら[はい]って言ってほしいな"
                    await client.send_message(message.channel, m)
                    message = await client.wait_for_message(author=message.author, check=check)
                    if (str(message.content.strip()) in yes_list) == True:
                        break
                    count = 1
                data.append(nickname)
                m = "おっけー！じゃあ" + nickname + "！"
                await client.send_message(message.channel, m)
                count = 0
                while True:
                    m = "初期設定をするからMCIDを教えてね！"
                    await client.send_message(message.channel, m)
                    message = await client.wait_for_message(author=message.author, check=check)
                    mcid = message.content.strip()
                    m = "MCIDは[" + mcid + "] で大丈夫かな?"
                    if count == 1:
                        m += "\n良かったら[はい]って言ってほしいな"
                    await client.send_message(message.channel, m)
                    message = await client.wait_for_message(author=message.author, check=check)
                    if (str(message.content.strip()) in yes_list) == True:
                        break
                    count = 1
                data.append(mcid)
                m = "MCIDは" + mcid + "だね！覚えたよ！"
                await client.send_message(message.channel, m)
                m = "じゃあ、Anniのランクも番号(半角数字)で教えて！\nUnRanked => 1\nNovice => 2\nSilver => 3\nGold => 4\nMaster => 5\nGrandMaster => 6\nAnnihilator => 7\nランクはAnniロビーで[/rank]すると確かめられるよ。"
                while True:
                    await client.send_message(message.channel, m)
                    message = await client.wait_for_message(author=message.author, check=check)
                    rank1 = message.content.strip()
                    if rank1.isdigit() == False:
                        m = random.choice(ang_list)
                        await client.send_message(message.channel, m)
                        m = "Anniのランクを番号(半角数字)で教えて！"
                    elif((int(rank1) == 1)or(int(rank1) == 7)):
                        m = "おっけー！"
                        await client.send_message(message.channel, m)
                        data.append(rank_list[int(rank1)-1][2])
                        break
                    elif((int(rank1) >= 2)and(int(rank1) <= 6)):
                        while True:
                            m = "ランクの数字はいくつ?"
                            await client.send_message(message.channel, m)
                            message = await client.wait_for_message(author=message.author, check=check)
                            rank2 = message.content.strip()
                            if rank2.isdigit() == False:
                                m = random.choice(ang_list)
                                await client.send_message(message.channel, m)
                                m = "Anniのランクを番号(半角数字)で教えて！"
                            elif((int(rank2) >= 1)and(int(rank2) <= 3)):
                                m = "おっけー！"
                                await client.send_message(message.channel, m)
                                data.append(rank_list[int(rank1)-1][int(rank2)-1])
                                break
                            else:
                                m = random.choice(ang_list)
                                await client.send_message(message.channel, m)
                                m = "Anniのランクを番号(半角数字)で教えて！"
                        break
                    else:
                        m = random.choice(ang_list)
                        await client.send_message(message.channel, m)
                        m = "Anniのランクを番号(半角数字)で教えて！"
                m = "MCID ==> " + data[1]
                m += "\nAnniRank ==>" + data[2]
                m += "\nこれが" + data[0] + "の情報だね！"
                await client.send_message(message.channel, m)
                jobs = ['0'] * 39
                jobs[8] = '1'
                for x in range(7):
                    for y in range(3):
                        if data[2] == rank_list[x][y]:
                            if x >= 1:
                                jobs[21] = '1'
                            if(x >= 1)and(y >= 1):
                                jobs[2] = '1'
                            if x >= 2:
                                jobs[37] = '1'
                            if(x >= 2)and(y >= 1):
                                jobs[1] = '1'
                            if(x >= 2)and(y >= 2):
                                jobs[15] = '1'
                            if x >= 3:
                                jobs[20] = '1'
                            if(x >= 3)and(y >= 2):
                                jobs[14] = '1'
                            if x >= 4:
                                jobs[26] = '1'
                job = ','.join(jobs)
                
                data.append(job)
                data.append(str(listnum))
                listnum += 1
                f = open( 'hatchandata\\listnum.txt', 'w')
                f.write(str(listnum))
                f.close()
                a = '\n'.join(data) + "\n"
                f = open( 'saves\\' + message.author.id + '.txt', 'w')
                f.write(a)
                f.close()
                m = "うん！覚えたよ！！"
                await client.send_message(message.channel, m)
                m = "後は #rule で使い方を確認してね"
                await client.send_message(message.channel, m)
                m = "購入済みの職業登録も忘れずにね！！"
                await client.send_message(message.channel, m)


    elif message.content.startswith('!img'):
        if client.user != message.author:
            if Flag == 0:
                m = "初めまして！" + message.author.name + "さん！\n"
                m += "まずは[!register]コマンドであなたのことを教えてね！"
                await client.send_message(message.channel, m)
            else:
                nickname = get_userdata(message.author.id, 'NickName')

                m = "職の画像を作るの?"
                await client.send_message(message.channel, m)
                m = "今" + nickname + "がもってる職は\n"
                m += get_jobs(message.author.id)
                m += "\nだって覚えてるけど、これで作っちゃって大丈夫?"
                await client.send_message(message.channel, m)
                message = await client.wait_for_message(author=message.author, check=check)
                if (str(message.content.strip()) in yes_list) == True:
                    m = "おっけー！じゃあちょっと待ってて！"
                    await client.send_message(message.channel, m)
                    create_pic(message.author.id)
                    m = "はい！できました！！"
                    await client.send_message(message.channel, m)
                    await client.send_file(message.channel,'img\\userimg\\' + message.author.id + '.png')
                else:
                    m = "おっけー！ちゃんと持ってる職を教えてからまた教えて！"
                    await client.send_message(message.channel, m)


    elif message.content.startswith('!job'):
        if client.user != message.author:
            if Flag == 0:
                m = "初めまして！" + message.author.name + "さん！\n"
                m += "まずは[!register]コマンドであなたのことを教えてね！"
                await client.send_message(message.channel, m)
            else:                
                m = ""
                
client.run("NDQyNjM0NjMyNzQ0MjcxODcy.DdCs2A.2mzJJI3CApn-btM6Xbz5spAycMo")
