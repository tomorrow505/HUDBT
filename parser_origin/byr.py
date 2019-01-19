# -*- coding: utf-8 -*-
# Author:Chengli

from bs4 import BeautifulSoup
from html2bbcode.parser import HTML2BBCode
import config
import re
import get_descr


# 根据原始网站的结构特征进行解析，不做多的说明
def parser_html(html, torrent_path):

    soup = BeautifulSoup(html, 'lxml')
    raw_info = {}
    raw_info['site'] = 'byr'

    # 副标题
    small_descr = soup.select('#subtitle')[0].get_text()
    sub_info = to_bbcode(str(soup.find('h1', id='share')))
    sub_info = re.sub('\[[^\u4e00-\u9fff]+\]|\[|\]', ' ', sub_info)
    sub_info = re.sub("国产|连载|华语|英文|大陆|欧美", "", sub_info).replace(' ','')
    if len(small_descr) == 0:
        small_descr = sub_info

    raw_info['small_descr'] = small_descr

    # 简介
    descr = to_bbcode(str(soup.find('div', id='kdescr')))
    try:
        # 这里检验的re的pattern有点问题，不过可以用，如果有豆瓣信息，自己构造简介
<<<<<<< HEAD
        link = re.search('.*douban.com/subject/(\d{8})', descr)
=======
        link = re.search('◎豆瓣链接.*douban.com/subject/(\d{7,8})', descr)
>>>>>>> 89ee45c83bf04b032af0ed9649648009693fc440
        link = ('https://movie.douban.com/subject/'+link.group(1)+'/')
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

    # 类型
    type_ = []
    type_.append(soup.select('#type')[0].get_text())
    type_.append(soup.select('#sec_type')[0].get_text())
    raw_info['type_'] = byr_2_hudbt_type(type_)

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


# 这里对原始简介进行一些操作，需要根据网站自己测试
def format_descr(descr):
    tmp = []
    descr = descr.split('\n')
    for line in descr:
        if len(line.strip()) == 0:
            pass
        else:
            tmp.append(line)
    descr = '\n'.join(tmp)
    descr = re.sub('海报.{0,3}\[img\]', '[img]', descr)
    descr = re.sub('简介.{0,4}◎', '简介\n◎', descr)
    return descr


# 类型转换有部分确实，如果提示没有定义code直接使用的bug就过来补一补
def byr_2_hudbt_type(type_):
    code = 0
    if type_[0] == "电影":
        if type_[1] == "华语":
            code = 401
        elif type_[1] == "欧洲" or type_[1] == "北美":
            code = 415
        elif type_[1] == "亚洲":
            code = 414

    elif type_[0] == "剧集":
        if type_[1] == "大陆":
            code = 402
        elif type_[1] == "日韩":
            code = 416
        elif type_[1] == "欧美":
            code = 418
        elif type_[1] == "港台":
            code = 417

    elif type_[0] == "动漫":
        if type_[1] == "周边":
            code = 429
        else:
            code = 427

    elif type_[0] == "综艺":
        if type_[1] == "大陆":
            code = 403
        elif type_[1] == "日韩":
            code = 420
        elif type_[1] == "欧美":
            code = 421
        elif type_[1] == "港台":
            code = 419

    elif type_[0] == "音乐":
        if type_[1] == "大陆":
            code = 408
        elif type_[1] == "日韩":
            code = 422
        elif type_[1] == "欧美":
            code = 423
        elif type_[1] == "港台":
            code = 408

    elif type_[0] == "软件":
        code = 411
    elif type_[0] == "资料":
        code = 412
    elif type_[0] == "体育":
        code = 407
    elif type_[0] == "记录":
        code = 404
    else:
        code = 409

    return code


if __name__ == "__main__":
    html = open('../test_files/byr.html', encoding='utf-8')
    parser_html(html)
