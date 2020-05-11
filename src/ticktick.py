import json
import csv

from csv import Error
from datetime import datetime as dt
import requests
#from src.cypter import deCode, enCode

class TickTick:
    """
    A TickTick.com instance.
    """
    path_of_logindata = '../loginData.csv'
    domain = "https://ticktick.com/"
    api = "api/v2/batch/check/9999"
    user_auth = "api/v2/user/signon?wc=true&remember=true"
    session = requests.Session()
    default_date = '2999-01-01'
    username = None 
    password = None
    def __init__(self, username, password, dida=False):
        if dida:
            self.domain = "https://dida365.com/"
        self.username = username
        self.password = password
        self.login()

    def login(self):
        #auth = "https://ticktick.com/api/v2/user/signon?wc=true&remember=true"
        auth = self.domain+self.user_auth
        response = self.session.post(auth, json={
             'username': self.username,
             'password': self.password,
         })
        if response.status_code != 200:
            print('Login failed!')

    def get_tasks(self, sdate1,sdate2=None):
        self.login()
        raw=self.session.get(self.domain+self.api).text
        tree=json.loads(raw)
        project_Dict={}
        rawPjid=tree['projectProfiles']
        for prj in rawPjid:

            project_Dict[prj['id']] = prj['name']
        tasklist = tree['syncTaskBean']['update']

        completed, undone = self.get_list(project_Dict, tasklist, sdate1, sdate2)

        return completed,undone


    def get_list(self, project_Dict, tasklist, sdate1, sdate2=None):
        """
        Get list fo completed tasks and undone tasks
        """
        completed = []
        undone = []
        for item in tasklist:
            try:
                completedTime = dt.strptime(item['completedTime'][:10], '%Y-%m-%d').date()
            except:
                completedTime = dt.strptime(self.default_date, '%Y-%m-%d').date()

            try:
                dueTime = dt.strptime(item['dueDate'][:10], '%Y-%m-%d').date()

            except:
                dueTime = dt.strptime(self.default_date, '%Y-%m-%d').date()

            try:
                title = item['title']
            except:
                continue
            try:
                id = item["projectId"]
                if 'inbox' in id:
                    project = 'Inbox'
                else:
                    project = project_Dict[id]
            except:
                project='Null'
            
            if self.evaluate(completedTime,sdate1,searchDate2=sdate2):
                completed.append([title, item['completedTime'][:10], project])
            elif self.evaluate(dueTime, sdate1, searchDate2=sdate2,cT=completedTime):
                try:
                    if item['progress'] !='0':
                        title+='(%s'%item['progress']+'%)'
                except:
                    pass
                undone.append([title, project])

        return completed, undone

    def evaluate(self, date, searchDate1, searchDate2=None, cT=None):
        #searchDate1 = dt.strptime(sdate1, '%Y-%m-%d').date()
        if searchDate2:
            #searchDate2 = dt.strptime(sdate2, '%Y-%m-%d').date()
            if cT:
                return (searchDate1<= date <= searchDate2) and not (searchDate1<= cT <= searchDate2)
            return searchDate1<= date <= searchDate2
        elif cT:
            return (date <= searchDate1) and (cT == dt.strptime(self.default_date, '%Y-%m-%d').date())
        else:
            return date == searchDate1
