# Patlama (16 kare), buz zemini (tek kare) ve buz kristali (GLB). tm_fx_lib.py sonrası çalışır.
from mathutils import Matrix
def noise4(b, u, v, sc_, W, z=0.0, detail=3):
    cmb=b.n('ShaderNodeCombineXYZ'); b.link(u,cmb.inputs[0]); b.link(v,cmb.inputs[1]); cmb.inputs[2].default_value=z
    nz=b.n('ShaderNodeTexNoise', noise_dimensions='4D'); nz.inputs['Scale'].default_value=sc_; nz.inputs['Detail'].default_value=detail; nz.inputs['Roughness'].default_value=0.55
    b.link(cmb.outputs[0], nz.inputs['Vector'])
    if isinstance(W,(int,float)): nz.inputs['W'].default_value=W
    else: b.link(W, nz.inputs['W'])
    return nz.outputs['Fac']
def mixc(b, fac, a, c):
    mx=b.n('ShaderNodeMix', data_type='RGBA'); b.link(fac, mx.inputs['Factor'])
    for sock,val in ((mx.inputs[6],a),(mx.inputs[7],c)):
        if isinstance(val,tuple): sock.default_value=val
        else: b.link(val, sock)
    return mx.outputs[2]
def boom_mat():
    mat=bpy.data.materials.get('FX_boom') or bpy.data.materials.new('FX_boom'); b=NB(mat)
    T=b.n('ShaderNodeValue'); T.name='T'; t=T.outputs[0]
    tc=b.n('ShaderNodeTexCoord'); sep=b.n('ShaderNodeSeparateXYZ'); b.link(tc.outputs['UV'], sep.inputs[0])
    u=b.m('MULTIPLY', b.m('SUBTRACT',sep.outputs[0],0.5),2.0); v=b.m('MULTIPLY', b.m('SUBTRACT',sep.outputs[1],0.5),2.0)
    r=b.m('SQRT', b.m('ADD', b.m('MULTIPLY',u,u), b.m('MULTIPLY',v,v)))
    n=b.m('SUBTRACT', noise4(b,u,v,1.6,b.m('MULTIPLY',t,1.1)), 0.5)
    n2=noise4(b,u,v,3.2,b.m('ADD',b.m('MULTIPLY',t,0.7),5.0),z=3.0)
    R=b.m('ADD',0.16, b.m('MULTIPLY',0.74, b.m('SUBTRACT',1.0, b.m('POWER', b.m('SUBTRACT',1.0,t), 3.0))))
    d=b.m('ADD', b.m('SUBTRACT',R,r), b.m('MULTIPLY',n, b.m('ADD',0.18, b.m('MULTIPLY',t,0.3))))
    d=b.m('SUBTRACT', d, b.m('MULTIPLY', b.m('MAXIMUM', b.m('SUBTRACT',t,0.45),0.0), b.m('MULTIPLY',n2,2.4)))
    h=b.m('ADD', b.m('SUBTRACT',1.0, b.m('MULTIPLY',t,1.3)), b.m('MULTIPLY',d,1.4))
    rp=b.ramp(h,[(0.0,hexc(0x3b302c)),(0.12,hexc(0x6a5650)),(0.22,hexc(0xc42a0a)),(0.38,hexc(0xff6a14)),(0.56,hexc(0xffb836)),(0.76,hexc(0xfff2c8))])
    ol=b.ramp(t,[(0.0,hexc(0x3a0c02)),(0.5,hexc(0x221a18))])
    col=mixc(b, b.m('LESS_THAN', d, 0.04), rp.outputs[0], ol.outputs[0])
    b.out(col, b.m('GREATER_THAN', d, 0.0))
    return mat
def frost_mat():
    mat=bpy.data.materials.get('FX_frost') or bpy.data.materials.new('FX_frost'); b=NB(mat)
    tc=b.n('ShaderNodeTexCoord'); sep=b.n('ShaderNodeSeparateXYZ'); b.link(tc.outputs['UV'], sep.inputs[0])
    u=b.m('MULTIPLY', b.m('SUBTRACT',sep.outputs[0],0.5),2.0); v=b.m('MULTIPLY', b.m('SUBTRACT',sep.outputs[1],0.5),2.0)
    r=b.m('SQRT', b.m('ADD', b.m('MULTIPLY',u,u), b.m('MULTIPLY',v,v)))
    n=b.m('SUBTRACT', noise4(b,u,v,2.6,1.7,detail=4), 0.5)
    d=b.m('ADD', b.m('SUBTRACT',0.90,r), b.m('MULTIPLY',n,0.16))
    def vor(scale):
        vo=b.n('ShaderNodeTexVoronoi', feature='DISTANCE_TO_EDGE'); vo.inputs['Scale'].default_value=scale
        b.link(tc.outputs['UV'], vo.inputs['Vector']); return vo.outputs['Distance']
    c1=b.m('LESS_THAN', vor(5.0), 0.022); c2=b.m('LESS_THAN', vor(13.0), 0.012)
    shade=b.m('ADD', r, b.m('MULTIPLY', noise4(b,u,v,6.0,3.3), 0.35))
    base=b.ramp(shade,[(0.0,hexc(0xf2fbff)),(0.42,hexc(0xc4ecff)),(0.70,hexc(0x86d2ff)),(0.95,hexc(0x4aa6ee))])
    col=mixc(b, b.m('MAXIMUM', b.m('MULTIPLY',c2,0.6), 0.0), base.outputs[0], hexc(0x5a9fe0))
    col=mixc(b, c1, col, hexc(0x1d5fa8))
    col=mixc(b, b.m('LESS_THAN', d, 0.035), col, hexc(0x123c7a))
    b.out(col, b.m('GREATER_THAN', d, 0.0))
    return mat
