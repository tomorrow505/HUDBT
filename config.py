# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 19:06:57 2019

@author: CL
"""

save_path = "E:\\发种测试"
backup_path = "E:\\发种测试\\backup"
download_path = "G:\\ftp共享\LocalUser\\651"
img_path = "E:\\发种测试\\imgs"
check_path = "E:\\发种测试\\check"

extend_descr_before = """
   [quote][*]网站资源自动搬运测试，当前测试站点{site}。
   [*]一切以种子源文件为准，有误请举报或者联系管理员。[/quote]   
   """

extend_descr_after = """
   [quote]转自{site}, 感谢发布者!
   [/quote]
"""

'''
<select name="type" id="browsecat">
<option value="0">请选择</option>
<option value="401">大陆电影</option>
<option value="413">港台电影</option>
<option value="414">亚洲电影</option>
<option value="415">欧美电影</option>
<option value="430">iPad</option>
<option value="433">抢先视频</option>
<option value="402">大陆剧集</option>
<option value="417">港台剧集</option>
<option value="416">亚洲剧集</option>
<option value="418">欧美剧集</option>
<option value="404">纪录片</option>
<option value="407">体育</option>
<option value="403">大陆综艺</option>
<option value="419">港台综艺</option>
<option value="420">亚洲综艺</option>
<option value="421">欧美综艺</option>
<option value="408">华语音乐</option>
<option value="422">日韩音乐</option>
<option value="423">欧美音乐</option>
<option value="424">古典音乐</option>
<option value="425">原声音乐</option>
<option value="406">音乐MV</option>
<option value="409">其他</option>
<option value="432">电子书</option>
<option value="405">完结动漫</option>
<option value="427">连载动漫</option>
<option value="428">剧场OVA</option>
<option value="429">动漫周边</option>
<option value="410">游戏</option>
<option value="431">游戏视频</option>
<option value="411">软件</option>
<option value="412">学习</option>
<option value="426">MAC</option>
<option value="1037">HUST</option>
</select>

'''