import os
from PIL import Image
import cv2 as cv
import numpy as np
import random as rn
import math as m
import json
import weightsnew 




def write_data(data):
    with open('wts.json','w') as json_file:
        json.dump(data,json_file)


        
def calculate_points(i,bcm,idx):
     global points
     global lbl
     r_cap,r_mod,l_cap=bcm[idx]
     for k in i:
          pt=r_cap*r_mod+k[0]*l_cap
          pt1=r_cap*r_mod+k[1]*l_cap
          points.append((lbl,pt[0],pt1[0],pt[1],pt1[1],0.1))
     
     
     
def alpha_partition(i):
     vis1=np.full((1000,),1)
     alpha_part=[]
     for ind,val in enumerate(i):
          if(vis1[ind]!=0):
               flag=1
               vis[ind]=0
               alpha1=val[0]
               alpha2=val[1]
               c1=max(alpha1,alpha2)
               c1_dash=min(alpha1,alpha2)
               while(flag==1):
                    flag=0
                    for k,a in enumerate(i):
                         c2=min(a[0],a[1])
                         c2_dash=max(a[0],a[1])
                         if(vis1[k]!=0 and not((c1<c2) or (c1_dash>c2_dash))):###############to be done in O(n)
                              alpha1=max(alpha1,alpha2,a[0],a[1])
                              alpha2=min(alpha1,alpha2,a[0],a[1])
                              c1=max(alpha1,alpha2)
                              c1_dash=min(alpha1,alpha2)
                              vis1[k]=0
                              flag=1
                              
                         
                    
               alpha_part.append((alpha1,alpha2))
               
               
     return alpha_part          
          

          
     
def find_line_para(i):

     p0=np.array([i[1],i[3]])#x1,y1
     p1=np.array([i[2],i[4]])#x2,y2

   
     l_cap=(p0-p1)/np.linalg.norm(p0-p1)

     
     r_cap=np.array([-l_cap[1],l_cap[0]])
     if(r_cap[0]<0):
          r_cap=-r_cap
     r_mod=np.dot(p0,r_cap)
     return r_mod,r_cap,l_cap


def calculate_bin_para(i):
    sum1=0
    sum2=0
    sum3=0
    for j in i:
        p0=np.array([j[0],j[2]])#(i[1],i[2],i[3],i[4],r_mod,r_cap,l_cap)
        p1=np.array([j[1],j[3]])
        l=np.linalg.norm(p0-p1)
        dt=j[5]*l
        mod_r=np.dot((p0+p1),dt)
        sum1+=dt
        sum2+=l
        sum3+=mod_r
    return sum1/sum2,sum3/(2*sum2)


       
def misplacement_check(i,k):

    mx,mn=max(i[1],i[2]),min(i[1],i[2])
    mx_dash,mn_dash=max(k[1],k[2]),min(k[1],k[2])
    if(mx!=mn):
        if(not(mn_dash>=mx or mx_dash<=mn)):
            return 1
        else:
            return 0
    else:
          mx,mn=max(i[3],i[4]),min(i[3],i[4])
          mx_dash,mn_dash=max(k[3],k[4]),min(k[3],k[4])
          if(not(mn_dash>=mx or mx_dash<=mn)):
              return 1
          else:   
              return 0

def length(k):
    p1=np.array([k[1],k[3]])
    p2=np.array([k[2],k[4]])
    return np.linalg.norm(p1-p2)
     
def calculate_alpha(rc,v,r,lcap):
    global ebsilon 
    a=(r-v)
    b=np.dot(a,rc)
    b=b*rc
    c=v+b
    d=(c-r)
    if(abs(lcap[0])>ebsilon):
         alpha=d[0]/lcap[0]
    else:
         alpha=d[1]/lcap[1]
    return alpha  
    
    

    
def find_alphas(i,bcm,index):
    alpha=[]
    r_cap,r_mod,l_cap=bcm[index]
    for j in i:
        p0=np.array([j[0],j[2]])
        p1=np.array([j[1],j[3]])
        r_vec=r_mod *r_cap
        alpha1=calculate_alpha(r_cap,p0,r_vec,l_cap)
        alpha2=calculate_alpha(r_cap,p1,r_vec,l_cap)
        alpha.append((alpha1,alpha2))
        
    return alpha    
        
        


        
