# -*- coding: utf-8 -*-

'''
根据parser_torrent返回来的文件名进行mediainfo的获取，前提是有豆瓣链接否则太乱了
本地使用main的话可以输入一个视频绝对路径来获取mediainfo
'''

import json
from pymediainfo import MediaInfo


# 需要pymediainfo，需要安装mediainfo软件并且将mediainfo.dll放到python安装目录下
def get_info(video_file):

    mediainfo = ''
    media_info = MediaInfo.parse(video_file)
    data = media_info.to_json()
    data = json.loads(data)['tracks']
    for key in data:
        # print(key)
        if key['track_type'] == 'General':
            general = get_general(key)
            mediainfo = general + '\n'
        elif key['track_type'] == 'Video':
            video = get_video(key)
            mediainfo = mediainfo + '\n' + video + '\n'
        elif key['track_type'] == 'Audio':
            audio = get_audio(key)
            mediainfo = mediainfo + '\n' + audio + '\n'

    mediainfo = '[quote]'+mediainfo+'[/quote]'

    return mediainfo


def get_general(key):

    general = []
    general.append(key['track_type'])
    general.append(check('UniqueID/String------------------: ', key, 'other_unique_id'))
    general.append(check('Format/String--------------------: ', key, 'format'))
    general.append(check('Format_Version-------------------: ', key, 'format_version'))
    general.append(check('FileSize/String------------------: ', key, 'other_file_size'))
    general.append(check('Duration/String------------------: ', key, 'other_duration'))
    general.append(check('OverallBitRate/String------------: ', key, 'other_overall_bit_rate'))
    general.append(check('Encoded_Date---------------------: ', key, 'encoded_date'))
    general.append(check('other_writing_application--------: ', key, 'other_writing_application'))
    general.append(check('Encoded_Application/String-------: ', key, 'writing_library'))

    general = '\n'.join(part for part in general if part)
    return general


def get_audio(key):

    general = []
    general.append(key['track_type'])

    general.append(check('ID/String------------------------: ', key, 'count_of_stream_of_this_kind'))
    general.append(check('Format/String--------------------: ', key, 'other_format'))
    general.append(check('Format/Info----------------------: ', key, 'format_info'))
    general.append(check('CodecID--------------------------: ', key, 'codec_id'))
    general.append(check('Duration/String------------------: ', key, 'other_duration'))
    general.append(check('BitRate/String-------------------: ', key, 'other_bit_rate'))
    general.append(check('Channel(s)/String----------------: ', key, 'other_channel_s'))
    general.append(check('ChannelLayout--------------------: ', key, 'channel_layout'))
    general.append(check('SamplingRate/String--------------: ', key, 'other_sampling_rate'))
    general.append(check('FrameRate/String-----------------: ', key, 'other_frame_rate'))
    general.append(check('Compression_Mode/String----------: ', key, 'compression_mode'))
    general.append(check('Video_Delay/String---------------: ', key, 'other_delay_relative_to_video'))
    general.append(check('StreamSize/String----------------: ', key, 'other_stream_size'))
    general.append(check('Title----------------------------: ', key, 'title'))
    general.append(check('Language/String------------------: ', key, 'other_language'))
    general.append(check('Default/String-------------------: ', key, 'default'))
    general.append(check('Forced/String--------------------: ', key, 'forced'))

    general = '\n'.join(part for part in general if part)
    return general


def get_video(key):

    general = []
    general.append(key['track_type'])

    general.append(check('ID/String------------------------: ', key, 'count_of_stream_of_this_kind'))
    general.append(check('Format/String--------------------: ', key, 'format'))
    general.append(check('Format/Info----------------------: ', key, 'format_info'))
    general.append(check('Format_Profile-------------------: ', key, 'format_profile'))
    general.append(check('Format_Settings------------------: ', key, 'format_settings'))
    general.append(check('Format_Settings_CABAC/String-----: ', key, 'format_settings__cabac'))
    general.append(check('Format_Settings_RefFrames/String-: ', key, 'other_format_settings__reframes'))
    general.append(check('CodecID--------------------------: ', key, 'codec_id'))
    general.append(check('Duration/String------------------: ', key, 'other_duration'))
    general.append(check('BitRate/String-------------------: ', key, 'other_bit_rate'))
    general.append(check('Width/String---------------------: ', key, 'other_width'))
    general.append(check('Height/String--------------------: ', key, 'other_height'))
    general.append(check('DisplayAspectRatio/String--------: ', key, 'other_display_aspect_ratio'))
    general.append(check('FrameRate_Mode/String------------: ', key, 'other_frame_rate_mode'))
    general.append(check('FrameRate/String-----------------: ', key, 'other_frame_rate'))
    general.append(check('ColorSpace-----------------------: ', key, 'color_space'))
    general.append(check('ChromaSubsampling/String---------: ', key, 'chroma_subsampling'))
    general.append(check('BitDepth/String------------------: ', key, 'other_bit_depth'))
    general.append(check('ScanType/String------------------: ', key, 'other_scan_type'))
    general.append(check('Bits-(Pixel*Frame)---------------: ', key, 'bits__pixel_frame'))
    general.append(check('StreamSize/String----------------: ', key, 'other_stream_size'))
    general.append(check('Default/String-------------------: ', key, 'default'))
    general.append(check('Forced/String--------------------: ', key, 'forced '))

    general = '\n'.join(part for part in general if part)
    return general


# 解析出来的基本信息有的视频没有，所以做一个检查
def check(str1, key, str2):
    if str2 in key.keys():
        if str2.find('other') >= 0:
            r_part = key[str2][0]
        else:
            r_part = key[str2]
        return str1 + r_part
    else:
        return ''


# 这里开了一个接口给get_picture，因为需要知道片子多长，在哪些时间节点截图拼接缩略图

def get_frame(video_file):
    media_info = MediaInfo.parse(video_file)
    data = media_info.to_json()
    data = json.loads(data)['tracks']
    for key in data:
        # print(key)
        if key['track_type'] == 'Video':
            frame_rate = key['frame_rate']
            frame_count = key['frame_count']
            break
    return frame_rate, frame_count


if __name__ == "__main__":
    file = input('请输入一个视频的绝对路径：')
    print(get_info(file))
    # frame_rate0, frame_count0 = get_frame(file)
    # print(frame_rate0, frame_count0)

