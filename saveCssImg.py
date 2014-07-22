# coding: utf-8 -*-

import urllib2,urllib
import sys,re,os,urlparse

class saveCssBackImg():
    def __init__(self,cssUrl,savePath,outInfo):

        self.cssUrl = cssUrl
        self.outInfo = outInfo
        self.savePath = mkdir(savePath)
        
    def saveImg(self):
        counter = 1
        errnum = 0
        imgList = self.getImgList()
        img_num = len(imgList)

        for img in imgList:  
            img = img.strip("'")
            img = img.strip('"')
            
            if re.match('^https?://', img):
                imgsrc = img.split('?')[0]
            else:
                imgsrc = urlparse.urljoin(self.cssUrl, img).split('?')[0]

            imgname = os.path.split(imgsrc)[1]
            try:  
              httpcode = urllib.urlopen(imgsrc).code  
            except:
              httpcode = None         

            if httpcode == 200 :
                try: 
                    urllib.urlretrieve(imgsrc, os.path.join(self.savePath,imgname))
                    info = u'[%2d/%2d]<a href="%s">%s</a>' %( counter, img_num , imgsrc,imgsrc  )
                except:
                    errnum += 1
                    info =  u'[%2d/%2d]<a href="%s">%s</a> <span style="color:red">保存失败[%s]</span>' %( counter, img_num , imgsrc ,imgsrc,errnum)
            else:
                 errnum += 1
                 info =  u'[%2d/%2d]<a href="%s">%s</a> <span style="color:red">[%s][code:%s]</span>' %( counter, img_num , imgsrc ,imgsrc ,errnum, httpcode)

            self.outInfo(info)   
            counter+=1 
        totalInfo = (img_num,errnum)
        self.outInfo(totalInfo) 

    def getImgList(self):
        allimglist = re.findall(r'url\s*\((.*?)\)', self.getCssContent())  
        imgList = set(allimglist)
        return imgList

    def getCssContent(self) :
        try:
            rsp = urllib2.urlopen(self.cssUrl,timeout = 1) 
            return rsp.read()
        except urllib2.URLError, e: 
          self.outInfo('<font color=red>%s</font>' % e )
          
        except BaseException, e:
          self.outInfo('<font color=red>%s</font>' % e )       


def mkdir(savePath):
    fullPath = os.path.join(os.getcwd(),savePath)
    if not os.path.exists(fullPath) :
      try:
        os.mkdir(os.path.join(os.getcwd(),savePath))
        return fullPath
      except:
        print 'can\'t creat dir: %s, please creat it manually! '  % fullPath
        return
    return fullPath