############################################################################################################################









################################ main ################################
        
if __name__== "__main__":

    global ebsilon
    global lbl
    global delta


    ############ parameters for tweking #######################
    delta=10
    thresh_bin=10
    range_thresh=0.05
    r_granularity=0.1
    theta_granularity=0.001
    threshold=10
    minLineLength=10
    maxLineGap=10
    extension='.png'


    ########## weight calculation parameters #######################
    increment_r=.5
    pixel_thresh=0.3
    samples=5
    default_val=3
    chk=15

    
    ############################################################


    

    path = './box_thresh/'
    # Store the image file names in a list as long as they are jpgs
    images = [f for f in os.listdir(path) if os.path.splitext(f)[-1] == extension]
    for i in images:
    
        
        lines=None
        label=0
        lbl=0
        lpc=0
        bn,res=[],[]
        image_name=path+i
        img = cv.imread(image_name,0)
        img2=cv.imread(image_name)
        _,img=cv.threshold(img,223,255,cv.THRESH_BINARY)
        
        ebsilon=0.1
     
        
        
        
        vis=np.full((1000,),1)

        while lines is None:
            lines = cv.HoughLinesP(img,r_granularity,theta_granularity,threshold,minLineLength,maxLineGap)
            lpc+=1
            if(lpc>15):
                break
        

        
    ##data formation    
        if(lpc<15):
            print("no of lines generated in houghline: %d"%len(lines))
            img1=np.zeros((551,828,3), np.uint8)
            for line in lines:
                 x1,y1,x2,y2 = line[0]
                 res.append((label,x1,x2,y1,y2,0.1))
                 label+=1
                 cv.line(img1,(int(x1),int(y1)),(int(x2),int(y2)),(0,255,0),1) 
            i=i.split(".")
            im_name=i[0]
            print("image  name : %s"%im_name)
            cv.imwrite('./images/'+im_name+'1.png',img1)

                 
        ##bin creation       
            for j,i in enumerate(res):
                    temp=[]
                    
                    if(vis[j]==1):
                        vis[j]=0
                        r_mod,r_cap,l_cap=find_line_para(i)
                        l=[]
                        flag=0
                        temp.append((i[1],i[2],i[3],i[4],r_mod,r_cap,l_cap))###############to be done in O(n)
                        while(flag==0):
                            flag=1
                            for m,k in enumerate(res):
                                if(vis[m]!=0):
                                    r_dash_mod,r_dash_cap,l_dash_cap=find_line_para(k)
                                    if((abs(r_mod-r_dash_mod)<thresh_bin) and (np.linalg.norm(r_cap-r_dash_cap)<range_thresh) and (misplacement_check(i,k))):
                                        vis[m]=0
                                        flag=0
                                        temp.append((k[1],k[2],k[3],k[4],r_dash_mod,r_dash_cap,l_dash_cap))
                                        if(length(k)>length(i)):
                                            i=k
                                            
                                    
                        bn.append(temp)

        ##parameters of bin                
            bn_cap_mod=[]                        
            for i in bn:
                bin_rcap,bin_rmod=calculate_bin_para(i)
                bin_lcap=np.array([-bin_rcap[1],bin_rcap[0]])
                bn_cap_mod.append((bin_rcap,bin_rmod,bin_lcap))
            
            alpha=[]
            for j,i in enumerate(bn):
                 x=find_alphas(i,bn_cap_mod,j)
                 alpha.append(x)
                 
        ##partiotining alpha
            alpha_part=[]     
            for j,i in enumerate(alpha):
                 x=alpha_partition(i)
                 alpha_part.append(x)


        ##calculating points
            global points
            points=[]
            for j,i in enumerate(alpha_part):
                calculate_points(i,bn_cap_mod,j)
            print("number of lines after snapping %s\n"%len(points))
            for _,x1,x2,y1,y2,_ in points:
                 cv.line(img2,(int(x1),int(y1)),(int(x2),int(y2)),(0,255,0),1)
                 
            cv.imwrite('./images/'+im_name+'2.png',img2)

            write_data(points)
weightsnew.weights(image_name) 
