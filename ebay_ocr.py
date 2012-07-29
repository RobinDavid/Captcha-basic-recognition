
import urllib
import re
from HTMLParser import HTMLParser
import pytesser
from StringIO import StringIO
from PIL import Image
import cv2.cv as cv
import os
from captcha_downloader import setup_Benchtest
from generic_ocr_operations import *

def crack(tocrack,withContourImage=False):
    #Function that intent to release all characters on the image so that the ocr can detect them
    
    #We just apply 4 filters but with multiples rounds
    resized = resizeImage(tocrack, (tocrack.width*6, tocrack.height*6))
    dilateImage(resized, 4)
    erodeImage(resized, 4)
    thresholdImage(resized, 200, cv.CV_THRESH_BINARY)
    
    if withContourImage: #If we want the image made only with contours
        contours = getContours(resized, 5)
        contourimage = cv.CreateImage(cv.GetSize(resized), 8, 3)
        cv.Zero(contourimage)
        cv.DrawContours(contourimage, contours, cv.Scalar(255), cv.Scalar(255), 2, cv.CV_FILLED)    
        
        contourimage = resizeImage(contourimage, cv.GetSize(tocrack))
        resized = resizeImage(resized, cv.GetSize(tocrack))
        return resized, contourimage
    
    resized = resizeImage(resized, cv.GetSize(tocrack))
    return resized
        
        
def process_all(results):
    dir = "Ebay" #Consider that all images are stored in the dir 'Ebay'
    for file,r in zip(os.listdir(dir),results):
        im = cv.LoadImage(os.path.join(dir,file),cv.CV_LOAD_IMAGE_GRAYSCALE) #Load the image
        im = crack(im) #intent to crack it
        res = pytesser.iplimage_to_string(im,psm=pytesser.PSM_SINGLE_WORD) #Do characters recognition
        res = res[:-2] #Remove the two \n\n always put at the end of the result
        if res == r: #Compare the result of the value contained in our list
            print file+": "+res+" | "+r+ " OK"
        else:
            print file+": "+res+" | "+r+" NO"
        
   
if __name__=="__main__":
    
    #Execute the following once to setup the envirronement
    '''
    dir = "Ebay"
    url = "https://scgi.ebay.fr/ws/eBayISAPI.dll?FetchCaptchaToken&parentPage=RegisterEnterInfo&tokenString=5WWZNQcAAAA%3D&ej2child=true"
    pattern = "LoadBotImage"
    setup_Benchtest(dir, url, pattern)
    '''
    
    #The list contains to got results for my bench
    results=["139866","400961","387740","431418","750113","572574","155885","440543","826316","233388","840189","349093","751181","270699","356535","743987","467643","342527","992978","879970",""]
    process_all(results) #Process all the images