def boom_render(frames=16, res=128):
    pl=plane('FXboom'); mat=boom_mat(); pl.data.materials.clear(); pl.data.materials.append(mat); ps=[]
    with Studio(['FXboom','FXcam'], res) as st:
        for i in range(frames):
            mat.node_tree.nodes['T'].outputs[0].default_value=i/(frames-1); ps.append(st.shot(D+'\\boom_%02d.png'%i))
    return atlas(ps,4,D+'\\fx_boom.png')
def frost_render(res=512):
    pl=plane('FXfrost'); mat=frost_mat(); pl.data.materials.clear(); pl.data.materials.append(mat)
    with Studio(['FXfrost','FXcam'], res) as st: return st.shot(D+'\\fx_frost.png')
# Buz kristali: altıgen gövde + sivri uç, hafif eğik; 3 çeşit + 5'li küme. Birim: 1 boy, taban y=0 (glTF +y yukarı).
def shard_mesh(name, h, rad, tip, twist, lean, seed):
    import bmesh, random
    rnd=random.Random(seed); bm=bmesh.new(); n=6; rings=[]
    for zf,sc_ in ((0.0,1.0),(1.0-tip,0.82)):
        ring=[]
        for i in range(n):
            a=i/n*math.tau+twist*zf + rnd.uniform(-0.12,0.12)
            rr=rad*sc_*rnd.uniform(0.85,1.12)
            ring.append(bm.verts.new((math.cos(a)*rr+lean*zf*h, math.sin(a)*rr, zf*h)))
        rings.append(ring)
    top=bm.verts.new((lean*h+rnd.uniform(-0.02,0.02), rnd.uniform(-0.02,0.02), h))
    for i in range(n):
        j=(i+1)%n; a,b_=rings[0],rings[1]
        bm.faces.new((a[i],a[j],b_[j],b_[i])); bm.faces.new((b_[i],b_[j],top))
    bm.faces.new(list(reversed(rings[0])))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me=bpy.data.meshes.get(name) or bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth=False
    return me
def shards_build():
    obs=[]
    specs=[('buz_sivri',1.0,0.12,0.34,0.3,0.05,1),('buz_kalin',0.75,0.17,0.3,-0.2,0.08,2),('buz_ince',1.15,0.08,0.4,0.5,0.1,3)]
    for nm,h,rad,tip,tw,ln,sd in specs:
        o=obj('FX_'+nm, shard_mesh('FX_'+nm,h,rad,tip,tw,ln,sd)); o.data=bpy.data.meshes['FX_'+nm]; o.location=(len(obs)*0.6,3,0); o.hide_render=True; obs.append(o)
    # küme: ortada büyük, çevrede eğik küçükler (tek mesh)
    import bmesh
    bm=bmesh.new()
    parts=[(0,0,0,1.0,0,0.0),(0.17,0.05,0.0,0.62,1,-28),(-0.15,0.08,0,0.55,2,26),(0.04,-0.17,0,0.5,0,-22),(-0.07,0.16,0,0.45,2,20)]
    for x,y,z,s,k,tilt in parts:
        tmp=bmesh.new(); tmp.from_mesh(obs[k].data)
        M=Matrix.Translation((x,y,z))@Matrix.Rotation(math.radians(tilt),4,'Y' if k!=0 else 'X')@Matrix.Rotation(math.radians(x*600),4,'Z')@Matrix.Diagonal((s,s,s,1))
        bmesh.ops.transform(tmp, matrix=M, verts=tmp.verts)
        me_t=bpy.data.meshes.new('tmpk'); tmp.to_mesh(me_t); tmp.free(); bm.from_mesh(me_t); bpy.data.meshes.remove(me_t)
    me=bpy.data.meshes.get('FX_buz_kume') or bpy.data.meshes.new('FX_buz_kume'); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth=False
    o=obj('FX_buz_kume', me); o.location=(2.0,3,0); o.hide_render=True; obs.append(o)
    return obs
def shards_export():
    obs=shards_build()
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in obs: o.select_set(True)
    bpy.context.view_layer.objects.active=obs[0]
    loc=[o.location.copy() for o in obs]
    for o in obs: o.location=(0,0,0)
    p=D+'\\buyucu_fx_buz.glb'
    bpy.ops.export_scene.gltf(filepath=p, export_format='GLB', use_selection=True, export_apply=False, export_materials='NONE', export_animations=False, export_skins=False, export_morph=False, export_yup=True)
    for o,l in zip(obs,loc): o.location=l
    return p
