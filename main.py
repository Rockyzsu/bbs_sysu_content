#-*-coding=utf-8-*-
__author__ = 'xda'
import requests,re,time,sys,chardet,codecs,urllib2
from lxml import etree
from toolkit import Toolkit
reload(sys)
sys.setdefaultencoding('gbk')
class getBBSContent():

    def __init__(self):
        self.header={'Host':'bbs.sysu.edu.cn',
                     'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36',
                     }


    def getContent(self,text):

        links_p=re.compile('<td class="td6"><a href=bbstcon\?board=(.*?)>')
        result=links_p.findall(text)
        url_board='http://bbs.sysu.edu.cn/bbstcon?board='
        #url+result[0]...
        for i in result:
            each_page_link=url_board+i
            print each_page_link
            content=requests.get(each_page_link,headers=self.header)
            content.encoding='gbk'
            s= content.text
            #req=urllib2.Request(each_page_link,headers=self.header)
            #resp=urllib2.urlopen(req).read()
            #c=content.decode('utf-8')
            #c=content
            #print c
            #print type(s)
            #print resp.decode('gbk')
            html=etree.HTML(s)
            #print content.decode('gbk')
            #t= chardet.detect(content)
            #print content['encoding']
            title=html.xpath('//title/text()')[0]
            #t=title[0].decode('gbk').encode('utf-8')
            #t= title[0].decode('gbk')
            #t= unicode(title[0],'gbk')
            print title
            filename=re.sub(u' - 逸仙时空BBS','',title)
            filename=Toolkit.filename_filter(filename)
            Toolkit.save2filecn(filename,title)
            Toolkit.save2filecn(filename,'\n\n*******************\n\n')
            detail=html.xpath('//td[@class="border content2"]')
            #print detail
            for i in detail:
                #print type(i)
                Toolkit.save2filecn(filename, i.xpath('string(.)'))
                #print i.xpath('string(.)')

            #f = open('log.txt','w')
            #f = codecs.open(filename,'w',encod)
            #f.write(t)
            #f.close()
            #print t
            #Toolkit.save2filezn("log",t)

            time.sleep(20)


    def getLoop(self,board):
        base_url='http://bbs.sysu.edu.cn/bbstdoc?board='
        url=base_url + board
        resp=requests.get(url,headers=self.header)
        resp.encoding='gbk'
        text=resp.text
        tree=etree.HTML(text)
        page=tree.xpath('//div[@id="footer"]/ul/li/b/text()')
        all_count= int(page[3])
        print all_count
        ii=1
        while ii <all_count+20:
            go_url=url+'&start='+str(ii)
            print go_url
            resp_=requests.get(go_url,headers=self.header)
            resp_.encoding='gbk'
            text_=resp_.text
            self.getContent(text_)
            ii=ii+20

        #&start=

if __name__=='__main__':
    obj=getBBSContent()
    obj.getLoop('Memory')