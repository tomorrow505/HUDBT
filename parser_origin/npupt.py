# -*- coding: utf-8 -*-
# Author:Chengli

from bs4 import BeautifulSoup
from html2bbcode.parser import HTML2BBCode
import config
import re
import get_descr


def parser_html(html, torrent_path):

    soup = BeautifulSoup(html, 'lxml')

    raw_info = {}

    # 网站
    raw_info['site'] = 'npupt'

#    #副标题
    small_descr = soup.select('.large')[0].get_text()
    raw_info['small_descr'] = small_descr

    # 类型
    info_1 = soup.find(class_='label label-success').get_text()
    info_2 = soup.find(class_='label label-info').get_text()
    raw_info['type_'] = npupt_2_hudbt_type(info_1 + info_2)

    # 简介
    ad = str(soup.find('div', class_='well small'))
    descr = to_bbcode(str(soup.select('#kdescr')[0]).replace(ad, ''))

    try:
        link = re.search(r'.*douban.com/subject/(\d{8})', descr)
        link = re.search(r'◎豆瓣链接.*douban.com/subject/(\d{7,8})', descr)
        link = ('https://movie.douban.com/subject/' + link.group(1)+'/')
        descr = get_descr.get_full_descr(link, torrent_path)
    except Exception:
        try:
            link_1 = re.search('.*imdb.com/title/(tt\d{7, 8})', descr)
            link_1 = 'https://www.imdb.com/title/'+link_1.group(1)+'/'
            descr = get_descr.get_full_descr(link_1, torrent_path)
        except Exception:
            print('该种子简介没有豆瓣或imdb链接.')
            descr = format_descr(descr)


    raw_info['descr'] = extend_descr(descr, raw_info['site'])

    # 清晰度
    raw_info['standard_sel'] = 0  # 默认：请选择，不提供清晰度指标

    return raw_info


def extend_descr(descr, site):
    before = config.extend_descr_before.format(site=site)
    after = config.extend_descr_after.format(site=site)
    return before + descr + after


def to_bbcode(descr):
    parser = HTML2BBCode()
    bbcode = parser.feed(descr)
    return bbcode


def format_descr(descr):
    tmp = []
    descr = descr.split('\n')
    for line in descr:
        if len(line.strip()) == 0:
            pass
        else:
            tmp.append(line)
    descr = '\n'.join(tmp)

    try:
        delete_str = re.findall(
            r'\[quote\].*Clone Info\n.*\[quote\]', descr)[0]
        descr = descr.replace(delete_str, '')
    except BaseException:
        pass
    # 图片补链接
    descr = descr.replace(
        '[img]attachments',
        '[img]https://npupt.com/attachments')
    descr = descr.replace(
        '[img]torrents/image/',
        '[img]https://npupt.com/torrents/image/')

    # 删除免责声明
    str_judge = '本站为非盈利性网站，本站的服务器中无任何资源内容'
    if descr.find(str_judge) >= 0:
        descr = descr[0:descr.find(str_judge) - 5]
    return descr


def npupt_2_hudbt_type(info):

    if info.find('剧集') >= 0:

        if info.find('大陆') >= 0:
            code = 402
        elif info.find('美剧') >= 0 or info.find('英剧') >= 0:
            code = 418
        elif info.find('日剧') >= 0 or info.find('韩剧') >= 0:
            code = 416
        elif info.find('港台') >= 0:
            code = 417

    elif info.find('电影') >= 0:

        if info.find('华语') >= 0:
            code = 401
        elif info.find('欧美') >= 0:
            code = 415
        elif info.find('日韩') >= 0:
            code = 414
        else:
            code = 414

    elif info.find('综艺') >= 0:
        code = 403

    elif info.find('音乐') >= 0:

        if info.find('华语') >= 0:
            code = 408
        elif info.find('欧美') >= 0:
            code = 423
        elif info.find('日韩') >= 0:
            code = 422

    elif info.find('纪录') >= 0:
        code = 404

    elif info.find('移动视频') >= 0:
        code = 430

    elif info.find('体育') >= 0:
        code = 407

    elif info.find('软件') >= 0:
        code = 411

    elif info.find('资料') >= 0:
        code = 412

    elif info.find('动漫') >= 0:
        code = 427

    else:
        code = 409

    return code


if __name__ == "__main__":

    html = open('../test_files/npupt.html', encoding='utf-8')

    parser_html(html)
