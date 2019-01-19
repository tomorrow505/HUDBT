# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 13:57:57 2019

@author: CL
"""

import requests
import get_picture
import parser_torrent
import get_mediainfo
import config


# 使用一位大佬提供的api获取结构化的数据
def get_descr_douban(url):

    ptgen_api_url = "https://api.rhilip.info/tool/movieinfo/gen"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    session = requests.session()

    session.headers = headers

    ptgen_api = session.get(ptgen_api_url, params={"url": url})

    ptgen_api_json = ptgen_api.json()

    descr = ptgen_api_json["format"]

    return descr


# 根据传来的种子路径获取mediainfo和视频缩略图，综合在一起

def get_full_descr(url, torrent_path):

    descr = get_descr_douban(url)

    file_dir, file_path = parser_torrent.get_info_from_torrent(torrent_path)

    abs_file_path = config.download_path+'\\'+file_path

    mediainfo = get_mediainfo.get_info(abs_file_path)

    img_loc = config.img_path+'\\'+file_path.split('\\')[-1]+'.jpg'

    pic_url = get_picture.get_picture(abs_file_path, img_loc)

    descr = descr + '\n' + mediainfo + '\n' + pic_url

    return descr


if __name__ == '__main__':

    print(get_descr_douban('https://movie.douban.com/subject/30377703/'))

