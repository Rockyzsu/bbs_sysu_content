#-*-coding=utf-8-*-
__author__ = 'xda'
#用法: 在同一个目录下，创建一个board.txt的文件，文件写入你想下载的版块的英文，比如每日一笑是Joke, 时光流转是Memory, 每写一个换一行
import requests,re,time,sys,chardet,codecs,urllib2,os
from lxml import etree
from toolkit import Toolkit
reload(sys)
sys.setdefaultencoding('gbk')
class getBBSContent():

    def __init__(self):
        self.header={'Host':'bbs.sysu.edu.cn',
                     'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36',
                     }


    def getContent(self,text,folder):

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
            try:
                print title
            except:
                print "Can't decode title, return"
                return 0
            filename=re.sub(u' - 逸仙时空BBS','',title)
            filename=Toolkit.filename_filter(filename)
            f_fullpath=os.path.join(folder,filename)
            try:
                Toolkit.save2filecn(f_fullpath,title)
                Toolkit.save2filecn(f_fullpath,'\n\n*******************\n\n')
                Toolkit.save2filecn(f_fullpath,each_page_link)
                Toolkit.save2filecn(f_fullpath,'\n\n*******************\n\n')
            except:
                print each_page_link
                print "Create file error, go to next article"
                return 0
            detail=html.xpath('//td[@class="border content2"]')
            #print detail
            for i in detail:
                #print type(i)
                Toolkit.save2filecn(f_fullpath, i.xpath('string(.)'))
                #print i.xpath('string(.)')

            #f = open('log.txt','w')
            #f = codecs.open(filename,'w',encod)
            #f.write(t)
            #f.close()
            #print t
            #Toolkit.save2filezn("log",t)

            time.sleep(5)


    def getLoop(self,board,folder):
        print "Board: ", board
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
            self.getContent(text_,folder)
            ii=ii+20
            print ii

        #&start=

if __name__=='__main__':
    obj=getBBSContent()
    data=Toolkit.readConfig('board.txt')
    for i in data:
        sub_folder = os.path.join(os.getcwd(), i)
        if os.path.exists(sub_folder)==False:
            os.mkdir(sub_folder)
        obj.getLoop(i,sub_folder)