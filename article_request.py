# _*_ coding: utf-8 _*_
import requests
import time
import urllib3
import html
import re
import html
import json
from bs4 import BeautifulSoup, element
from bs4 import NavigableString

__author__ = "weaponzhi"


def headers_to_dict(headers):
    headers = headers.split("\n")
    d_headers = dict()
    for h in headers:
        if h:
            k, v = h.split(":", 1)
            d_headers[k] = v.strip()
    return d_headers


def crawl():
  url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MjA5MTQyMA==&scene=126&devicetype=iOS11.4.1&version=16070227&lang=en&nettype=WIFI&a8scene=0&fontScale=94&pass_ticket=aGWzzp8%2Bzyir2DKPLDnrceAi21LIqICuCOJi4d46Qnc3H4YWQtybMQQwha0k6Vv5&wx_header=1"
  headers ={
      'Host': 'mp.weixin.qq.com',
      'Cookie': 'devicetype=iOS11.4.1; lang=en; pass_ticket=aGWzzp8+zyir2DKPLDnrceAi21LIqICuCOJi4d46Qnc3H4YWQtybMQQwha0k6Vv5; version=16070227; wap_sid2=CI/I96QLElxNSEJKcXljSVhxNGRMUXlEdUd6TW5FUEpxejlVR2tmSGs0ajdocW9wRDRIeWVNYlNVOUFvTm9ZSFV5MWZHNG1VTWprM1NBWURPZnB6NnZleVlIREtQOHdEQUFBfjC8wajcBTgNQJVO; wxuin=3030246415; wxtokenkey=777; rewardsn=; pgv_pvid=7650693240',
      'X-WECHAT-KEY': 'ac42b1aa2afa340b2e560f13ee9f1beb1a20ebc43f5d307b4604acba10a9d3fbcb75d0073b3a94b19427651a1447cbcbd1ab67bc5d84083ddce69a192f4b7e0b9b167c5ce099f58e6c2debda5e54e3fd',
      'X-WECHAT-UIN': 'MzAzMDI0NjQxNQ%3D%3D',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77 MicroMessenger/6.7.2 NetType/WIFI Language/en',
      'Accept-Language': 'en-us',
      'Accept-Encoding': 'br, gzip, deflate',
      'Connection':  'keep-alive',
  }
  #headers = headers_to_dict(headers)
  response = requests.get(url, headers=headers, verify=False)
  result = response.json()
  if '<title>验证</title>' in response.text:
      raise Exception("获取微信公众号文章失败，可能是因为你的请求参数有误，请重新获取")
  data = extract_data(response.text)
  
  rex = r'\\/'
  for item in data:
      pattern = re.sub(rex, '/', html.unescape(data.get(item)))
      response = requests.get(pattern, headers=headers, verify=False)
      parser_text_to_file(item, response.text)
  #crawl_msg(11)
  
def parser_text_to_file(title, article_content):
    soup = BeautifulSoup(article_content, 'html.parser', from_encoding='utf8')
    node = soup.find(id="js_content")
    write_text_to_file(title, node)


def write_text_to_file(title, node):
    contents = node.descendants
    for item in contents:
        if isinstance(item, NavigableString):
            with open(title, "a", encoding="utf-8") as f:
                f.write(str(item))
                f.write('\n\n')

def handle_node(node):
    if node.span:
        node = node.span
        handle_node(node)


def extract_data(html_content):
    rex = "msgList = '({.*?})'"
    pattern = re.compile(pattern=rex, flags=re.S)
    match = pattern.search(html_content)
    if match:
        data = match.group(1)
        data = html.unescape(data)
        data = json.loads(data)
        articles = data.get("list")
        articles_lists = dict()
        for item in articles:
            if item.get("app_msg_ext_info"):
                articles_lists[item["app_msg_ext_info"]["title"]] = item["app_msg_ext_info"]["content_url"]
        return articles_lists

'''
def crawl_msg(offset=0):
  url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5MjA5MTQyMA==&f=json&offset=10&count=10&is_ok=1&scene=126&uin=777&key=777&pass_ticket=aGWzzp8%2Bzyir2DKPLDnrceAi21LIqICuCOJi4d46Qnc3H4YWQtybMQQwha0k6Vv5&wxtoken=&appmsg_token=972_n5E2DXr9N7hz2L7mihnSAbe3THf2Ra_lMfZC0w~~&x5=0&f=json'
  headers ={
      'Host': 'mp.weixin.qq.com',
      'Accept-Encoding': 'br, gzip, deflate',
      'Cookie': 'devicetype=iOS11.4.1; lang=en; pass_ticket=aGWzzp8+zyir2DKPLDnrceAi21LIqICuCOJi4d46Qnc3H4YWQtybMQQwha0k6Vv5; version=16070227; wap_sid2=CI/I96QLElxDOFV3dTNUeElBNXNpVG1pMENGekM5NTVLLW9VR2N6SDVZUl9IVjdMOGlJb2h1ZlNnRHE3Xy1yVnlUb1dOSzNqUXI4UElxTm1VdDJYcnF2YUx5U2Q1Y3dEQUFBfjCZ2KjcBTgNQJVO; wxuin=3030246415; wxtokenkey=777; rewardsn=; pgv_pvid=7650693240',
      'Connection': 'keep-alive',
      'Accept': '*/*',
      'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77 MicroMessenger/6.7.2 NetType/WIFI Language/en',
      'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MjA5MTQyMA==&scene=126&devicetype=iOS11.4.1&version=16070227&lang=en&nettype=WIFI&a8scene=0&fontScale=94&pass_ticket=aGWzzp8%2Bzyir2DKPLDnrceAi21LIqICuCOJi4d46Qnc3H4YWQtybMQQwha0k6Vv5&wx_header=1',
      'Accept-Language': 'en-us',
  }
  response = requests.get(url, headers=headers,verify=False)
  if '<title>验证</title>' in response.text:
      raise Exception("获取微信公众号文章失败，可能是因为你的请求参数有误，请重新获取")
  result = response.json()
  if result.get("ret") == 0:
      msg_list = result.get("general_msg_list")
      data = json.loads(msg_list)
      articles = data.get("list")
      articles_lists = dict()
      for item in articles:
          if item.get("app_msg_ext_info"):
              articles_lists[item["app_msg_ext_info"]["title"]] = item["app_msg_ext_info"]["content_url"]
      rex = r'\\/'
      for item in articles_lists:
          pattern = re.sub(rex, '/', html.unescape(articles_lists.get(item)))
          response = requests.get(pattern, headers=headers, verify=False)
          parser_text_to_file(item, response.text)
      print("抓取数据: offset=%s, data=%s" % (offset, msg_list))
      has_next = result.get("can_msg_continue")
      if has_next == 1:
          next_offset = result.get("next_offset")
          time.sleep(2)
          crawl_msg(next_offset)
  else:
      print("无法正确获取内容，请重新从Fiddler/Charles获取请求参数和请求头")
      exit()
'''

if __name__ == '__main__':
    urllib3.disable_warnings()
    #crawl_msg(84)
    crawl()
