# Alev dili: 16 kare (alev doğar, yükselir, kopar). Kenardaki koyu bant = sticker çizgisi. Çalıştır: flame_render(n_frames, res)
def flame_mat():
    mat=bpy.data.materials.get('FX_flame') or bpy.data.materials.new('FX_flame'); b=NB(mat)
    T=b.n('ShaderNodeValue'); T.name='T'; T.outputs[0].default_value=0.3
    S=b.n('ShaderNodeValue'); S.name='SEED'; S.outputs[0].default_value=0.0
    tc=b.n('ShaderNodeTexCoord'); sep=b.n('ShaderNodeSeparateXYZ'); b.link(tc.outputs['UV'], sep.inputs[0])
    u,v=sep.outputs[0],sep.outputs[1]
    vy=b.m('ADD',b.m('MULTIPLY',v,2.2),b.m('MULTIPLY',T.outputs[0],-1.8))
    cmb=b.n('ShaderNodeCombineXYZ'); b.link(b.m('MULTIPLY',u,2.0),cmb.inputs[0]); b.link(vy,cmb.inputs[1]); b.link(S.outputs[0],cmb.inputs[2])
    nz=b.n('ShaderNodeTexNoise', noise_dimensions='4D'); nz.inputs['Scale'].default_value=2.2; nz.inputs['Detail'].default_value=3; nz.inputs['Roughness'].default_value=0.55
    b.link(cmb.outputs[0], nz.inputs['Vector']); b.link(b.m('MULTIPLY',T.outputs[0],1.3), nz.inputs['W'])
    n=b.m('SUBTRACT', nz.outputs['Fac'], 0.5)
    grow=b.m('MINIMUM', b.m('MULTIPLY',T.outputs[0],4.0), 1.0)
    shrink=b.m('SUBTRACT',1.0, b.m('POWER', T.outputs[0], 2.2))
    env=b.m('MULTIPLY',grow,shrink)
    lift=b.m('MULTIPLY', b.m('MAXIMUM', b.m('SUBTRACT',T.outputs[0],0.45),0.0), 0.9)
    vv=b.m('SUBTRACT', v, lift)
    ax=b.m('MULTIPLY', b.m('ABSOLUTE', b.m('SUBTRACT',u,0.5)), 2.0)
    w=b.m('MULTIPLY', b.m('POWER', b.m('MAXIMUM', b.m('SUBTRACT',1.0,vv),0.0), 0.75), b.m('MULTIPLY',env,0.78))
    d=b.m('SUBTRACT', w, ax)
    d=b.m('ADD', d, b.m('MULTIPLY', n, b.m('ADD', b.m('MULTIPLY',vv,0.9), 0.15)))
    d=b.m('SUBTRACT', d, b.m('MULTIPLY', b.m('MAXIMUM', b.m('SUBTRACT',0.10, vv),0.0), 4.0))
    r=b.ramp(d,[(0.0,hexc(0x000000)),(0.001,hexc(0x3a0800)),(0.045,hexc(0xd8280a)),(0.12,hexc(0xff6a14)),(0.22,hexc(0xffb030)),(0.32,hexc(0xffe680)),(0.42,hexc(0xfffbe8))])
    b.out(r.outputs[0], b.m('GREATER_THAN', d, 0.0))
    mat.surface_render_method='DITHERED'
    return mat
def flame_render(frames=16, res=128, seeds=(0,1)):
    pl=plane('FXflame'); mat=flame_mat(); pl.data.materials.clear(); pl.data.materials.append(mat)
    outs=[]
    with Studio(['FXflame','FXcam'], res) as st:
        for seed in seeds:
            ps=[]
            for i in range(frames):
                mat.node_tree.nodes['T'].outputs[0].default_value=i/(frames-1)
                mat.node_tree.nodes['SEED'].outputs[0].default_value=seed*7.3
                ps.append(st.shot(D+'\\flame_%d_%02d.png'%(seed,i)))
            outs.append(atlas(ps,4,D+'\\fx_flame%d.png'%seed))
    return outs
