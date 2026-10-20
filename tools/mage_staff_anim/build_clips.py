import sys,json; sys.path.insert(0, __import__('os').path.dirname(__file__))
from glbnodes import *
import numpy as np
j,b=load('buyucu_zambak.js'); W,par=worlds(j)
names=[n.get('name') for n in j['nodes']]; idx={n:i for i,n in enumerate(names)}
arm=idx['Armature']; A=np.linalg.inv(W[arm])
D=json.load(open('mage_staff_clips.json'))
C=np.array([[1,0,0],[0,0,-1],[0,1,0]],float)  # glTF → Blender
def m2q(R):
    t=np.trace(R)
    if t>0: s=np.sqrt(t+1)*2; w=s/4; x=(R[2,1]-R[1,2])/s; y=(R[0,2]-R[2,0])/s; z=(R[1,0]-R[0,1])/s
    elif R[0,0]>R[1,1] and R[0,0]>R[2,2]: s=np.sqrt(1+R[0,0]-R[1,1]-R[2,2])*2; w=(R[2,1]-R[1,2])/s; x=s/4; y=(R[0,1]+R[1,0])/s; z=(R[0,2]+R[2,0])/s
    elif R[1,1]>R[2,2]: s=np.sqrt(1+R[1,1]-R[0,0]-R[2,2])*2; w=(R[0,2]-R[2,0])/s; x=(R[0,1]+R[1,0])/s; y=s/4; z=(R[1,2]+R[2,1])/s
    else: s=np.sqrt(1+R[2,2]-R[0,0]-R[1,1])*2; w=(R[1,0]-R[0,1])/s; x=(R[0,2]+R[2,0])/s; y=(R[1,2]+R[2,1])/s; z=s/4
    q=np.array([x,y,z,w]); return q/np.linalg.norm(q)
bones=D['bones']
rest={n:A@W[idx[n]] for n in bones}
out={'fps':D['fps'],'bones':[n.replace(':','') for n in bones],'clips':{}}
for cn,frames in D['clips'].items():
    Q=[[] for _ in bones]; P=[]
    prev=[None]*len(bones)
    for row in frames:
        Wp={}
        for n,m in zip(bones,row):
            Mb=np.eye(4); Mb[:3,:4]=np.array(m).reshape(3,4)
            Cg=np.eye(4); Cg[:3,:3]=C
            Dg=np.linalg.inv(Cg)@Mb@Cg
            Wp[n]=Dg@rest[n]
        for k,n in enumerate(bones):
            p=names[par[idx[n]]]
            L=(np.linalg.inv(Wp[p])@Wp[n]) if p in Wp else Wp[n]
            R=L[:3,:3]; sc=np.linalg.norm(R,axis=0); q=m2q(R/sc)
            if prev[k] is not None and np.dot(prev[k],q)<0: q=-q
            prev[k]=q; Q[k]+= [round(float(v),4) for v in q]
            if n=='mixamorig:Hips': P+=[round(float(v),4) for v in L[:3,3]]
    out['clips'][cn]={'q':Q,'p':P}
s=json.dumps(out,separators=(',',':'))
open('mage_staff_anim.json','w').write(s)
print(len(s), {k:len(v['p'])//3 for k,v in out['clips'].items()})
print('hips f0 guard', out['clips']['atkA']['p'][:3], 'scale chk', [round(float(x),3) for x in np.linalg.norm(Wp['mixamorig:RightHand'][:3,:3],axis=0)])
