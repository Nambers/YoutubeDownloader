# -*- coding: utf-8 -*-
# @Time: 2021/1/10
# @Author: Eritque arcus
# @File: Youtube.py
# @License: MIT
# @Environment:
#           - windows 10
#           - python 3.6.2
# @Dependence:
#           - jsdom in npm(windows also can use)
#           - requests, execjs, re, json in python
import requests
import execjs
import re
import json


def gethtml(url):
    # set the headers or the website will not return information
    # the cookies in here you may need to change
    headers = {
        "cache-Control": "no-cache",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                  "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "lang=en; country=CN; uid=fd94a82a406a8dd4; sfHelperDist=72; reference=14; "
                  "clickads-e2=90; poropellerAdsPush-e=63; promoBlock=64; helperWidget=92; "
                  "helperBanner=42; framelessHdConverter=68; inpagePush2=68; popupInOutput=9; "
                  "_ga=GA1.2.799702638.1610248969; _gid=GA1.2.628904587.1610248969; "
                  "PHPSESSID=030393eb0776d20d0975f99b523a70d4; x-requested-with=; "
                  "PHPSESSUD=islilfjn5alth33j9j8glj9776; _gat_helperWidget=1; _gat_inpagePush2=1",
        "origin": "https://en.savefrom.net",
        "pragma": "no-cache",
        "referer": "https://en.savefrom.net/1-youtube-video-downloader-4/",
        "sec-ch-ua": "\"Google Chrome\";v=\"87\", \"Not;A Brand\";v=\"99\",\"Chromium\";v=\"87\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "iframe",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/87.0.4280.88 Safari/537.36"}
    # set the parameter, we can get from chrome
    kv = {"sf_url": url,
          "sf_submit": "",
          "new": "1",
          "lang": "en",
          "app": "",
          "country": "cn",
          "os": "Windows",
          "browser": "Chrome"}
    # do the POST request
    r = requests.post(url="https://en.savefrom.net/savefrom.php", headers=headers,
                      data=kv)
    r.raise_for_status()
    # get the result
    return r.text


if __name__ == '__main__':
    # target(youtube address) url
    url = "https://www.youtube.com/watch?v=YPvtz1lHRiw"
    # get the target text
    reo = gethtml(url)
    # Remove the code from the head and tail (we need the javascript part, information store with encryption in js part)
    reo = reo.split("<script type=\"text/javascript\">")[1].split("</script>")[0]
    # override the alert function, because in the code there has one place using
    # and we cannot do the alerting in execjs(it is meaningless) however, if we donnot override, the code will raise a error
    reo = reo.replace("(function(){", "(function(){\nthis.alert=function(){};")
    # split each line(help us find the decrypt function in last few line)
    reA = reo.split("\n")
    # get the depcrypt function
    name = reA[len(reA) - 3].split(";")[0] + ";"
    # add jsdom into the execjs because the code will use(maybe there is a solution without jsdom, but i have no idea)
    addition = """
    const jsdom = require("jsdom");
    const { JSDOM } = jsdom;
    const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
    window = dom.window;
    document = window.document;
    XMLHttpRequest = window.XMLHttpRequest;
    """
    # use execjs to execute the js code, and the cwd is the result of `npm root -g`(the path of npm in your computer)
    ct = execjs.compile(addition + reo, cwd=r'C:\Users\19308\AppData\Roaming\npm\node_modules')
    # do the decryption
    text = ct.eval(name.split("=")[1].replace(";", ""))
    # get the result in json
    result = re.search('show\((.*?)\);;', text, re.I | re.M).group(0).replace("show(", "").replace(");;", "")
    # use `json` to load json
    j = json.loads(result)
    # the selection of video(in this case, num=1 mean the video is
    # - 360p known from j["url"][num]["quality"]
    # - MP4 known from j["url"][num]["type"]
    # - audio known from j["url"][num]["audio"]
    num = 1
    downurl = j["url"][num]["url"]
    # do some download
    # thanks :)
    # - EOF -
