# -*- coding: utf-8 -*-

'''

根据parser_torrent传过来的某个视频的绝对路径进行截图存储到由种子id+config构成的绝对路径，上传返回网络地址

'''

import os
import get_mediainfo
import requests
import json


# 需要将从网络上下载的ffmpeg的bin目录放到系统环境中
# 根据视频的绝对地址将图片保存到本地

def get_picture(file_loc, img_loc):
	# 获取截图时间节点
	time = []
	ratio, total = get_mediainfo.get_frame(file_loc)
	total_time = int(total)/(int(ratio.split('.')[0]))
	start = total_time * 0.1  # 第一张图开始的时间节点
	step = total_time * 0.8/11  # 后续步长
	time.append(change_to_ss(start))
	for i in range(1, 12):
		midle = start + i*step
		time.append(change_to_ss(midle))

	for i in range(12):
		base_command = 'ffmpeg -ss {time} -i {file} -vframes 1 -y -vf "scale=500:-1" out-{i}.jpg'
		ffmpeg_sh = base_command.format(time=time[i], file=file_loc, i=i)
		os.system(ffmpeg_sh)
	set_par = 'tile=3x4:nb_frames=0:padding=5:margin=5:color=random'
	base_command = 'ffmpeg -i "out-%d.jpg" -y -filter_complex "{set}" {img_loc}'.format(set=set_par, img_loc=img_loc,)

	os.system(base_command)

	for i in range(12):
		os.remove('out-{i}.jpg'.format(i=i))

	# 拼接图床上传需要的信息上传返回图片网址
	data = {
		'smfile': open(img_loc, "rb"),
		'file_id': ' '
		}
	pic_url = send_picture(files=data)

	thanks = '[quote]自动随机截图，不喜勿看。——>该部分感谢@[url=https://hudbt.hust.edu.cn/userdetails.php?id=107055][color=Red]rach[/color][/url]的指导[/quote]\n'

	return thanks+'[img]'+pic_url+'[/img]'


def send_picture(files=None):

	des_url = 'https://sm.ms/api/upload'
	try:
		des_post = requests.post(
			url=des_url,
			files=files)
	except Exception as exc:
		print('发布图片失败: %s' % exc)

	data = json.loads(des_post.content.decode())['data']

	url_to_descr = data['url']

	return url_to_descr


# 将时间转换成HH:MM:SS格式
def change_to_ss(number):
	hh = int(number/3600)
	number_ = number - 3600*hh
	mm = int(number_/60)
	ss = int(number_ - 60*mm)
	hh = str(hh).zfill(2)
	mm = str(mm).zfill(2)
	ss = str(ss).zfill(2)
	time = '%s:%s:%s' % (hh, mm, ss)
	return time


if __name__ == "__main__":

	file = r'./test.mkv'
	img_ = r'./test.jpg'
	get_picture(file, img_)

