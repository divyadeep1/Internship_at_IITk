import numpy as np
import matplotlib.pyplot as plt
import math as m
import os 
import uuid 


## query can be none
##            or
##   an array of parameters inside an array

## given an unique id so that images with  same name do not over ride.

class grapher():
    
    def __init__(self,query=[[None]],path='./'):
        self.count1=0
        self.path=path
        self.query=query



    def plot_all(self,index,stats):
        count=0
        for value in self.query:
            print(value)
            if(value[0]==None):
                print("###")
                for A in stats:
                    for j,name in enumerate(A.dtype.names):  ## this part will plot all the parameters in one graph
                        if 'index' not in name:
                            plt.plot(A[name])
                    x=uuid.uuid1()        
                    plt.savefig(os.path.join(self.path,'all_'+str(x)+'_.png'))    
                    plt.gcf().clear()
            else:
                if(value!=None):
                        print('yes')
                        for A in stats:
                            for j,name in enumerate(A.dtype.names): ### this part will plot all the selected parameters in one graph  
                                if name in value:
                                    plt.plot(A[name])
                            x=uuid.uuid1()      
                            plt.savefig(os.path.join(self.path,'selected_'+str(x)+'_.png'))
                            plt.gcf().clear()
                                    
                    
            
    
       
if __name__=='__main__':

    temp=[]
    x=[]
    r=np.arange(.1,100,.1)
    for i in r:
        temp.append((m.log(i),m.sin(i)))
    stats=np.array(temp,dtype=[('loss', 'f4'),
                               ('accuracy', 'f4')])
    x.append(stats)
    
    a=grapher([['loss'],['accuracy','loss'],[None]])
    a.plot_all(0,x)
        

    
    
