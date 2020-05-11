#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import csv
import datetime
import os
import socket
import sys
import time

import requests
import telebot as tb
import urllib3
import getpass

#from src import util as ut
import onedrive
import util as ut
from template import head, td_html, wk_html
from ticktick import TickTick


path_of_log='../'
path_of_login_data = ut.path_of_logindata
token = ''
logger = None
onedrive_client = None
bot = tb.TeleBot('')
cachePath='cache.csv'
command_list = ['today', 'yesterday','thiswk','lastwk','start','library','film','day','week']
fieldnames = ut.fieldnames
head_ch = head.replace('<br>', '')
      
sttarttime=time.time()
logger = ut.initlog()
logger.info('--> Initiating OneDrive Client')
us,token=ut.getUserData(path_of_login_data,'teleToken')
onedrive_client = onedrive.init_onedrive()

bot = tb.TeleBot(token)
username, password=ut.getUserData(path_of_login_data,'tick')
tick_client=TickTick(username=username,password=password)
logger.info('--> Bot started!')


@bot.message_handler(commands=['start', 'help'])
def sartInfo(message):
    userid = str(message.from_user.id)
    if userid != '781549524':
        bot.send_message('781549524','Unknow contact from: @%s\nContent:%s'%(message.from_user.username,message.text))
        return
    for cmd in command_list:
        bot.send_message(userid,'/%s'%cmd)
    init_cache(userid)
    return

@bot.message_handler(commands=['library'])
def lib(message):
    userid = str(message.from_user.id)
    if userid != '781549524':
        bot.send_message('781549524','Unknow contact from: @%s\nContent:%s'%(message.from_user.username,message.text))
        return
    info=ut.get_seat_info()
    bot.send_message(userid,'%s'%info)
    return

@bot.message_handler(commands=['film'])
def film(message):
    userid = str(message.from_user.id)
    if userid != '781549524':
        bot.send_message('781549524','Unknow contact from: @%s\nContent:%s'%(message.from_user.username,message.text))
        return
    os.system('python3 /home/pi/FilmScrap/src/thefilmwacher.py')
    bot.send_message(userid,'Sending EMail...')
    return

@bot.message_handler(commands=['day'])
def dayy(message):
    userid = str(message.from_user.id)
    if userid != '781549524':
        bot.send_message('781549524','Unknow contact from: @%s\nContent:%s'%(message.from_user.username,message.text))
        return
    try:
        td = ut.get_modified_sum(tick=tick_client, datekey=message.text[5:])
        ut.write_user_cache(userid, 'summary', td)
        bot.send_message(message.chat.id,'Daily Review:\n%s'%td,parse_mode="HTML")
        bot.send_message(message.chat.id, 'Please rate today with number of ⭐(1,2,3...)!')
        ut.write_user_cache(userid,'status','starsTD')
        ut.write_user_cache(userid,'time',datetime.date.today())
    except:
        bot.send_message(message.chat.id, 'Wrong format！eg: /day 2020-4-1')
    return

@bot.message_handler(commands=['week'])
def weeek(message):
    userid = str(message.from_user.id)
    if userid != '781549524':
        bot.send_message('781549524',
                        'Unknow contact from: @%s\nContent:%s' % (message.from_user.username, message.text))
        return
    try:
        td = ut.get_modified_sum(tick_client,message.text[6:],week=True)
        ut.write_user_cache(userid, 'summary', td)
        bot.send_message(message.chat.id, 'Weekliy Review:\n%s' % td, parse_mode="HTML")
        bot.send_message(message.chat.id, 'Please rate this week with number of ⭐(1,2,3...)!')
        i = td.index('Done')
        wk = td[:i - 5]
        ut.write_user_cache(userid, 'time', wk)
        ut.write_user_cache(userid, 'status', 'starsWK')
    except:
        bot.send_message(message.chat.id, 'Wrong format！eg: /week 2020-4-1')
    return

@bot.message_handler(commands=['today'])
def today(message):
    userid = str(message.from_user.id)
    if userid != '781549524':
        bot.send_message('781549524','Unknow contact from: @%s\nContent:%s'%(message.from_user.username,message.text))
        return
    td = ut.get_Summary(tick_client,'today')
    ut.write_user_cache(userid, 'summary', td)
    bot.send_message(message.chat.id,'Daily review:\n%s'%td,parse_mode="HTML")
    bot.send_message(message.chat.id, 'Please rate today with number of ⭐(1,2,3...)!!')
    ut.write_user_cache(userid,'status','starsTD')
    ut.write_user_cache(userid,'time',datetime.date.today())
    return

