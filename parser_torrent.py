# -*- coding: utf-8 -*-

'''
为了匹配ut传过来的消息，根据torrent信息返回种子内容下载的：
    1、文件就一个的话：相对路径
    2、文件多个的话：  所在目录和某个视频相对路径
'''


import torrent_parser as tp


def get_info_from_torrent(file):

    data = tp.parse_torrent_file(file)
    info = data['info']
    file_dir = info['name']
    if 'files' in info.keys():
        biggest = 0
        file_path = ''
        files = info['files']
        for file in files:
            if file['length'] > biggest and (file['path'][0].endswith('mp4'or 'mkv'or 'avi'or 'ts' or 'mov')):
                file_path = file['path'][0]
        file_path = file_dir+'\\'+file_path
        return file_dir, file_path
    else:
        return file_dir, file_dir


if __name__ == "__main__":

    # file_ = r'C:\test.torrent'
    file_ = input('请输入一个种子的绝对路径')
    print(get_info_from_torrent(file_))

