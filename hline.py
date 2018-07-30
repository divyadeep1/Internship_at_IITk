import os
from PIL import Image
import cv2 as cv
import numpy as np
import random as rn
import math as m
import json
import weightsnew   
def find_dis(a,b,c,d):
    global ebs
    x=min([abs(a-c),abs(a-d),abs(b-c),abs(b-d)])
    if(x<ebs):
        return 1
    else:
        return 0
    
def hline():   
    
    path = './Input_images/'
    # Store the image file names in a list as long as they are jpgs
    images = [f for f in os.listdir(path) if os.path.splitext(f)[-1] == '.png']
    for i in images:
        img = cv.imread(path+i,0)
        #img=cv.imread('ti55.png',0)
       # img = cv.Canny(img,250,250,apertureSize = 7)
        #cv.imwrite('canny_of_image_used.jpg',img)
        _,img=cv.threshold(img,223,255,cv.THRESH_BINARY)
        print(i)
        global ebs
        ebs=3
        ct1=0
        res=[]
        lines = None
        label=0
        sample=15
        rpt=10
        c_thresh=13
        while lines is None :

            #lines = cv.HoughLinesP(img,int(r),theta,int(thresh),minLineLength=int(min_l_l),maxLineGap=int(mlg))
            #print("no")
            ct1+=1
            if(ct1==20):
                break;
            lines = cv.HoughLinesP(img, .1,.001,10,minLineLength=10,maxLineGap=10)
            #lines = cv.HoughLinesP(img, 1,m.pi/180,50,minLineLength=50,maxLineGap=10)
             
            #lines = cv.HoughLines(img,.1,0.01,49)
        
            
        
        img = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
        img=np.zeros((553,828,3), np.uint8)
        for line in lines:
            x1,y1,x2,y2 = line[0]
            cv.line(img,(int(x1),int(y1)),(int(x2),int(y2)),(0,255,0),1)
        cv.imwrite('./hough_line_output/'+i,img)
        print("image ready in 4")
            
            
        if(ct1<20):
            print(len(lines))
##            img = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
            img=np.zeros((553,828,3), np.uint8)
            for line in lines:
               flag=1
               x1,y1,x2,y2 = line[0]
               if(res!=[]):
                   for _ in range(rpt):
                        
                        for k in res:
                            if(k[1]==k[2]):
                                for t in range(sample):
                                    if((((x1+t)==k[1] and (x2+t)==k[2])or((x1-t)==k[1] and (x2-t)==k[2]))):
                                        chk=find_dis(y1,y2,k[3],k[4])

                                       # print('changed x')
                                        if(chk==1):
                                            x1,x2=k[1],k[2]
                                            break
                        for k in res:
                            if(k[3]==k[4]):
                                for t in range(sample):
                                    if((((y1+t)==k[3] and (y2+t)==k[4])or((y1-t)==k[3] and (y2-t)==k[4]))):
                                        chk=find_dis(x1,x2,k[1],k[2])
##                                        print('changed y')
                                        if(chk==1):
                                             y1,y2=k[3],k[4]
                                             break
                    
                        for k in res:                
                                if(k[1]!=k[2] and k[3]!=k[4] and x1!=x2 and y1!=y2):
                                    for t in range(sample):
                                        slope1=(y2-y1)/(x2-x1)
                                        slope2=(k[4]-k[3])/(k[2]-k[1])
                                        if(slope1==slope2):
                                            #print("yes")
                                            c1=y1-slope1*x1
                                            c2=k[3]-slope2*k[1]
                                            c=abs(c1-c2)
                                            #chk=find_dis(y1,y2,k[3],k[4])
                                            if(c<c_thresh):
                                                if((y1-slope2*x1-c2)<0):
                                                    y1,y2=y1+c,y2+c
                                                else:
                                                    y1,y2=y1-c,y2-c      
                        for k in res:
                            if(k[1]==x1 and k[2]==x2 and k[3]==y1 and k[4]==y2):
                                flag=0
               if(flag==1):          
                   res.append((label,int(x1),int(x2),int(y1),int(y2),0.1))
                   label+=1
                   cv.line(img,(int(x1),int(y1)),(int(x2),int(y2)),(0,255,0),1)
            print(len(res))    
            
            cv.imwrite('./hough_line_output_snapped/'+i,img)
            print("image ready in 5")
           
            with open('wts.json', 'w') as outfile:
                     json.dump(res, outfile)
                     
            weightsnew.weights(i)




                        

                                            
        
