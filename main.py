import discord
import os
import random
import sys
import copy
from PIL import Image, ImageDraw, ImageFilter

client = discord.Client()

#             0     1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19    20    21    22    23    24    25    26    27    28    29    30    31    32    33    34    35    36    37    38
job_list = ['ACR','ALC','ARC','ASN','BAR','BER','BLO','BUI','CIV','DAS','DEF','ENC','ENG','FAR','HAN','HEA','HUN','ICE','IMM','LUM','MER','MIN','NIN','PYR','RIF','ROB','SCP','SCO','SNI','SPI','SPY','SUC','SWA','THO','TIN','TRA','VAM','WAR','WIZ']
rank_list = ['UnRanked','Novice-Ⅰ','Novice-Ⅱ','Novice-Ⅲ','Silver-Ⅰ','Silver-Ⅱ','Silver-Ⅲ','Gold-Ⅰ','Gold-Ⅱ','Gold-Ⅲ','Master-Ⅰ','Master-Ⅱ','Master-Ⅲ','Grand Master-Ⅰ','Grand Master-Ⅱ','Grand Master-Ⅲ','Annihilator']
yes_list = []
ang_list = []
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
    elif s == "BAN":
        x = 5
    elif s == "ALL":
        x = -1
    
    txt = f.readlines()
    f.close()
    data = []
    for y in txt:
        data.append(y[:-1])
    if((x >= 0) and (x <= 5)):
        if x == 3:
            a = data[3]
            return a.split(',')
        else:
            return data[x]
    else:
        return data


#ユーザidから職画像を生成して保存する関数,xが1の時はもってない職画像を生成する
def create_pic(userid,joblist):
    MCID = get_userdata(userid,'MCID')
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
    print(MCID + "の職画像を保存しました")
        
#ユーザidから解放済みの職をアルファベット3字で[,]を区切りとしてstringとして返す関数
#xが1の時は未解放の職を返す
def get_jobs(userid,x):
    joblist = get_userdata(userid,'job')
    count = 0
    s = ""
    for n in joblist:
        if x == 1:
            if n == '0':
                s += job_list[count] + ","
            count += 1
        else:
            if n == '1':
                s += job_list[count] + ","
            count += 1
    return s[:-1]

#ユーザidからユーザデータを取り出し、上書きする関数
#s:どのデータを書き換えるかを文字で,setdata:新しいデータ
def set_userdata(userid, s, setdata):
    data = get_userdata(userid, 'ALL')
    x = 0
    if s == "MCID":
        x = 1
    elif s == "rank":
        x = 2
    elif s == "job":
        x = 3
    elif s == "listNum":
        x = 4
    elif s == "BAN":
        x = 5
    data[x] = setdata
    a = '\n'.join(data) + "\n"
    f = open( 'saves\\' + userid + '.txt', 'w')
    f.write(a)
    f.close()

#全ユーザのMCIDを全ての情報と紐付けて取り出し、MCIDに一致した場合に全ての情報をリストで返す.不一致はFalse
def get_seluserdata(authorid,selMCID):
    f = open( 'hatchandata\\userid.txt', 'r')
    txt = f.readlines()
    f.close()
    ALLuserMCID = []
    ALLuserdata = []
    for x in txt:
        ALLuserMCID.append(get_userdata(x[:-1],'MCID'))
        y = get_userdata(x[:-1],'ALL')
        y.append(x[:-1])
        ALLuserdata.append(y)
    num = 0
    for x in ALLuserMCID:
        if x in selMCID:
            return ALLuserdata[num]
        num += 1
    y = get_userdata(authorid,'ALL')
    y.append(authorid)
    return y
        
    
#ユーザの発言内容にyes_listの内容が含まれているかどうかを判定する関数
def is_yes(content):
    global yes_list
    for y in yes_list:
        if (y in content):
            return True
    return False
    
@client.event
async def on_ready():
    global listnum
    global yes_list
    global ang_list
    
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    f = open( 'hatchandata\\listnum.txt', 'r')
    listnum = int(f.read())
    f.close()

    f = open( 'hatchandata\\yes_list.txt', 'r')
    txt = f.readlines()
    f.close()
    for y in txt:
        yes_list.append(y[:-1])

    f = open( 'hatchandata\\ang_list.txt', 'r')
    txt = f.readlines()
    f.close()
    for y in txt:
        ang_list.append(y[:-1])

