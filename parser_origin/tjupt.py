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
    raw_info['site'] = 'tjupt'

    # 副标题
    small_descr = soup.select('td .rowfollow')[2].get_text()
    raw_info['small_descr'] = small_descr
#    print(small_descr)

    # 类型
    info = ''.join(to_bbcode(str(soup.select('td .rowfollow')[3])).split())
    raw_info['type_'] = tjupt_2_hudbt_type(info)

    # 详细信息
    raw_info['info'] = to_bbcode(str(soup.select('td .rowfollow')[4]))

    # 简介
    descr = str(soup.find('div', id='kdescr'))
    ad = str(soup.find('div', id='ad_torrentdetail'))
    descr = descr.replace(ad, '')
    descr = to_bbcode(descr)
    try:
<<<<<<< HEAD
<<<<<<< HEAD
        link = re.search('.*douban.com/subject/(\d{8})', descr)
=======
        link = re.search('◎豆瓣链接.*douban.com/subject/(\d{7,8})', descr)
>>>>>>> 89ee45c83bf04b032af0ed9649648009693fc440
=======
        link = re.search('◎豆瓣链接.*douban.com/subject/(\d{7,8})', descr)
>>>>>>> 89ee45c83bf04b032af0ed9649648009693fc440
        link = ('https://movie.douban.com/subject/'+link.group(1)+'/')
        descr = get_descr.get_full_descr(link, torrent_path)
    except Exception as exc:
        try:
            link_1 = re.search('.*imdb.com/title/(tt\d{7, 8})', descr)
            link_1 = 'https://www.imdb.com/title/'+link_1.group(1)+'/'
            descr = get_descr.get_full_descr(link_1, torrent_path)
        except Exception:
            print('该种子简介没有豆瓣或imdb链接.')
            descr = format_descr(descr)


    raw_info['descr'] = extend_descr(descr, raw_info['site'])
    # print(raw_info['descr'])

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

    # 图片补链接
    descr = descr.replace(
        '[img]attachments',
        '[img]https://www.tjupt.org/attachments')
    descr = descr.replace(
        'https://www.tjupt.org/jump_external.php?ext_url=', '')
    descr = descr.replace('/jump_external.php?ext_url=', '')
    descr = descr.replace('%3A', ':')
    descr = descr.replace('%2F', '/')

    return descr


def tjupt_2_hudbt_type(info):

    if info.find('剧集') >= 0:

        if info.find('大陆') >= 0:
            code = 402
        elif info.find('欧美') >= 0:
            code = 418
        elif info.find('日韩') >= 0:
            code = 416
        elif info.find('港台') >= 0:
            code = 417

    elif info.find('电影') >= 0:

        if info.find('大陆') >= 0:
            code = 401
        elif info.find('欧美') >= 0:
            code = 415
        elif info.find('日韩') >= 0:
            code = 414
        elif info.find('港台') >= 0:
            code = 413

    elif info.find('综艺') >= 0:

        if info.find('大陆') >= 0:
            code = 403
        elif info.find('欧美') >= 0:
            code = 421
        elif info.find('日韩') >= 0:
            code = 420
        elif info.find('港台') >= 0:
            code = 419

    elif info.find('音乐') >= 0:

        if info.find('大陆') >= 0:
            code = 408
        elif info.find('欧美') >= 0:
            code = 423
        elif info.find('日韩') >= 0:
            code = 422
        elif info.find('港台') >= 0:
            code = 408

    elif info.find('动漫') >= 0:
            code = 427

    elif info.find('纪录片') >= 0:
        code = 404

    elif info.find('移动视频') >= 0:
        code = 430

    elif info.find('体育') >= 0:
        code = 407

    elif info.find('软件') >= 0:
        code = 411

    elif info.find('资料') >= 0:
        code = 412

    else:
        code = 409

    return code


if __name__ == "__main__":

    html_ = open('../test_files/tjupt.html', encoding='utf-8')

    parser_html(html_)
