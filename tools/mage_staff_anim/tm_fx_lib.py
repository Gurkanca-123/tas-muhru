# Taş Mührü efekt dokuları (Büyücü). Ana sahnede TM_FX koleksiyonu: ortografik kamera + düz yüzey, Cycles (CPU).
# Çizim sırasında diğer nesneler render'dan gizlenir, motor/kamera/çözünürlük sonra geri yüklenir (sahne değiştirilmez).
import bpy, math, os, numpy as np
D=r"C:\Users\Asus\Documents\tas_muhru_anim\fx"
os.makedirs(D, exist_ok=True)
sc=bpy.context.scene
def coll():
    c=bpy.data.collections.get('TM_FX')
    if not c: c=bpy.data.collections.new('TM_FX'); sc.collection.children.link(c)
    return c
def fxcam():
    cam=bpy.data.objects.get('FXcam')
    if not cam:
        cam=bpy.data.objects.new('FXcam', bpy.data.cameras.new('FXcam')); coll().objects.link(cam)
    cam.data.type='ORTHO'; cam.data.ortho_scale=2.0; cam.location=(0,0,30); cam.rotation_euler=(0,0,0)
    cam.data.clip_start=0.1; cam.data.clip_end=100
    return cam
def obj(name, me=None):
    o=bpy.data.objects.get(name)
    if not o:
        o=bpy.data.objects.new(name, me); coll().objects.link(o)
    return o
def plane(name):
    o=bpy.data.objects.get(name)
    if o: return o
    me=bpy.data.meshes.new(name); me.from_pydata([(-1,-1,25),(1,-1,25),(1,1,25),(-1,1,25)],[],[(0,1,2,3)])
    uv=me.uv_layers.new()
    for i,l in enumerate(me.loops): uv.data[i].uv=[(0,0),(1,0),(1,1),(0,1)][l.vertex_index]
    return obj(name, me)
class NB:
    def __init__(s, mat):
        mat.use_nodes=True; s.t=mat.node_tree; s.t.nodes.clear(); s.x=0
    def n(s, typ, **kw):
        nd=s.t.nodes.new(typ); nd.location=(s.x,0); s.x+=180
        for k,v in kw.items(): setattr(nd,k,v)
        return nd
    def link(s,a,b): s.t.links.new(a,b)
    def m(s, op, a, b=None, clamp=False):
        nd=s.n('ShaderNodeMath', operation=op); nd.use_clamp=clamp
        for i,v in enumerate((a,b)):
            if v is None: continue
            if isinstance(v,(int,float)): nd.inputs[i].default_value=v
            else: s.link(v, nd.inputs[i])
        return nd.outputs[0]
    def ramp(s, src, stops, const=True):
        nd=s.n('ShaderNodeValToRGB'); cr=nd.color_ramp; cr.interpolation='CONSTANT' if const else 'LINEAR'
        while len(cr.elements)>1: cr.elements.remove(cr.elements[-1])
        cr.elements[0].position=stops[0][0]; cr.elements[0].color=stops[0][1]
        for p,c in stops[1:]:
            e=cr.elements.new(p); e.color=c
        s.link(src, nd.inputs[0]); return nd
    def out(s, col, alpha):
        em=s.n('ShaderNodeEmission'); s.link(col, em.inputs[0]); em.inputs[1].default_value=1.0
        tr=s.n('ShaderNodeBsdfTransparent'); mx=s.n('ShaderNodeMixShader'); s.link(alpha, mx.inputs[0]); s.link(tr.outputs[0], mx.inputs[1]); s.link(em.outputs[0], mx.inputs[2])
        o=s.n('ShaderNodeOutputMaterial'); s.link(mx.outputs[0], o.inputs[0])
def hexc(h,a=1.0):
    c=[((h>>16)&255)/255,((h>>8)&255)/255,(h&255)/255]
    c=[x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in c]
    return (c[0],c[1],c[2],a)
class Studio:
    # with Studio(show=[...], res=128): render_still(path)
    def __init__(s, show, res, samples=16):
        s.show=set(show); s.res=res; s.samples=samples
    def __enter__(s):
        r=sc.render; s.bk=dict(engine=r.engine, ft=r.film_transparent, rx=r.resolution_x, ry=r.resolution_y, rp=r.resolution_percentage, cam=sc.camera,
            vt=sc.view_settings.view_transform, lk=sc.view_settings.look, fmt=r.image_settings.file_format, cm=r.image_settings.color_mode, fp=r.filepath)
        s.hid=[]
        for o in sc.objects:
            if o.name not in s.show and not o.hide_render: o.hide_render=True; s.hid.append(o)
        for o in sc.objects:
            if o.name in s.show: o.hide_render=False
        r.engine='CYCLES'; r.film_transparent=True  # Eevee bu bağlantıda Blender'ı çökertiyor → Cycles CPU
        cy=sc.cycles; s.cy=dict(dev=cy.device, sm=cy.samples, dn=cy.use_denoising, ad=cy.use_adaptive_sampling)
        cy.device='CPU'; cy.samples=s.samples; cy.use_denoising=False; cy.use_adaptive_sampling=False; r.resolution_x=r.resolution_y=s.res; r.resolution_percentage=100
        r.image_settings.file_format='PNG'; r.image_settings.color_mode='RGBA'
        sc.view_settings.view_transform='Standard'; sc.view_settings.look='None'
        sc.camera=fxcam()
        return s
    def shot(s, path):
        sc.render.filepath=path; bpy.ops.render.render(write_still=True); return path
    def __exit__(s, *a):
        r=sc.render; b=s.bk
        cy=sc.cycles; c=s.cy; cy.device=c['dev']; cy.samples=c['sm']; cy.use_denoising=c['dn']; cy.use_adaptive_sampling=c['ad']
        r.engine=b['engine']; r.film_transparent=b['ft']; r.resolution_x=b['rx']; r.resolution_y=b['ry']; r.resolution_percentage=b['rp']; sc.camera=b['cam']
        sc.view_settings.view_transform=b['vt']; sc.view_settings.look=b['lk']; r.image_settings.file_format=b['fmt']; r.image_settings.color_mode=b['cm']; r.filepath=b['fp']
        for o in s.hid: o.hide_render=False
        for o in sc.objects:
            if o.name.startswith('FX'): o.hide_render=True
def atlas(paths, cols, out):
    ims=[bpy.data.images.load(p) for p in paths]; W=ims[0].size[0]; rows=(len(ims)+cols-1)//cols
    A=np.zeros((rows*W, cols*W, 4), np.float32)
    for i,im in enumerate(ims):
        a=np.array(im.pixels[:],np.float32).reshape(W,W,4); r=i//cols; c=i%cols
        A[(rows-1-r)*W:(rows-r)*W, c*W:(c+1)*W]=a
    for im in ims: bpy.data.images.remove(im)
    img=bpy.data.images.new('atlas_tmp', cols*W, rows*W, alpha=True); img.alpha_mode='STRAIGHT'
    img.pixels=A.ravel(); img.filepath_raw=out; img.file_format='PNG'; img.save(); bpy.data.images.remove(img)
    return out
