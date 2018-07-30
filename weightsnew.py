import os
import random
import numpy as np
import cv2 as cv
import math as m
import random as rn
import json
import check as ch


def load_data():
    
    with open('wts.json') as json_file:
        data = json.load(json_file)
        return data

    
def write_data(data,i):
    i=i.split("/")
    i=i[-1]
    i=i.split(".")
    
    with open('./json/'+i[0]+'.json','w') as json_file:
        json.dump(data,json_file)
    print(" final json file with weights ready\n")
    print(".............................\n")

        

def bnd(data,inc_r,thresh_wt,img,sample,dis_value):
    global check
    global chk
    global check1
    global check2
    global check3
    ymax,xmax=img.shape
    avg=[]
    f=inc_r

    _,x1,x2,y1,y2,w=data
    p0=np.array([y1,x1])
    p1=np.array([y2,x2])
    m=(p0-p1)/np.linalg.norm(p0-p1)
    r_cap=np.array([-m[1],m[0]])

    for i in range(sample):
     
        inc_r=f
        alpha=rn.uniform(0,1)
        p=alpha*p0 + (1-alpha)*p1
        pv1=p_value(p,img)

        while True: 
            pc=p+(r_cap*inc_r)

            if(pc[0]<0 or pc[1]<0 or pc[0]+1>=ymax or pc[1]+1>=xmax):#if the point is beyond image size
                dis1=dis_value
                check1.append((p[0],p[1],r_cap[0],r_cap[1]))
                check2.append((pc[0],pc[1],r_cap[0],r_cap[1]))
                break 
            pv2=p_value(pc,img)
            if(pv2==0):
                dis1=0
                break
            if(abs(pv2-pv1)>thresh_wt):
                dis1=np.linalg.norm(p-pc)
                if(dis1>chk):
                    check.append((p[0],p[1],r_cap[0],r_cap[1]))
                    check3.append((pc[0],pc[1],r_cap[0],r_cap[1]))
                break
            else:
                inc_r+=f
      
        inc_r=f
        while True:
            
            pc=p+((-r_cap)*inc_r)
            if(pc[0]<0 or pc[1]<0 or pc[0]+1>=ymax or pc[1]+1>=xmax):#if the point is beyond image size
                dis=dis_value
                avg.append(dis1+dis)
                check1.append((p[0],p[1],-r_cap[0],-r_cap[1]))
                check2.append((pc[0],pc[1],-r_cap[0],-r_cap[1]))
                break
            
            pv2=p_value(pc,img)
            if(pv2==0):
                dis=np.linalg.norm(p-pc)
                avg.append(dis1+dis)
                break
                
            if(abs(pv2-pv1)>thresh_wt):
                dis=np.linalg.norm(p-pc)
                avg.append(dis1+dis)
                if(dis>chk):
                    check.append((p[0],p[1],-r_cap[0],-r_cap[1]))
                    check3.append((pc[0],pc[1],r_cap[0],r_cap[1]))

                
                break
            else:
                inc_r+=f

                
    std=np.std(avg)
    mean=sum(avg)/len(avg)
    av=[]
    for i in avg:
        if (i>=(mean-2*std) and i<=(mean+2*std)):
            av.append(i)

   
    if(len(av)>0):

        result=(sum(av)/len(av))

        if((sum(av)/len(av))>17):
            result=3
            
        data[5]=result/2
        return data
    else:
        data[5]=dis_value/2
        return data
        



def p_value(p,img):
 
    y,x=p[0],p[1]
    
    p0=np.floor(p)
    p0=p0.astype(int)

    dp=p-p0

    dp1=np.ceil(dp)
    
    dp1=dp1.astype(int)
    
    p00=p0
    p01=p0+(np.array([0,1])*dp1)
    p10=p0+(np.array([1,0])*dp1)
    p11=p0+dp1

    
    v = np.array([img[p00[0],p00[1]], img[p01[0],p01[1]], img[p10[0],p10[1]],img[p11[0],p11[1]]])
    
    
    dy, dx = dp

    f_00 = dy * dx
    f_01 = dy * (1 - dx)
    f_10 = (1 - dy) * dx
    f_11 = (1 - dy) * (1 - dx)
    f = np.array([ f_11, f_10, f_01, f_00])
    return(np.dot(v,f))


def weights(image_name,
            increment_r=.5,
            pixel_thresh=0.3,
            samples=5,
            default_val=3,
            ck=15):
    
    print("calculating weight")
    global count1
    global count2
    global check
    global check1
    global check2
    global check3
    global chk
    chk=ck
    count2=0
    count1=0
    check,check1,check2,check3=[],[],[],[]
    img = cv.imread(image_name,0)
    _,img=cv.threshold(img,223,255,cv.THRESH_BINARY)
    data=load_data()

    new_data=[]
    img1=np.zeros((551,828,3), np.uint8)
    
    for i in data:
        x=bnd(i,inc_r=increment_r,thresh_wt=pixel_thresh,img=img,sample=samples,dis_value=default_val)
        new_data.append(x)
        cv.line(img1,(int(i[1]),int(i[3])),(int(i[2]),int(i[4])),(255,255,0),1)
    k=image_name    
    k=k.split("/")
    k=k[-1]
    k=k.split(".")
    
    cv.imwrite('./images/'+k[0]+'3.png',img1)
    with open('check_data.json','w') as json_file:
        json.dump(check,json_file)
    with open('check1_data.json','w') as json_file:
        json.dump(check1,json_file)
    with open('check2_data.json','w') as json_file:
        json.dump(check2,json_file)
    with open('check3_data.json','w') as json_file:
        json.dump(check3,json_file)    
    write_data(new_data,image_name)
    ch.check1(image_name)

