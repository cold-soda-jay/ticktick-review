import csv
import datetime as dt
import logging
import os
import onedrivesdk
import sys
import requests
import re

from csv import Error
from cypter import deCode,enCode
from ticktick import TickTick



fieldnames = ['userID','status','summary','time','star','comment']
logPath='cache.csv'
path_of_logindata = './data.csv'

def init_keydict():
    today=dt.date.today()
    start = today - dt.timedelta(days=today.weekday())
    end = start + dt.timedelta(days=6)
    thiswk=[start,end]
    lstart=start - dt.timedelta(days=7)
    lend=lstart + dt.timedelta(days=6)
    lastwk=[lstart,lend]
    keyDict = {}
    keyDict['today']=today
    keyDict['yesterday']=today-dt.timedelta(days=1)
    keyDict['thiswk']=thiswk
    keyDict['lastwk']=lastwk
    return keyDict


def get_Summary(tick,key):
    keydict=init_keydict()
    day=keydict[key]
    COMPLETED = ''
    UNDONE = '\n<b>Undone</b>:\n'
    #tick = TickTick()
    if day.__class__ is dt.date:
        completed, undone = tick.get_tasks(day)
        HEAD=day
    else:
        completed, undone = tick.get_tasks(day[0],day[1])
        HEAD='%s~%s'%(dt.date.strftime(day[0],"%Y-%m-%d"),dt.date.strftime(day[1],"%Y-%m-%d"))
    for cp in completed:
        COMPLETED += '- %s [%s]\n' % (cp[0], cp[2])
    if len(undone)==0:
        UNDONE=''
    else:
        for ud in undone:
            UNDONE += '- %s [%s]\n' % (ud[0], ud[1])
    output = "%s\n\n<b>Done</b>:\n%s\n%s" % (HEAD, COMPLETED,UNDONE)
    return output


def get_modified_sum(tick,datekey,week=False):
    day=dt.datetime.strptime(datekey,'%Y-%m-%d').date()
    #tick = TickTick()
    COMPLETED = ''
    UNDONE = '\n<b>Undone</b>:\n'
    if week:
        start = day - dt.timedelta(days=day.weekday())
        end = start + dt.timedelta(days=6)
        thiswk = [start, end]
        completed, undone = tick.get_tasks(thiswk[0], thiswk[1])
        HEAD = '%s~%s' % (dt.date.strftime(thiswk[0], "%Y-%m-%d"), dt.date.strftime(thiswk[1], "%Y-%m-%d"))
    else:
        completed, undone = tick.get_tasks(day)
        HEAD = str(day)

    for cp in completed:
        COMPLETED += '- %s [%s]\n' % (cp[0], cp[2])
    if len(undone)==0:
        UNDONE=''
    else:
        for ud in undone:
            UNDONE += '- %s [%s]\n' % (ud[0], ud[1])
    output = "%s\n\n<b>Done</b>:\n%s\n%s" % (HEAD, COMPLETED,UNDONE)
    return output


def initlog():
    today = dt.date.today()
    logadress='../logs/%s/'%today
    try:
        os.mkdir(logadress)
    except (FileExistsError,FileNotFoundError) as e:
        print(e)
    # create logger with 'spam_application'
    logger = logging.getLogger('RecoBot')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('%sRecoBotlog.log'%(logadress))
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def getUserData(fpath,key):
    with open(fpath, 'rt', encoding='utf-8') as myFile:
        reader = csv.DictReader(myFile)
        try:
            for row in reader:
                if row['key'] == key:
                    return deCode(row['username']), deCode(row['password'])
        except Error as e:
            print(e)


def get_user_cache(userid, key):
    global logPath
    with open(logPath, "rt", encoding='utf-8') as log:
        reader = csv.DictReader(log)
        for row in reader:
            if row['userID'] == userid:
                return row[key]


def write_user_cache(userid, key, value):
    global logPath,fieldnames
    csvdict = csv.DictReader(open(logPath, 'rt', encoding='utf-8', newline=''))
    dictrow = []
    for row in csvdict:
        if row['userID'] == userid:
            row[key] = value
        # rowcache.update(row)
        dictrow.append(row)

    with open(logPath, "w+", encoding='utf-8', newline='') as lloo:
        # lloo.write(new_a_buf.getvalue())
        wrier = csv.DictWriter(lloo, fieldnames)
        wrier.writeheader()
        for wowow in dictrow:
            wrier.writerow(wowow)


