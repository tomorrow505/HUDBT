# -*- coding: utf-8 -*-

from time import sleep
from selenium import webdriver
import json

options = webdriver.ChromeOptions()

options.add_argument(
    '--user-data-dir=C:/Users/CL/AppData/Local/Google/Chrome/User Data')

driver = webdriver.Chrome(
    executable_path='*\\chromedriver.exe', # 指向你自己下载的chromedriver的目录
    options=options)


def load_pt_sites():

    pt_sites = {}

    try:
        with open('pt_sites.json', 'r') as pt_file:
            pt_sites = json.load(pt_file)
    except BaseException:
        print("Json load failed")
    finally:
        return pt_sites


# initial

hudbt = {
    'abbr': 'hudbt',
    'domain': 'https://hudbt.hust.edu.cn',
    'index': 'https://hudbt.hust.edu.cn/index.php',
    'cookie': []
}
npupt = {
    'abbr': 'npupt',
    'domain': 'https://npupt.com',
    'index': 'https://npupt.com/index.php',
    'cookie': []
}
stju = {
    'abbr': 'stju',
    'domain': 'https://pt.sjtu.edu.cn',
    'index': 'https://pt.sjtu.edu.cn/index.php',
    'cookie': []
}
tjupt = {
    'abbr': 'tjupt',
    'domain': 'https://www.tjupt.org',
    'index': 'https://www.tjupt.org/index.php',
    'cookie': []
}
byr = {
    'abbr': 'byr',
    'domain': 'https://bt.byr.cn',
    'index': 'https://bt.byr.cn/index.php',
    'cookie': []
}
nwsuaf6 = {
    'abbr': 'nwsuaf6',
    'domain': 'https://pt.nwsuaf6.edu.cn',
    'index': 'https://pt.nwsuaf6.edu.cn/index.php',
    'cookie': []
}

pt_sites = {}

pt_sites['byr'] = byr
pt_sites['hudbt'] = hudbt
pt_sites['npupt'] = npupt
pt_sites['stju'] = stju
pt_sites['tjupt'] = tjupt
pt_sites['nwsuaf6'] = nwsuaf6


def get_cookie(url):
    driver.get(url)
    cookies_0 = driver.get_cookies()

    cookies_1 = {}
    for item in cookies_0:
        cookies_1[item['name']] = item['value']
    return cookies_1


def save_site_info(pt_sites):
    cookies_file = 'pt_sites.json'
    with open(cookies_file, 'w') as f:
        json.dump(pt_sites, f)


if __name__ == "__main__":

    for site in pt_sites:
        url = pt_sites[site]['index']
        pt_sites[site]['cookie'] = get_cookie(url)
        sleep(5)

    driver.quit()

    save_site_info(pt_sites)