@bot.message_handler(commands=['thisWK','thiswk'])
def thisWK(message):
    userid = str(message.from_user.id)
    if userid != '781549524':
        bot.send_message('781549524','Unknow contact from: @%s\nContent:%s'%(message.from_user.username,message.text))
        return
    td = ut.get_Summary(tick_client,'thiswk')
    ut.write_user_cache(userid, 'summary', td)
    bot.send_message(message.chat.id,'Weekly review:\n%s'%td,parse_mode="HTML")
    bot.send_message(message.chat.id, 'Please rate this week with number of ⭐(1,2,3...)!')
    i=td.index('Done')
    wk = td[:i - 5]
    ut.write_user_cache(userid, 'time', wk)
    ut.write_user_cache(userid,'status','starsWK')
    return

@bot.message_handler(commands=['lastWK','lastwk'])
def lastWK(message):
    userid = str(message.from_user.id)
    if userid != '781549524':
        bot.send_message('781549524','Unknow contact from: @%s\nContent:%s'%(message.from_user.username,message.text))
        return
    td = ut.get_Summary(tick_client,'lastwk')
    ut.write_user_cache(userid, 'summary', td)
    bot.send_message(message.chat.id, 'Weekly review:\n%s' %td,parse_mode="HTML")
    bot.send_message(message.chat.id, 'Please rate last week with number of ⭐(1,2,3...)!')
    i=td.index('Done')
    wk = td[:i - 5]
    ut.write_user_cache(userid, 'time', wk)
    ut.write_user_cache(userid, 'status', 'starsWK')
    return

@bot.message_handler(commands=['yesterday','yd'])
def yesterdAY(message):
    userid = str(message.from_user.id)
    if userid != '781549524':
        bot.send_message('781549524','Unknow contact from: @%s\nContent:%s'%(message.from_user.username,message.text))
        return
    td = ut.get_Summary(tick_client,'yesterday')
    ut.write_user_cache(userid, 'summary', td)
    bot.send_message(message.chat.id, 'Daily review:\n%s' % td,parse_mode="HTML")
    bot.send_message(message.chat.id, 'Please rate today with number of ⭐(1,2,3...)!')
    ut.write_user_cache(userid, 'status', 'starsTD')
    ut.write_user_cache(userid, 'time', ut.get_yesterday())
    
    return

def get_input(messages):
    for message in messages:

        userid=str(message.from_user.id)
        if userid != '781549524':
            bot.send_message('781549524',
                            'Unknow contact from: @%s\nContent:%s' % (message.from_user.username, message.text))
            return
        with open(cachePath, "rt", encoding='utf-8') as log:
            reader = csv.DictReader(log)
            userList = [row['userID'] for row in reader]
        if userid not in userList:
            init_cache(userid)
        logger.info(u'%s'%str(message.text))
        if message.from_user.first_name.lower() != 'joe':
            return
        for cmd in command_list:
            if '/%s'%cmd in message.text:
                return
        if ut.get_user_cache(userid,'status')=='starsTD':
            ut.write_user_cache(userid,'star',ut.convert_star(message.text))
            ut.write_user_cache(userid, 'status', 'commentTD')
            bot.send_message(message.chat.id, 'Comment and Summary:')
            return
        if ut.get_user_cache(userid,'status')=='commentTD':
            ut.write_user_cache(userid, 'comment', message.text)
            tody = ut.get_user_cache(userid, 'summary')
            stars = ut.get_user_cache(userid, 'star')
            sumi = 'Summary of today:\n\n%s\n---------\nStars:\n%s\n\n---------\n\nComment:\n\n%s' % (tody, stars, message.text)
            bot.send_message(userid,sumi,parse_mode="HTML")
            ut.write_user_cache(userid, 'status', 'svTD')
            bot.send_message(message.chat.id, 'Do you want to save it??')
            return
        if ut.get_user_cache(userid,'status')=='svTD' and ('yes' in message.text.lower() or 'sure' in message.text.lower() or 'ok' in message.text.lower()):
            td = ut.get_user_cache(userid, 'summary')
            if 'Done' in td:
                i=td.index('Done')
            else:
                i=td.index('Undoen')
            wk = td[:i - 2]
            month_num = datetime.datetime.today().month
            time = ut.get_user_cache(userid, 'time')
            tody = ut.get_user_cache(userid, 'summary')
            stars = ut.get_user_cache(userid, 'star')
            comm=ut.get_user_cache(userid, 'comment')
            content = '%s\n---------\n<b>Stars</b>:\n%s\n\n---------\n\n<b>Comment and Summary</b>:\n\n%s'%(tody,stars,comm)
            content_td=content.replace('\n','<br>')
            susu = td_html.format(content_td=content_td)
            sumi = head_ch + susu
            ut.saveFile('Month-%s' % month_num, 'Daily Review(%s)'%time,sumi,onedrive_client)
            bot.send_message(userid,'Succeed!')
            ut.write_user_cache(userid, 'status', '0')
            bot.send_message(message.chat.id, 'It is done.')
            return
        if ut.get_user_cache(userid,'status')=='starsWK':
            ut.write_user_cache(userid,'star',ut.convert_star(message.text))
            ut.write_user_cache(userid, 'status', 'commentWK')
            bot.send_message(message.chat.id, 'Comment and Summary!')
            return
        if ut.get_user_cache(userid,'status')=='commentWK':
            ut.write_user_cache(userid, 'comment', message.text)
            tody = ut.get_user_cache(userid, 'summary')
            stars = ut.get_user_cache(userid, 'star')
            sumi = 'Summary of week:\n\n%s\n---------\nStars:\n%s\n\n---------\n\nComment:\n\n%s' % (tody, stars, message.text)
            bot.send_message(userid,sumi,parse_mode="HTML")
            ut.write_user_cache(userid, 'status', 'svWK')
            bot.send_message(message.chat.id, 'Do you want to save it?')
            return
        if ut.get_user_cache(userid,'status')=='svWK' and ('yes' in message.text.lower() or 'sure' in message.text.lower() or 'ok' in message.text.lower()):
            wkk = ut.get_user_cache(userid, 'summary')
            wk = ut.get_user_cache(userid, 'time')
            month_num = datetime.datetime.today().month
            stars = ut.get_user_cache(userid, 'star')
            comm = ut.get_user_cache(userid, 'comment')
            content = '%s\n---------\n<b>Stars</b>:\n%s\n\n---------\n\n<b>Comment</b>:\n\n%s'%(wkk,stars,comm)
            content_td = content.replace('\n', '<br>')
            susu = wk_html.format(week=wk,content_wk=content_td)
            sumi = head_ch + susu
            ut.saveFile('Month-%s' % month_num, 'Weekly Review(%s)'%wk, sumi, onedrive_client)
            bot.send_message(userid,'Succeed!')
            ut.write_user_cache(userid, 'status', '0')
            bot.send_message(message.chat.id, 'It is done.')
            return

