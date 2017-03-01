#-*-coding=utf-8-*-
__author__ = 'xda'
import requests,re
from lxml import etree

class getBBSContent():

    def __init__(self):
        self.header={'Host':'bbs.sysu.edu.cn',
                     'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36',
                     }


    def getContent(self,board):
        base_url='http://bbs.sysu.edu.cn/bbstdoc?board='
        url=base_url + board
        text=requests.get(url,headers=self.header).text
        links_p=re.compile('<td class="td6"><a href=bbstcon\?board=(.*?)>')
        result=links_p.findall(text)
        #url+result[0]...
        for i in result:
            each_page_link=base_url+i
            content=requests.get(each_page_link,headers=self.header).text
            html=etree.HTML(content)
            title=html.xpath('//title/text()')
            print title[0]






if __name__=='__main__':
    obj=getBBSContent()
    obj.getContent('Memory')