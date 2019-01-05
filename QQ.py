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
