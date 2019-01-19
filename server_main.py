# -*- coding: utf-8 -*-
# Author:Chengli


import threading
import requests
import json
import config
from time import sleep
import parser_torrent
from parser_origin import byr, tjupt, npupt
import shutil
import re
import sys
from urllib.parse import unquote
import os


class Task (threading.Thread):
    def __init__(self, origin_url):
        super(Task, self).__init__()
        self.origin_url = origin_url

    def run(self):
        main(self.origin_url)


def load_pt_sites():
    pt_sites = {}
    try:
        with open('pt_sites.json', 'r') as pt_file:
            pt_sites = json.load(pt_file)
    except Exception as exc:
        print("Pt_sites.Json load failed: %s" % exc)
        sys.exit(0)
    finally:
        return pt_sites


def find_origin_site(url):
    match_site = ''
    pt_sites = load_pt_sites()
    for site in pt_sites:
        domain = pt_sites[site]['domain']
        if ''.join(url.split(' ')).find(domain) >= 0:
            print("该种子来自于%s!" % pt_sites[site]['abbr'])
            match_site = site
            break
    if match_site == '':
        print('不支持的网站')
        sys.exit(0)
    return pt_sites[match_site]


def get_id(url):
    id_ = re.search('id=(\d{6})', url)
    my_id = id_.group(1)
    if not my_id:
        my_id = 0
        print('获取种子id失败！')
    return my_id


def get_response(url, cookie):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    session = requests.session()

    session.headers = headers

    response = session.get(url, cookies=cookie)

    return response


def get_html(url, cookie):
    try:
        response = get_response(url, cookie)
        html = response.text
        print('获取原始网页解析！')
    except Exception as exc:
        print('原始网页获取失败: %s' % exc)
        sys.exit(0)
    return html


def parser_choose(abbr, html, torrent_path):

    if abbr == 'byr':
        raw_info = byr.parser_html(html, torrent_path)
    elif abbr == 'tjupt':
        raw_info = tjupt.parser_html(html, torrent_path)
    elif abbr == 'npupt':
        raw_info = npupt.parser_html(html, torrent_path)

    return raw_info


def download_torrent(host, tid, cookie):

    download_url = "{host}/download.php?id={tid}".format(host=host, tid=tid)
    response = get_response(download_url, cookie)

    content = response.headers['Content-Disposition'].replace('"', '')
    if host == 'https://npupt.com':
        content = (unquote(content, 'utf-8'))
        # print(content)
    try:
        origin_filename = re.search('filename=(.*?).torrent', content).group(1)
        # print(origin_filename)
    except Exception as exc:
        print('获取下载种子的文件名失败: %s' % exc)
        exit(0)
    file_path = config.save_path + '\\%s.torrent' % origin_filename

    # 传给待发布的站点
    filename = ' '.join(re.sub('^\[.{3,10}?\]|.mp4$|.mkv$|\[|\]|[^-\w]|[\u4e00-\u9fff]', ' ', origin_filename).split('.')).lstrip()
    back_file_path = config.backup_path + '\\%s.torrent' % filename

    try:
        response.raise_for_status()
        f = open(back_file_path, 'wb')
        for chunk in response.iter_content(100000):
            f.write(chunk)
        f.close()
        shutil.copyfile(back_file_path, file_path)
        print('种子下载保存成功！')
    except Exception as exc:
        print('种子下载失败: %s' % exc)
        sys.exit(0)

    return filename


def upload_torrent(raw_info, params=None, data=None, files=None):

    pt_sites = load_pt_sites()
    hudbt = pt_sites['hudbt']
    des_url = "{host}/takeupload.php".format(host=hudbt['domain'])
    des_cookie = hudbt['cookie']

    abs_file_path = config.backup_path + '\\%s' % raw_info['filename'] + '.torrent'
    try:
        files = [
            ("file", (raw_info['filename'], open(abs_file_path, "rb"), "application/x-bittorrent")),
            ("nfo", ("", "", "application/octet-stream")),
        ]
    except Exception as exc:
        print('待上传文件寻找失败: %s' % exc)
        sys.exit(0)

    data = {
        "dl-url": "",
        "name": raw_info['filename'],
        "small_descr": raw_info["small_descr"],
        "url": "",
        "descr": raw_info["descr"],
        "type": str(raw_info["type_"]),
        "data[Tcategory][Tcategory][]": "",
        "standard_sel": str(raw_info["standard_sel"]),
        "uplver": 'yes',
    }

    print('开始准备发布蝴蝶种子！')
    try:
        des_post = requests.post(
            url=des_url,
            params=params,
            data=data,
            files=files,
            cookies=des_cookie)
    except Exception as exc:
        print('发布种子失败: %s' % exc)
        sys.exit(0)

    print('获取上传种子下载链接……')

    seed_torrent_download_id = get_id(des_post.url)
    if seed_torrent_download_id == 0:
        sys.exit(0)
    else:
        print('准备下载蝴蝶种子！ id = %s' % seed_torrent_download_id)
        download_torrent(hudbt['domain'], seed_torrent_download_id, des_cookie)


def check(direction):
    if os.path.isfile(direction):
        return True
    else:
        return False


def main(origin_url):

    origin_site = find_origin_site(origin_url)
    if not origin_site:
        sys.exit(0)
    origin_cookie = origin_site['cookie']

    # 更改一下逻辑，先下载种子解析出返回的东西
    host = origin_site['domain']
    tid = get_id(origin_url)
    print('下载原始网站种子……')

    filename = download_torrent(host, tid, origin_cookie)
    # 待上传种子的绝对路径

    print('正在解析种子……')
    try:
        torrent_path = config.backup_path + '\\%s.torrent' % filename
        file_dir, file_path = parser_torrent.get_info_from_torrent(torrent_path)
    except Exception as exc:
        print('种子解析失败： %s' % exc)
        sys.exit(0)

    print('种子解析成功！')
    direction = config.check_path+'\\'+file_dir+'.txt'
    print('开始监听下载状态！')
    while True:
        if check(direction):
            break
        else:
            # print('休息10秒')
            sleep(10)

    html = get_html(origin_url, origin_cookie)
    raw_info = parser_choose(origin_site['abbr'], html, torrent_path)
    print('网页解析成功！')

    raw_info['filename'] = filename
    upload_torrent(raw_info)


if __name__ == '__main__':

    # 设置线程栈的大小
    # count = 0
    # threading.stack_size(64*1024)
    detail_link = input('请输入种子详情界面对应链接：')
    main(detail_link)
