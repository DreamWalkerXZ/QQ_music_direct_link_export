# QQ_music_direct_link_export

# QQ音乐无损解析教程

*Credit to DreamWalkerXZ under CC BY 4.0*

## 1.搜索

```python
keyword = '李健'
search_api = 'http://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.center&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=50&w=' + keyword + '&jsonpCallback=searchCallbacksong2020&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
response = requests.get(search_api).text
```

![搜索数据](https://s1.ax1x.com/2018/11/10/iqlW9I.png)

即歌曲就在json.loads(response)['data']\['song']['list']中

## 2.解析

首先我们来看一个解析后的url：

```python
'http://streamoc.music.tc.qq.com/M800000PLHrM2luXiz.mp3?vkey=CA23BC73FA35144644BAD2C8E3026425F724AD8AA117AD079FB5812177575B59044EF642A3B422F3A9E7FEFF185839FC163444AD015BB875&guid=DreamWalkerXZ&uin=123456&fromtag=8'
```

然后把它的参数给分离出来

```python
'http://streamoc.music.tc.qq.com/' + prefix + mid + extension + '?vkey=' + vkey + '&guid=' + guid + '&uin=' + uin + '&fromtag=8'
```

### prefix与extension

prefix是音频格式的前缀， 与extension相对应

| quality | prefix | extension |
| ------- | ------ | --------- |
| dts     | D00A   | .flac     |
| ape     | A000   | .ape      |
| flac    | F000   | .flac     |
| 320     | M800   | .mp3      |
| aac     | C600   | .m4a      |
| ogg     | O600   | .ogg      |
| 128     | M500   | .mp3      |

至于如何判断是否有此品质，只需要在第一步的搜索结果中的json.loads(response)['data']\['song']['list']\[歌曲位置]['file']中判断size_128, size_320, size_aac, size_ape, size_dts, size_flac, size_ogg这几个项的值是否为0即可（为0则代表无此品质）

### mid

mid是QQ音乐中每一首歌曲的唯一标识符

mid即json.loads(response)['data']\['song']['list']\[歌曲位置]['mid']的值

### uin与guid

guid和uin随意填充即可, 但是要与后面生成vkey时所填的一致

### vkey

vkey是一个通过算法生成的具有时效性的字符串

生成算法如下：

```python
vkey = json.loads(requests.get('http://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=0&loginUin=' + uin + '&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&uin=' + uin + '&songmid=003a1tne1nSz1Y&filename=C400003a1tne1nSz1Y.m4a&guid=' + guid).text)['data']['items'][0]['vkey']
# 1.注意uin与guid在生成vkey和拼接直链时要一致
# 2.如果服务器在国外，请使用国内的HTTP代理来访问此接口，否则会因为版权问题无法解析
```

## 成品

> QQ.py （类）

```python
import json
import requests


class QQ():
    def search(self, song_name):
        search_url = 'http://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.center&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=50&w=' + song_name + '&jsonpCallback=searchCallbacksong2020&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
        search_result = []
        for item in json.loads(requests.get(search_url).text)['data']['song']['list']:
            name = item['name']
            singer = ''.join(singer['name'] + '+' for singer in item['singer']).rstrip('+')
            album = item['album']['name']
            media_mid = item['file']['media_mid']
            types = []
            if item['file']['size_128'] != 0:
                types.append('128')
            if item['file']['size_320'] != 0:
                types.append('320')
            if item['file']['size_aac'] != 0:
                types.append('aac')
            if item['file']['size_ape'] != 0:
                types.append('ape')
            if item['file']['size_dts'] != 0:
                types.append('dts')
            if item['file']['size_flac'] != 0:
                types.append('flac')
            if item['file']['size_ogg'] != 0:
                types.append('ogg')
            search_result.append({'name': name, 'singer': singer, 'album': album, 'media_mid': media_mid, 'types': types})
        return search_result

    def get_audio_url(self, media_mid, type):
        if type == 'dts':
            type = {'prefix': 'D00A', 'extension': '.flac'}
        elif type == 'ape':
            type = {'prefix': 'A000', 'extension': '.ape'}
        elif type == 'flac':
            type = {'prefix': 'F000', 'extension': '.flac'}
        elif type == '320':
            type = {'prefix': 'M800', 'extension': '.mp3'}
        elif type == 'aac':
            type = {'prefix': 'C600', 'extension': '.m4a'}
        elif type == 'ogg':
            type = {'prefix': 'O600', 'extension': '.ogg'}
        elif type == '128':
            type = {'prefix': 'M500', 'extension': '.mp3'}
        else:
            raise Exception("Invalid type", type)
        uin = '123456'
        guid = 'DreamWalkerXZ'
        vkey = json.loads(requests.get('http://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=0&loginUin=' + uin + '&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&uin=' + uin + '&songmid=003a1tne1nSz1Y&filename=C400003a1tne1nSz1Y.m4a&guid=' + guid).text)['data']['items'][0]['vkey']
        return 'http://streamoc.music.tc.qq.com/' + type['prefix'] + media_mid + type['extension'] + '?vkey=' + vkey + '&guid=' + guid + '&uin=' + uin + '&fromtag=8'

```

> 调用示例

```python
import QQ


qq = QQ.QQ()


# 搜索
search_result = qq.search('李健')
print(search_result)
###
[{'name': '贝加尔湖畔',
  'singer': '李健',
  'album': '依然',
  'media_mid': '000PLHrM2luXiz',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '假如爱有天意',
  'singer': '李健',
  'album': '李健',
  'media_mid': '003u0BdF1aocDJ',
  'types': ['128', '320', 'aac', 'flac', 'ogg']},
 {'name': '父亲写的散文诗',
  'singer': '李健',
  'album': '歌手 第8期',
  'media_mid': '000kJyuz4XCoOT',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '风吹麦浪',
  'singer': '李健',
  'album': '想念你',
  'media_mid': '000VItvW1y75J6',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '春风十里不如你',
  'singer': '李健',
  'album': '春风十里不如你',
  'media_mid': '001KfBE41t5s8F',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '传奇',
  'singer': '李健',
  'album': '似水流年',
  'media_mid': '00471z1Z49DUmW',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '异乡人',
  'singer': '李健',
  'album': '想念你',
  'media_mid': '001Liwq92gKerW',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '抚仙湖',
  'singer': '李健',
  'album': '想念你',
  'media_mid': '0016EGeo41UeGu',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '沧海轻舟',
  'singer': '李健',
  'album': '李健',
  'media_mid': '001WDB6342DM9f',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '水流众生',
  'singer': '李健',
  'album': '水流众生',
  'media_mid': '004eLWmo36vXU9',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '爱江山更爱美人 + 一剪梅',
  'singer': '吴秀波+李健',
  'album': '跨界歌王第三季 第12期',
  'media_mid': '003kbJqY4ESjGb',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '红豆曲 ＋ 一生所爱',
  'singer': '李健',
  'album': '歌手 第10期',
  'media_mid': '00281NAt3OFJxv',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '唐僧在女儿国抒怀并看着女儿国王的眼睛',
  'singer': '李健+岳云鹏',
  'album': '歌手 歌王之战',
  'media_mid': '0033LHzO3i0I6R',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '向往',
  'singer': '李健',
  'album': '为你而来',
  'media_mid': '001CLHur1ekin4',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '十点半的地铁',
  'singer': '李健',
  'album': '歌手 第9期',
  'media_mid': '003vObYU3VG6Yd',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '梦一场',
  'singer': '李健',
  'album': '遥远的天空底下',
  'media_mid': '002aYvDj0Ejdph',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '我始终在这里',
  'singer': '李健',
  'album': '依然',
  'media_mid': '003ZDNEb46Cnel',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '懂得',
  'singer': '李健',
  'album': '懂得',
  'media_mid': '002AzeJ92OvaLo',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '似水流年',
  'singer': '李健',
  'album': '似水流年',
  'media_mid': '002rXVeQ29nM5K',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '等我遇见你',
  'singer': '李健',
  'album': '等我遇见你',
  'media_mid': '004czDP51xf9Qt',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '月光',
  'singer': '李健+邢天溯',
  'album': '月光',
  'media_mid': '002xL8sn14yEmJ',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': "水流众生 + Pi's Lullaby",
  'singer': '李健+旦增尼玛',
  'album': '2018中国好声音 第13期',
  'media_mid': '0026ZFix0FhShV',
  'types': ['128', '320', 'aac', 'flac', 'ogg']},
 {'name': '一往情深的恋人',
  'singer': '李健',
  'album': '音乐傲骨',
  'media_mid': '000KQrdK4LnAio',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '城市之光',
  'singer': '李健',
  'album': '城市之光',
  'media_mid': '0000XgX43v7WMx',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': 'Love Is Over',
  'singer': '李健',
  'album': '歌手 第11期',
  'media_mid': '002t3tfn3y2eCp',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '美若黎明',
  'singer': '李健',
  'album': '李健',
  'media_mid': '004XNJDO4AOU4Q',
  'types': ['128', '320', 'aac', 'ape', 'dts', 'flac', 'ogg']},
 {'name': '父亲',
  'singer': '李健',
  'album': '为你而来',
  'media_mid': '0037II3o36pk4N',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '山歌好比春江水',
  'singer': '李健',
  'album': '山歌好比春江水',
  'media_mid': '003axPON2GWoMv',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '为你而来',
  'singer': '李健',
  'album': '为你而来',
  'media_mid': '0031GbS21zkmio',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '心升明月',
  'singer': '李健',
  'album': '依然',
  'media_mid': '004fiWop08WVhP',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '故乡',
  'singer': '李健',
  'album': '故乡',
  'media_mid': '003QSA8L2pRgMv',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '矜持',
  'singer': '李健',
  'album': '遥远的天空底下',
  'media_mid': '001bTKM82MM0Kx',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '故乡山川',
  'singer': '李健',
  'album': '音乐傲骨',
  'media_mid': '003FiXOv4fu5tw',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '让我一次爱个够 + 因为爱所以爱 + 抚仙湖 + 等你下课 + 霍元甲 + 万里长城永不倒',
  'singer': '周杰伦+谢霆锋+李健+庾澄庆',
  'album': '2018中国好声音 第1期',
  'media_mid': '002kl3jU20ZhWf',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '我愿人长久',
  'singer': '李健',
  'album': '我愿人长久',
  'media_mid': '001jHQQb2DRqKI',
  'types': ['128', '320', 'aac', 'ogg']},
 {'name': '青春再见',
  'singer': '水木年华+李健+老狼+叶世荣',
  'album': '怒放之青春再见',
  'media_mid': '003vNuAK2HnIcQ',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '风一样自由',
  'singer': '张博+邢佳栋+李健+张宁江',
  'album': '战雷 电视剧原声带',
  'media_mid': '000tj3mu1IdYpb',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '深海之寻',
  'singer': '李健',
  'album': '李健',
  'media_mid': '003yp9eo3HmD3c',
  'types': ['128', '320', 'aac', 'ape', 'dts', 'flac', 'ogg']},
 {'name': '当有天老去',
  'singer': '李健',
  'album': '拾光',
  'media_mid': '000HPdy04OhaMN',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '绽放',
  'singer': '李健',
  'album': '似水流年',
  'media_mid': '000Go2BE3pZKtc',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '雾中列车',
  'singer': '李健+王俊凯',
  'album': '雾中列车',
  'media_mid': '004Akkce39MD2k',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '陀螺',
  'singer': '李健',
  'album': '遥远的天空底下',
  'media_mid': '003mNvZz3XgPJQ',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '丽江',
  'singer': '李健',
  'album': '拾光',
  'media_mid': '0003h4Vg0UsUJH',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '消失的月光',
  'singer': '李健',
  'album': '李健',
  'media_mid': '004YSae13gb0zf',
  'types': ['128', '320', 'aac', 'ape', 'dts', 'flac', 'ogg']},
 {'name': '风吹黄昏',
  'singer': '李健',
  'album': '李健',
  'media_mid': '001LwxmU2im2GE',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '你一言我一语',
  'singer': '李健',
  'album': '你一言我一语',
  'media_mid': '004SgplL25NNdW',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '三月的一整月',
  'singer': '李健',
  'album': '歌手 2017巅峰会',
  'media_mid': '000b1Kxo3RYr7V',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '等待黎明',
  'singer': '李健',
  'album': '等待黎明',
  'media_mid': '000wjQbd2J2Kbd',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '风花树',
  'singer': '李健',
  'album': '徜徉',
  'media_mid': '002YHh4B3V6uie',
  'types': ['128', '320', 'aac', 'ape', 'flac', 'ogg']},
 {'name': '日落之前',
  'singer': '李健',
  'album': '李健',
  'media_mid': '0047DwLA1u9FEx',
  'types': ['128', '320', 'aac', 'ape', 'dts', 'flac', 'ogg']}]
###

# 解析
audio_url = qq.get_audio_url('001Liwq92gKerW', '320')
print(audio_url)
###
http://streamoc.music.tc.qq.com/M800001Liwq92gKerW.mp3?vkey=17E517E90215EB25F6DD717CE479C6E9573EB9505EA633F4909A32725B490ACDF5A934BB8674363A90C8C076104C2412E6FCADCF58FB5DC0&guid=DreamWalkerXZ&uin=123456&fromtag=8
###
```

另外欢迎大家访问"[https://musicget.dreamwalkerxz.tk/](https://musicget.dreamwalkerxz.tk/)"来使用我的在线解析