@client.event
async def on_message(message):
    if ( "未来" in message.content.strip()):
        n = random.randint(1,5)
        if n == 1:
            m = ("<@!" + message.author.id + ">\n唐突の元カノ")
            await client.send_message(message.channel, m)
            m = ("<@!240287190750330890> \nあっ墓穴掘った")
            await client.send_message(message.channel, m)

            n = random.randint(1,5)
            if n == 1:
                m = ("<@!223771827657375754> \nところで彼女出来た?")
                await client.send_message(message.channel, m)

    if message.content.startswith('!'):
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
            nickname = get_userdata(message.author.id, 'NickName')
            MCID = get_userdata(message.author.id, 'MCID')
            Rank = get_userdata(message.author.id, 'rank')
            jobs = get_userdata(message.author.id, 'job')
        
        if message.content.startswith('!register'):
            if client.user != message.author:
                if Flag == 1:
                    m = "もう！" + nickname + "！これは初めての人だけのコマンドだよ！！"
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
                        if is_yes(message.content.strip()) == True:
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
                        if is_yes(message.content.strip()) == True:
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
                        if rank1.isdecimal() == False:
                            m = random.choice(ang_list)
                            await client.send_message(message.channel, m)
                            m = "Anniのランクを番号(半角数字)で教えて！"
                        elif((int(rank1) == 1)or(int(rank1) == 7)):
                            m = "おっけー！"
                            await client.send_message(message.channel, m)
                            if int(rank1) == 1:
                                n = 0
                            if int(rank1) == 7:
                                n = 16
                            data.append(str(n))
                            break
                        elif((int(rank1) >= 2)and(int(rank1) <= 6)):
                            while True:
                                m = "ランクの数字はいくつ?"
                                await client.send_message(message.channel, m)
                                message = await client.wait_for_message(author=message.author, check=check)
                                rank2 = message.content.strip()
                                if rank2.isdecimal() == False:
                                    m = random.choice(ang_list)
                                    await client.send_message(message.channel, m)
                                    m = "ランクの数字はいくつ?"
                                elif((int(rank2) >= 1)and(int(rank2) <= 3)):
                                    m = "おっけー！"
                                    await client.send_message(message.channel, m)
                                    n = (int(rank1) - 2) * 3
                                    n += int(rank2)
                                    data.append(str(n))
                                    break
                                else:
                                    m = random.choice(ang_list)
                                    await client.send_message(message.channel, m)
                                    m = "ランクの数字はいくつ?"
                            break
                        else:
                            m = random.choice(ang_list)
                            await client.send_message(message.channel, m)
                            m = "Anniのランクを番号(半角数字)で教えて！"
                    
                    jobs = ['0'] * 39
                    jobs[8] = '1'
                    if n >= 1:
                        jobs[21] = '1'
                    if n >= 2:
                        jobs[2] = '1'
                    if n >= 4:
                        jobs[37] = '1'
                    if n >= 5:
                        jobs[1] = '1'
                    if n >= 6:
                        jobs[15] = '1'
                    if n >= 7:
                        jobs[20] = '1'
                    if n >= 9:
                        jobs[14] = '1'
                    if n >= 10:
                        jobs[27] = '1'

                    job = ','.join(jobs)
                    data.append(job)
                    data.append(str(listnum))
                    data.append('0')
                    listnum += 1
                    f = open( 'hatchandata\\listnum.txt', 'w')
                    f.write(str(listnum))
                    f.close()

                    a = '\n'.join(data) + "\n"
                    f = open( 'saves\\' + message.author.id + '.txt', 'w')
                    f.write(a)
                    f.close()

                    f = open( 'hatchandata\\userid.txt', 'a')
                    f.write(message.author.id + "\n")
                    f.close()

                    m = "じゃあ最後に持ってる職を教えてもらおうかな。"
                    await client.send_message(message.channel, m)
                    count = 0
                    jobs_a = copy.deepcopy(jobs)
                    while True:
                        s = ""
                        num = 0
                        for n in jobs:
                            if n == '0':
                                s += job_list[num] + ","
                            num += 1
                        m = s[:-1] + "\nこの中から持ってる職を教えてね！"
                        await client.send_message(message.channel, m)
                        nojobs = s.split(',')
                        message = await client.wait_for_message(author=message.author, check=check)
                        num = 0
                        s = ","
                        for x in job_list:
                            if x in message.content.strip():
                                if (x in nojobs) == True:
                                    jobs[num] = '1'
                                    s += job_list[num] + ","
                            num += 1
                        m = "りょーかい！"
                        await client.send_message(message.channel, m)
                        create_pic(message.author.id, jobs)
                        m = "ということは持ってる職は\n"
                        m += get_jobs(message.author.id, 0)
                        m += s[:-1]
                        m += "\nこんな感じで、画像にするとこうなるのかな?"
                        if count == 1:
                            m += "\n良かったら[はい]って言ってほしいな"
                        await client.send_message(message.channel, m)
                        await client.send_file(message.channel,'img\\userimg\\' + message.author.id + '.png')
                        message = await client.wait_for_message(author=message.author, check=check)
                        if is_yes(message.content.strip()) == True:
                            setdata = ','.join(jobs)
                            set_userdata(message.author.id, 'job', setdata)
                            break
                        else:
                            m = "えっと、じゃあもっかい聞くよ。"
                            await client.send_message(message.channel, m)
                            count == 1
                            jobs = copy.deepcopy(jobs_a)
                    
                    m = "うん！" + data[0] + "のこと覚えたよ！！"
                    await client.send_message(message.channel, m)
                    m = "後は #rule で使い方を確認してね"
                    await client.send_message(message.channel, m)

        elif message.content.startswith('!job'):
            if client.user != message.author:
                if Flag == 0:
                    m = "初めまして！" + message.author.name + "さん！\n"
                    m += "まずは[!register]コマンドであなたのことを教えてね！"
                    await client.send_message(message.channel, m)
                else:
                    num = 0
                    nojobs = get_jobs(message.author.id,1)
                    m = "職の更新だね！" + nickname + "がまだ持ってなかった職は…\n"
                    m += nojobs
                    m += "  だから、\n"
                    count = 0
                    while True:
                        s = ","
                        m += "どれを新しく買ったの?"
                        await client.send_message(message.channel, m)
                        nojoblist = nojobs.split(',')
                        message = await client.wait_for_message(author=message.author, check=check)
                        num = 0
                        for x in job_list:
                            if x in message.content.strip():
                                if (x in nojoblist) == True:
                                    jobs[num] = '1'
                                    s += job_list[num] + ","
                            num += 1
                        m = "りょーかい！"
                        await client.send_message(message.channel, m)
                        create_pic(message.author.id, jobs)
                        m = "ということは持ってる職はこんな感じで、\n"
                        m += get_jobs(message.author.id, 0)
                        m += s[:-1]
                        m += "\n画像にするとこうなるのかな?"
                        if count == 1:
                            m += "\n良かったら[はい]って言ってほしいな"
                        await client.send_message(message.channel, m)
                        await client.send_file(message.channel,'img\\userimg\\' + message.author.id + '.png')
                        message = await client.wait_for_message(author=message.author, check=check)
                        if is_yes(message.content.strip()) == True:
                            m = "おっけー！覚え直しておくね。"
                            await client.send_message(message.channel, m)
                            setdata = ','.join(jobs)
                            set_userdata(message.author.id, 'job', setdata)
                            break
                        else:
                            m = "えっと、じゃあもっかい聞くよ。\n"
                            count = 1

        elif message.content.startswith('!remove'):
            if client.user != message.author:
                if Flag == 0:
                    m = "初めまして！" + message.author.name + "さん！\n"
                    m += "まずは[!register]コマンドであなたのことを教えてね！"
                    await client.send_message(message.channel, m)
                else:
                    count = 0
                    num = 0
                    s = ""
                    job = get_jobs(message.author.id,0)
                    joblist = job.split(',')
                    for x in job_list:
                        if x in message.content:
                            if (x in joblist) == True:
                                jobs[num] = '0'
                                s += job_list[num] + ","
                                count = 1
                        num += 1
                    if count == 0:
                        m = "よくわかんないけどこのままでよさそうだね！"
                        await client.send_message(message.channel, m)
                    else:
                        m = nickname + "は [" + s[:-1] + "] を持ってなかったんだね！\n覚え直しておくよ。"
                        await client.send_message(message.channel, m)
                        setdata = ','.join(jobs)
                        set_userdata(message.author.id, 'job', setdata)
                        create_pic(message.author.id, jobs)

        elif message.content.startswith('!nickname'):
            if client.user != message.author:
                if Flag == 0:
                    m = "初めまして！" + message.author.name + "さん！\n"
                    m += "まずは[!register]コマンドであなたのことを教えてね！"
                    await client.send_message(message.channel, m)
                else:
                    newnickname = message.content[10:]
                    m = "これからは" + nickname + "のことを" + newnickname + "って呼べばいいのかな?"
                    await client.send_message(message.channel, m)
                    message = await client.wait_for_message(author=message.author, check=check)
                    if is_yes(message.content.strip()) == True:
                        m = "おっけー！" + newnickname + "！これからもよろしく！！"
                        set_userdata(message.author.id, "NickName", newnickname)
                    else:
                        m = "うん！" + nickname + "！これからもよろしく！！"
                    await client.send_message(message.channel, m)
                    
        elif message.content.startswith('!MCID'):
            if client.user != message.author:
                if Flag == 0:
                    m = "初めまして！" + message.author.name + "さん！\n"
                    m += "まずは[!register]コマンドであなたのことを教えてね！"
                    await client.send_message(message.channel, m)
                else:
                    newMCID = message.content[6:]
                    m = "MCIDを[" + MCID + "]から[" + newMCID + "]に変えたの?"
                    await client.send_message(message.channel, m)
                    message = await client.wait_for_message(author=message.author, check=check)
                    if is_yes(message.content.strip()) == True:
                        m = "おっけー！[" + newMCID + "]で覚え直しておくね！！"
                        set_userdata(message.author.id, "MCID", newMCID)
                    else:
                        m = "うん！[" + MCID + "] のまま覚えておくよ！！"
                    await client.send_message(message.channel, m)

        elif message.content.startswith('!Rank'):
            if client.user != message.author:
                if Flag == 0:
                    m = "初めまして！" + message.author.name + "さん！\n"
                    m += "まずは[!register]コマンドであなたのことを教えてね！"
                    await client.send_message(message.channel, m)
                else:
                    if int(Rank) <= 15:
                        m = "Anniのランク上がったの?"
                        await client.send_message(message.channel, m)
                        message = await client.wait_for_message(author=message.author, check=check)
                        if is_yes(message.content.strip()) == True:
                            newRank = int(Rank)+1
                            m = "おめでと！\n" + rank_list[int(Rank)] + "から" + rank_list[newRank] + "になったんだね！"
                            set_userdata(message.author.id, "rank", str(newRank))
                            s = "none"
                            if newRank == 1:
                                jobs[21] = '1'
                                s = job_list[21]
                            elif newRank == 2:
                                jobs[2] = '1'
                                s = job_list[2]
                            elif newRank == 4:
                                jobs[37] = '1'
                                s = job_list[37]
                            elif newRank == 5:
                                jobs[1] = '1'
                                s = job_list[1]
                            elif newRank == 6:
                                jobs[15] = '1'
                                s = job_list[15]
                            elif newRank == 7:
                                jobs[20] = '1'
                                s = job_list[20]
                            elif newRank == 9:
                                jobs[14] = '1'
                                s = job_list[14]
                            elif newRank == 10:
                                jobs[27] = '1'
                                s = job_list[27]

                            if s != "none":
                                await client.send_message(message.channel, m)
                                m = "ということは、" + s + "を解放したんだね！職の画像も作り直しておくね"
                                setdata = ','.join(jobs)
                                set_userdata(message.author.id, "job", setdata)
                                create_pic(message.author.id, jobs)
                        else:
                            m = "ふーん..."
                        await client.send_message(message.channel, m)
                    else:
                        m = nickname + "はもうAnnihilatorだから上がらないでしょ！:angry:"
                        await client.send_message(message.channel, m)
                            
                        
        elif message.content.startswith('!show'):
            if client.user != message.author:
                if Flag == 0:
                    m = "初めまして！" + message.author.name + "さん！\n"
                    m += "まずは[!register]コマンドであなたのことを教えてね！"
                    await client.send_message(message.channel, m)
                else:
                    selMCID = message.content[6:]
                    seldata = get_seluserdata(message.author.id, selMCID)
                    m = "MCID:[" + seldata[1] + "]の情報をカイジするよ！\n\n"
                    m += "AnniRank:[" + rank_list[int(seldata[2])] + "]\n持ってる職は ["
                    jobs = seldata[3].split(',')
                    count = 0
                    for x in jobs:
                        if x == '1':
                            m += job_list[count] + ','
                        count += 1
                    m = m[:-1] + "]で画像にするとこうだよ！"
                    await client.send_message(message.channel, m)
                    await client.send_file(message.channel,'img\\userimg\\' + seldata[6] + '.png')

        elif message.content.startswith('!search'):
            if client.user != message.author:
                if Flag == 0:
                    m = "初めまして！" + message.author.name + "さん！\n"
                    m += "まずは[!register]コマンドであなたのことを教えてね！"
                    await client.send_message(message.channel, m)
                else:
                    f = open( 'hatchandata\\userid.txt', 'r')
                    txt = f.readlines()
                    f.close()
                    ALLuserMCID = []
                    ALLuserdata = []
                    Flag = 0
                    hasusers = []
                    seljob = ""
                    for x in txt:
                        ALLuserMCID.append(get_userdata(x[:-1],'MCID'))
                        ALLuserdata.append(get_userdata(x[:-1],'job'))
                    num = 0
                    for x in job_list:
                        if x not in message.content:
                            Flag += 1
                        else:
                            seljob += x + ','
                            count = 0
                            for n in ALLuserdata:                                
                                if n[num] == '0':
                                    ALLuserMCID[count] = "§exception"
                                count += 1
                        num += 1
                    if Flag <= 38:
                        m = seljob[:-1] + "を持ってる人は…\n"
                        for a in ALLuserMCID:
                            if a != "§exception":
                                hasusers.append(a)
                        hasusers.sort()
                        if hasusers == "":
                            m += "いないみたいだね…"
                        else:
                            m += "```\n" + '\n'.join(hasusers) + "```\nだよ！"
                    else:
                        m = "それは存在しない職だよ"

                    await client.send_message(message.channel, m)
                    
                    
        elif message.content.startswith('!教育'):
            if ("エンジニア" in [y.name.lower() for y in message.author.roles])or("幹部" in [y.name.lower() for y in message.author.roles]):
                if(message.channel.id == '442950419434700810'):
                    m = "yes_listの中身を変更します。操作中別のチャットを行わないでください。"
                    await client.send_message(message.channel, m)
                    
                    m = ""
                    
                    global yes_list
                    for n in yes_list:
                        m += n + "\n"
                        
                    msg = discord.Embed(title='現在のlistの中身', description= m, colour=0x3498db)
                    await client.send_message(message.channel, embed=msg)
                    
                    m = "追加 => 1\n削除 => 2"
                    await client.send_message(message.channel, m)
                    message = await client.wait_for_message(author=message.author, check=check)
                    if message.content.strip() == '1':
                        m = "yes_listに追加する単語を入力してください"
                        await client.send_message(message.channel, m)
                        message = await client.wait_for_message(author=message.author, check=check)
                        #既にあるものだったら除外
                        if is_yes(message.content.strip()) == True:
                            m = "その単語は既にyes_listに登録されています。"
                            await client.send_message(message.channel, m)
                        else:
                            f = open( 'hatchandata\\yes_list.txt', 'a')
                            f.write(message.content.strip()+ "\n")
                            f.close()
                            m = "単語:" + message.content.strip() + " をyes_listに追加しました"
                            await client.send_message(message.channel, m)
                            yes_list.append(message.content.strip())

                    elif message.content.strip() == '2':
                        m = "yes_listから削除する単語を入力してください"
                        await client.send_message(message.channel, m)
                        message = await client.wait_for_message(author=message.author, check=check)
                        #無いものだったら除外
                        if is_yes(message.content.strip()) == False:
                            m = "その単語はyes_listに登録されていません。"
                            await client.send_message(message.channel, m)
                        else:
                            f = open( 'hatchandata\\yes_list.txt', 'w+')
                            txt = f.readlines()
                            n = []
                            for s in txt:
                                if (s[:-1] != message.content.strip()):
                                    n.append(s)
                            f.writelines(n)
                            yes_list = []
                            for y in n:
                                yes_list.append(y[:-1])
                            m = "単語:" + message.content.strip() + " をyes_listから削除しました"
                            await client.send_message(message.channel, m)
                    else:
                        m = "入力が不正です。終了します。"
                        await client.send_message(message.channel, m)
                else:
                    m = "そのコマンドはこのチャンネルじゃ使えないよ！"
                    await client.send_message(message.channel, m)
            else:
                m = "このコマンドを使う権限がないみたいだよ"
                await client.send_message(message.channel, m)

        elif message.content.startswith('!map'):
            if client.user != message.author:
                map = message.content[5:]
                await client.send_file(message.channel,'img\\maps\\' + map + '.png')

@client.event
async def on_member_join(member):
    server = member.server
    channel = [channel for channel in client.get_all_channels()
    if channel.id == '419780533011087371'][0]
    m = "#LBGへようこそ! " + member.mention + " 設定をするから[!register]って打ってね！"
    await client.send_message(channel, m)

client.run("NDQyNjM0NjMyNzQ0MjcxODcy.DdCs2A.2mzJJI3CApn-btM6Xbz5spAycMo")
