
import pytesser
import os
import cv2.cv as cv
from generic_ocr_operations import *

class ProbabilisticCracker():

    def __init__(self, im):
        self.image = im
        self.values = [{},{},{},{},{},{}] #Will hold occurrence of characters
        self.ocrvalue = "" #Final value
      
    def getValue(self):
        return self.ocrvalue #Return the final value
      
    def crack(self,dilateiter=4, erodeiter=4, threshold=200, size=(155,55)): #Take all parameters
        resized = resizeImage(self.image, (self.image.width*6, self.image.height*6))
    
        dilateImage(resized, dilateiter)
        erodeImage(resized, erodeiter)
        thresholdImage(resized,threshold, cv.CV_THRESH_BINARY)
        
        resized = resizeImage(resized, size)
        
        #Call the tesseract engine
        ret = pytesser.iplimage_to_string(resized)
        ret = ret[:-2]
        return ret
    
    def run(self): #Main method
        w = self.image.width
        h = self.image.height
        
        for dilate in [1,3,4,5]:
            for erode in [1,3,4,5]:
                for thresh in [125,150,175,200]:
                    for size in [(int(w*0.5),int(h*0.5)),(w,h),(w*2,h*2),(w*3,h*3)]:
                        val = self.crack(dilate, erode, thresh, size) #Call crack successively all parameters
                        #print "Val:",val
                        self.accumulateChars(val) #Call accumulate
        self.postAnalysis()
                        
    def accumulateChars(self,val):
        l = len(val)
        for i in range(6): #Only iterate the 6 first chars
            if i > l-1: #Break the length of the string lower
                break
            c = val[i]
            if c.isdigit(): #Put the char only if this is a digit
                if self.values[i].has_key(c):
                    self.values[i][c] += 1 #Add 1 if the entry character already exists
                else:
                    self.values[i][c] = 1
    
    def postAnalysis(self): #Analyse at the end
        for vals in self.values:#For every dictionnary
            c, v = self.max(vals) #Take the most occuring
            #print "Max:", c,v
            self.ocrvalue += c #Append it to the final string
            
    def max(self, d):
        m = 0
        elt = ''
        for k,v in d.items():
            if v > m:
                m = v
                elt = k
        return elt, m


def process_all(results):
    dir = "Ebay"
    for file,r in zip(os.listdir(dir),results): #For every file in the directory
        im = cv.LoadImage(os.path.join(dir,file),cv.CV_LOAD_IMAGE_GRAYSCALE) #Open the file
        cracker = ProbabilisticCracker(im) #Instantiate the ProbabilistricCracker
        cracker.run() #Run it
        res = cracker.getValue() #Take the final value
        
        if res == r: #Compare it with the right one
            print file+": "+res+" | "+r+ " OK"
        else:
            print file+": "+res+" | "+r+" NO"
        nb=6
        count = 0
        for c1,c2 in zip(res,r): #Make a char/char comparison to compute the accuracy
            if c1 == c2:
                count +=1
        print "Avg: ", (count*100)/nb, "%"
        

if __name__=="__main__":

    results=["139866","400961","387740","431418","750113","572574","155885","440543","826316","233388","840189","349093","751181","270699","356535","743987","467643","342527","992978","879970",""]
    process_all(results)
