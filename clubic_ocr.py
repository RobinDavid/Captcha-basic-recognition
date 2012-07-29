'''
Created on 20 juil. 2012

@author: robin
'''
import urllib
import re
from HTMLParser import HTMLParser
import pytesser
from StringIO import StringIO
from PIL import Image
import cv2.cv as cv
import os
from captcha_downloader import setup_Benchtest

def crack(tocrack):
    im = cv.CreateImage(cv.GetSize(tocrack), 8, 1)
    cv.Split(tocrack, None, None, im, None)
    cv.Threshold(im, im, 250, 255, cv.CV_THRESH_BINARY)

    txt = pytesser.iplimage_to_string(im)
    return txt[:-2]
     
def process_all(results):
    dir = "Clubic"
    for file,r in zip(os.listdir(dir),results):
        im = cv.LoadImage(os.path.join(dir,file))
        res = crack(im)
        if res == r:
            print file+": "+res+" | "+r+ " OK"
        else:
            print file+": "+res+" | "+r+" NO"

if __name__ == "__main__":
    #setup_Benchtest()
    '''
    dir = "Clubic"
    url = 'http://www.clubic.com/api/creer_un_compte.php'
    pattern = "captcha"
    setup_Benchtest(dir, url, pattern,"latin-1")
    #process_all()
    '''
    results = ["368477","857905","666330","523840","295697","257174","661445","816945","232698","991634","425734","204318","230742","478796","597656","879755","774292","299738","130276","426116"]
    process_all(results)
    '''
    dl = Clubic_Captcha_Downloader()
    dl.run()
    im = dl.getImage()
    print crack(im)
    
    cv.ShowImage("Image", im)
    cv.WaitKey(0)
    '''