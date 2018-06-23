from plyfile import PlyElement, PlyData
import numpy as np
class face_maker():
    def __init__(self,z0,z1):
        self.mply = []
        self.face = []
        self.triads = []
        self.z0=z0
        self.z1=z1
    def quad(self,v1,v2,n):
        x1,y1=float(v1[0]), float(v1[1])
        x2,y2=float(v2[0]), float(v2[1])
        #print(x1,y1,x2,y2)
        nx1,ny1=n
        fc=[]
        z0,z1=self.z0,self.z1
        mply=self.mply
        count=len(mply)
        mply.append((x1,y1,z0,nx1,ny1,0))
        mply.append((x2,y2,z0,nx1,ny1,0))
        mply.append((x2,y2,z1,nx1,ny1,0))
        mply.append((x1,y1,z1,nx1,ny1,0))
        fc=(count,count+1,count+2,count+3)
        self.face.append((fc,))
        
    def top_bottom_quads(self,v00,v01,v10,v11):
        nx1,ny1=0,0
        fc=[]
        z0,z1=self.z0,self.z1
        mply=self.mply
        count=len(mply)
        mply.append((v00[0],v00[1],z0,nx1,ny1,-1))
        mply.append((v01[0],v01[1],z0,nx1,ny1,-1))
        mply.append((v11[0],v11[1],z0,nx1,ny1,-1))
        mply.append((v10[0],v10[1],z0,nx1,ny1,-1))
        fc=(count,count+1,count+2,count+3)
        self.face.append((fc,))
        count=len(mply)
        mply.append((v00[0],v00[1],z1,nx1,ny1,1))
        mply.append((v01[0],v01[1],z1,nx1,ny1,1))
        mply.append((v11[0],v11[1],z1,nx1,ny1,1))
        mply.append((v10[0],v10[1],z1,nx1,ny1,1))
        fc=(count,count+1,count+2,count+3)
        self.face.append((fc,))
        
    def add_triads(self,triads_to_add):
        #print(triads_to_add)
        z0, z1 = self.z0, self.z1
        for zone in triads_to_add:
            ctr = 0
            i = len(self.mply)
            for v in zone:
                self.mply.append((v[0],v[1],z0,0,0,-1))
                ctr +=1
                if ctr>2:
                    self.triads.append(((i,i+1,i+2),))
                    i += 1
            ctr = 0
            i = len(self.mply)
            for v in zone:
               self.mply.append((v[0],v[1],z1,0,0,1))
               ctr +=1
               if ctr>2:
                   self.triads.append(((i,i+1,i+2),))
                   i += 1
        
    def generate_ply(self,stream):
        b=np.array(self.mply,dtype=[('x','f4'),('y','f4'),('z','f4'),('nx','f4'),('ny','f4'),('nz','f4')])
        a=np.array(self.face,dtype=[('vertex_indices', 'i4', (4,))])
        c=np.array(self.triads,dtype=[('vertex_indices', 'i4', (3,))])
        b=b.ravel()
        a=a.ravel()
        c=c.ravel()
        el = PlyElement.describe(b, 'vertex')
        el0 = PlyElement.describe(a, 'quads')
        if len(self.triads)>0:
        	el1 = PlyElement.describe(c, 'triads')
        	PlyData([el,el0,el1],text=True).write(stream)
        else:
            PlyData([el,el0],text=True).write(stream)