def init_cache(userid):
    with open(cachePath, "a+", encoding='utf-8') as log:
        writer = csv.writer(log)
        writer.writerow([userid, '0','','','',''])

def start_bot(args):
    with open(cachePath, 'w', newline='',encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(fieldnames)
    ti = datetime.datetime.now()
    print("Bot started: " + str(ti))
    print(str(time.time()-sttarttime))
    bot.set_update_listener(get_input)
    try:
        bot.polling(none_stop=True, interval=0, timeout=3)
    except (OSError, TimeoutError, ConnectionResetError, requests.exceptions.ReadTimeout, urllib3.exceptions.ReadTimeoutError,
            socket.timeout, RecursionError, urllib3.exceptions.ProtocolError,requests.exceptions.ConnectionError) as e:
        logger.error('---> %s' % str(e))
        time.sleep(0.5)


def init_userdata(args):
    tk_username=input('Username of TickTick: ')
    tk_pass=getpass.getpass("Password of TickTick: ")
    od_username=input("client id of Onedrive: ")
    od_pass= input("client secret of Onedrive: ")
    tele_token=getpass.getpass("Token of Telegram: ")
    ut.newUserData(ut.path_of_logindata, username=tk_username,password=tk_pass,key='tick')
    ut.newUserData(ut.path_of_logindata,username=od_username,password=od_pass,key='APIsecret')
    ut.newUserData(ut.path_of_logindata,username='teleToken', password=tele_token,key='teleToken')
    print('User configuration saved!')


def main():
    parser = argparse.ArgumentParser()

    sub_parser = parser.add_subparsers(title='\n-----------------------------------------\nTicktick-Review',
                                       description='\n',
                                       help='With [command] -h you can see usage of all functions.')
    init_parser = sub_parser.add_parser('init',help='Init user config with name and target folder. See init -h')
    init_parser.add_argument('-tick', required=False, help='')
    init_parser.add_argument('-onedrive', required=False, help='')
    init_parser.set_defaults(func=init_userdata)

    start_parser = sub_parser.add_parser('start', help='Start Bot')

    start_parser.set_defaults(func=start_bot)
    args = parser.parse_args()
    if len(args._get_kwargs())==0:
        #print(welcome)
        parser.print_help()
        parser.exit(1)
    else:
        args.func(args)


main()
