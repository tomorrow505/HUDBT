# -*- coding: utf-8 -*-

# utorrent 执行代码 "C:\Users\CL\hudbt\hudbt.bat" "%D" "%N"

import sys
import config


def write_task_txt(info):

    txt_path = config.check_path+'\\'+info[1]+'.txt'
    with open(txt_path, 'w+') as f:
        f.write('OK')


if __name__ == "__main__":

    info_ = sys.argv[1:]
    write_task_txt(info_)

