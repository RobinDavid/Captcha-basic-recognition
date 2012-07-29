import urllib
import re
from HTMLParser import HTMLParser
from StringIO import StringIO
from PIL import Image
import cv2.cv as cv
import os

class Captcha_Downloader():

    class MyHTMLParser(HTMLParser):
    #This parser will try to find the given pattern an return the captcha url
        def __init__(self,pattern):
            HTMLParser.__init__(self) 
            self.image_url = None
            self.pattern =pattern
            
        def handle_starttag(self, tag, attrs):
            if tag == "img":
                for attr in attrs:
                    if attr[0] == "src":
                        if re.search(self.pattern, attr[1]):
                            self.image_url = attr[1]
        
        def getLink(self):
            return self.image_url
    
    def __init__(self, url, pattern, encoding=None):
        self.url = url
        self.encoding = encoding
        self.parser = self.MyHTMLParser(pattern)
        self.image_url = None
        self.imagestr = None
        self.image= None
        
    def run(self):
        f = urllib.urlopen(self.url) #Open registration form
        if self.encoding is None:
            txt = f.read()#get page
        else:
            txt = f.read().decode(self.encoding)
        
        self.parser.feed(txt) #Parse HTML to get image url
        
        self.image_url = self.parser.getLink()

        f = urllib.urlopen(self.image_url) #Open image url
        self.imagestr = f.read() #Read it
        
        
        self.string_to_iplimage(self.imagestr)#Convert image
        
        
    def string_to_iplimage(self, im):
    #Convert the image return by urllib into an OpenCV image
        pilim = StringIO(im)
        source = Image.open(pilim).convert("RGB")
        
        self.image = cv.CreateImageHeader(source.size, cv.IPL_DEPTH_8U, 3)
        cv.SetData(self.image, source.tostring())
        cv.CvtColor(self.image, self.image, cv.CV_RGB2BGR)
    
    def getImage(self):
        return self.image
    
    
def setup_Benchtest(dir, url, pattern, encoding=None):#Create a folder with multiples images
    if os.path.exists(dir):
        for file in os.listdir(dir): #Remove all files of the dir if there's any
            os.remove(os.path.join(dir,file))
        os.removedirs(dir)
    os.mkdir(dir)
    dl = Captcha_Downloader(url, pattern, encoding) #Create the downloader once
    for i in range(20): #Download 20 image
        dl.run()
        im = dl.getImage()
        cv.SaveImage(os.path.join(dir,dir+str(i)+".png"), im)