def saveFile(foldername, fileName, tt, client):
    filp='%s.html'%fileName
    with open(filp, 'w', encoding='utf-8') as file:
        file.write(tt)

    summary_id='ED1A0D88BB2A445F%218025'
    fold_id=get_folder_id(client, foldername, summary_id)
    if fold_id is None:
        f = onedrivesdk.Folder()
        i = onedrivesdk.Item()
        i.name = foldername
        i.folder = f
        client.item(drive='me', id=summary_id).children.add(i)
        fold_id = get_folder_id(client, foldername, summary_id)

    client.item(drive='me', id=fold_id).children[filp].upload(filp)
    os.remove(filp)


def get_folder_id(client, foldername, summary_id):
    root_folder = client.item(drive='me', id=summary_id).children.get()
    for fold in root_folder:
        if fold.name == foldername:
            return fold.id
    return None


def convert_star(text):
    try:
        number=int(text)       
        stars = number * '⭐'        
        return stars
    except ValueError as e:
        print(e)


def newUserData(fpath, username=None, password=None,key=None):
    if username==None and password==None:
        key = input('Key name:\n')
        username = input('Username:\n')
        password = input('Pass word:\n')
    cusername = enCode(username)
    cpassword = enCode(password)
    with open(fpath, "a+") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([key,cusername,cpassword])


def get_yesterday():
    today = dt.date.today()
    oneday = dt.timedelta(days=1)
    yesterday = today - oneday
    return yesterday


def get_seat_info():
    html=requests.get('https://seatfinder.bibliothek.kit.edu/karlsruhe/getdata.'
                'php?callback=jQuery21407451994564516051_1559296485007&location%5B0%5D=LSG%2CLSM%2CLST%'
                '2CLSN%2CLSW%2CLBS%2CBIB-N%2CFBC%2CFBP%2CLAF%2CFBA%2CFBI%2CFBM%2CFBW%2CFBH%2CFBD%2CTheaBib%2CBLB%2CWIS&values'
                '%5B0%5D=seatestimate%2Cmanualcount&after%5B0%5D=-10800seconds&before%5B0%5D=now&limit%5B0%5D=-17&location%5'
                'B1%5D=LSG%2CLSM%2CLST%2CLSN%2CLSW%2CLBS%2CBIB-N%2CFBC%2CFBP%2CLAF%2CFBA%2CFBI%2CFBM%2CFBW%2CFBH%2CFBD%2CTheaBib%2CBLB%2C'
                'WIS&values%5B1%5D=location&after%5B1%5D=&before%5B1%5D=now&limit%5B1%5D=1&refresh=&_=1559296485011')

    stage_tag={'LSG':'3rd floor new','LSM':'3rd floor old','LST':'2nd floor new','LSN':'2nd floor old','LSW':'1st floor new','LBS':'1st floor old'}
    infodict={}
    total=0
    tfree=0

    for stage in stage_tag:
        pattern = r'name":"%s","occ.*?{"timestamp":'%stage
        seatinfo=re.findall(pattern,html.text)
        if len(seatinfo) >0:
            occupied=re.findall(r'"occupied_seats".*?,',seatinfo[0])[0]
            onumber=re.findall(r'[0-9]{1,2}',occupied)[0]
            total+=int(onumber)
            free=re.findall(r'"free_seats".*?}',seatinfo[0])[0]
            fnumber=re.findall(r'[0-9]{1,2}',free)[0]
            total+=int(fnumber)
            tfree+=int(fnumber)
            percent=int(int(fnumber)*100/(int(fnumber)+int(onumber)))
            infodict[stage_tag[stage]]=str(percent)+'%'
        else:
            infodict[stage_tag[stage]]='No info'


    result='Available seats in library:\n'
    for text in infodict:
        result+='%s: %s.\n'%(text,infodict[text])
    result+='Total available seats: %s'%(str(int(tfree*100/(total+0.1)))+'%')
    return result

