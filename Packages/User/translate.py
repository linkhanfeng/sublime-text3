import json
import urllib
import re
import hashlib
from string import Template

import sublime
import sublime_plugin


class GoogleTranslateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        def sendRequest(url, params):
            pstr = ''
            for k,v in params.items():
                fixstr = ('?' if pstr == '' else '&')
                pstr =  pstr + fixstr + k +  '=' + v
            qUrl = url + pstr

            proxy_handler = urllib.request.ProxyHandler({})
            opener = urllib.request.build_opener(proxy_handler)
            with opener.open(qUrl) as f:
                data = f.read()
                jsonResultString = data.decode()
                jsonResult = json.loads(jsonResultString)
                pass
            return jsonResult

        selected_point = self.view.sel()[0]
        # 查询单词
        s_word = self.view.substr(selected_point)
        isEn = re.findall('[a-zA-Z0-9]+',s_word)

        # 百度
        url_baidu = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        appid = '20180305000131189'
        salt = '1234salt56'
        passKey = 'ktmJAzaP6htDBalyfUFX'
        signStr = '20180305000131189' + s_word + salt + passKey
        signStrMd5 = hashlib.md5(signStr.encode(encoding='UTF-8')).hexdigest()
        params_baidu = {
            'q': urllib.parse.quote(s_word),
            'from': "en" if isEn else "zh",
            'to': "zh" if isEn else "en",
            'appid': appid,
            'salt': salt,
            'sign': signStrMd5,
        }
        res_baidu = sendRequest(url_baidu, params_baidu)

        url_google = 'http://translate.google.cn/translate_a/single'
        params_google = {
            'client':'gtx',
            'sl': "en" if isEn else "zh-CN",
            'tl': "zh-CN" if isEn else "en",
            'dt':'t',
            'q':urllib.parse.quote(s_word)
        }
        res_google = sendRequest(url_google, params_google)

        baidu_word = ''
        baidu_word_html = ''
        for item in res_baidu['trans_result']:
            baidu_word = baidu_word + item['dst']
            baidu_word_html = baidu_word_html + '<p style="margin: 4px;">' + item['dst'] + '</p>'

        google_word = ''
        google_word_html = ''
        for item in res_google[0]:
            google_word = google_word + item[0]
            google_word_html = google_word_html + '<p style="margin: 4px;">' + item[0] + '</p>'

        sublime.set_clipboard(baidu_word.lower() + '\n' + google_word.lower())

        popupHtml = '<div style="border:1px solid #ccc; padding: 0 5px;"><span style="font-size:12px;margin:0;">百度:</span>' + baidu_word_html + '</div>' + '<div style="border:1px solid #ccc; padding: 0 5px;"><span style="font-size:12px;margin:0;">谷歌:</span>' + google_word_html + '</div>'
        self.view.show_popup(popupHtml, sublime.HIDE_ON_MOUSE_MOVE_AWAY, -1, 600, 500)