import json
import cv2 as cv

def check1(im_name):
    with open('check_data.json') as json_file:
        check = json.load(json_file)
                          
    with open('check1_data.json') as json_file:
        check1 = json.load(json_file)
    with open('check2_data.json') as json_file:
        check2 = json.load(json_file)
    with open('check3_data.json') as json_file:
        check3 = json.load(json_file)


    img=cv.imread(im_name)
    for  y,x,_,_ in check:
        cv.circle(img,(int(x),int(y)), 2, (0,0,255), 2)
    for  y,x,_,_ in check3:
        cv.circle(img,(int(x),int(y)), 2, (255,0,0), 2)
        
    for  y,x,_,_ in check1:
        cv.circle(img,(int(x),int(y)), 2, (0,255,0), 2)
    for  y,x,_,_ in check2:
        cv.circle(img,(int(x),int(y)), 2, (0,255,255), 2)    
    i=im_name
    i=i.split("/")
    i=i[-1]
    i=i.split(".")    
    cv.imwrite('./images/'+i[0]+'4.png',img)                      
