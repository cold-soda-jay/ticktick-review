import onedrivesdk
import time

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import util as ut

path = ut.path_of_logindata


def init_onedrive():
    redirect_uri = "https://login.live.com/oauth20_desktop.srf"
    client_id,client_secret = ut.getUserData(path,'APIsecret')

    client = onedrivesdk.get_default_client(client_id=client_id,
                                            scopes=['wl.signin',
                                                    'wl.offline_access',
                                                    'onedrive.readwrite'])
    auth_url = client.auth_provider.get_auth_url(redirect_uri)

    user_name,password = ut.getUserData(path,'onedrive')
    code = get_token(user_name, password, auth_url)

    client.auth_provider.authenticate(code, redirect_uri, client_secret)
    return client



def get_token(user_name,password,auth_url):
    options = Options()
    options.add_argument('headless')

    driver = webdriver.Chrome(chrome_options=options)
    # driver.set_window_size(2, 2)

    driver.get(auth_url)
    driver.implicitly_wait(5)
    driver.get(auth_url)

    login_field = driver.find_element_by_name("loginfmt")
    login_field.send_keys(user_name)

    next_btn = driver.find_element(By.ID, "idSIButton9")
    next_btn.click()
    time.sleep(1)

    psw_field = driver.find_element_by_name("passwd")
    psw_field.send_keys(password)

    signin_btn = driver.find_element(By.ID, "idSIButton9")
    signin_btn.click()
    time.sleep(1)

    print(driver.current_url)

    # parse URL to get code and close the browser
    tokens = driver.current_url.split('=')
    driver.quit()
    access_code = tokens[1].split('&')[0]
    return access_code


# def upload(client,filepath,onedrivepath=None):
#     client.item(drive='me', id='root').children[filepath].upload('D:\Workspace_Pycharm\WiwiSeminar\src\ChatBot/userCache.csv')




# client =init_onedrive()
# returned_item = client.item(drive='me', id='ED1A0D88BB2A445F%214750').children['newtry.png'].upload('./authrization.png')
#upload(client,'D:\Workspace_Pycharm\WiwiSeminar\src\ChatBot/userCache.csv')