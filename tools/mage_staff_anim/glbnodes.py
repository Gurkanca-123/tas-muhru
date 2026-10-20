import base64,json,struct,re,sys
import numpy as np
def load(js,key=None):
    s=open(js).read(); m=re.findall(r"\['([^']+)'\]\s*=\s*'([^']+)'",s)
    b=base64.b64decode(m[0][1] if not key else dict(m)[key])
    L=struct.unpack('<I',b[12:16])[0]; j=json.loads(b[20:20+L])
    bin_=b[20+L+8:]
    return j,bin_
def q2m(q):
    x,y,z,w=q
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
def trs(n):
    M=np.eye(4)
    if 'matrix' in n: return np.array(n['matrix']).reshape(4,4).T
    R=q2m(n.get('rotation',[0,0,0,1])); S=np.diag(n.get('scale',[1,1,1]))
    M[:3,:3]=R@S; M[:3,3]=n.get('translation',[0,0,0]); return M
def worlds(j):
    par={}
    for i,n in enumerate(j['nodes']):
        for c in n.get('children',[]): par[c]=i
    W={}
    def w(i):
        if i in W: return W[i]
        M=trs(j['nodes'][i]); W[i]=(w(par[i])@M) if i in par else M; return W[i]
    for i in range(len(j['nodes'])): w(i)
    return W,par
