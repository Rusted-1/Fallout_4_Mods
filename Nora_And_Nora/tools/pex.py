"""Minimal Fallout 4 .pex reader/disassembler."""
import struct,sys
OPS={0:('nop',0),1:('iadd',3),2:('fadd',3),3:('isub',3),4:('fsub',3),5:('imul',3),6:('fmul',3),7:('idiv',3),8:('fdiv',3),9:('imod',3),10:('not',2),11:('ineg',2),12:('fneg',2),13:('assign',2),14:('cast',2),15:('cmp_eq',3),16:('cmp_lt',3),17:('cmp_le',3),18:('cmp_gt',3),19:('cmp_ge',3),20:('jmp',1),21:('jmpt',2),22:('jmpf',2),23:('callmethod',3,1),24:('callparent',2,1),25:('callstatic',3,1),26:('return',1),27:('strcat',3),28:('propget',3),29:('propset',3),30:('array_create',2),31:('array_length',2),32:('array_getelement',3),33:('array_setelement',3),34:('array_findelement',4),35:('array_rfindelement',4),36:('is',3),37:('struct_create',1),38:('struct_get',3),39:('struct_set',3),40:('array_findstruct',5),41:('array_rfindstruct',5),42:('array_add',3),43:('array_insert',3),44:('array_removelast',1),45:('array_remove',3),46:('array_clear',1)}
class P:
    def __init__(s,b): s.b=b;s.i=0
    def u8(s): v=s.b[s.i];s.i+=1;return v
    def u16(s): v=struct.unpack_from('<H',s.b,s.i)[0];s.i+=2;return v
    def u32(s): v=struct.unpack_from('<I',s.b,s.i)[0];s.i+=4;return v
    def i32(s): v=struct.unpack_from('<i',s.b,s.i)[0];s.i+=4;return v
    def f32(s): v=struct.unpack_from('<f',s.b,s.i)[0];s.i+=4;return v
    def u64(s): v=struct.unpack_from('<Q',s.b,s.i)[0];s.i+=8;return v
    def ws(s): n=s.u16();v=s.b[s.i:s.i+n].decode('latin1');s.i+=n;return v
def load(path):
    p=P(open(path,'rb').read());S=[]
    out={'magic':p.u32()}
    assert out['magic']==0xFA57C0DE,hex(out['magic'])
    out['ver']=(p.u8(),p.u8());out['game']=p.u16();out['time']=p.u64()
    out['src']=p.ws();out['user']=p.ws();out['machine']=p.ws()
    n=p.u16();S=[p.ws() for _ in range(n)];out['strings']=S
    def var():
        t=p.u8()
        if t==0: return None
        if t in(1,2): return ('id' if t==1 else 'str',S[p.u16()])
        if t==3: return p.i32()
        if t==4: return p.f32()
        if t==5: return bool(p.u8())
        raise ValueError(t)
    out['hasdebug']=p.u8()
    if out['hasdebug']:
        p.u64();
        for _ in range(p.u16()):
            p.u16();p.u16();p.u16();p.u8();c=p.u16();p.i+=2*c
        for _ in range(p.u16()):
            p.u16();p.u16();p.u16();p.u32();c=p.u16();p.i+=2*c
        for _ in range(p.u16()):
            p.u16();p.u16();c=p.u16();p.i+=2*c
    uf=p.u16();out['userflags']=[(S[p.u16()],p.u8()) for _ in range(uf)]
    def func():
        f={'ret':S[p.u16()],'doc':S[p.u16()],'uflags':p.u32(),'flags':p.u8()}
        f['params']=[(S[p.u16()],S[p.u16()]) for _ in range(p.u16())]
        f['locals']=[(S[p.u16()],S[p.u16()]) for _ in range(p.u16())]
        code=[]
        for _ in range(p.u16()):
            op=p.u8();spec=OPS[op];args=[var() for _ in range(spec[1])]
            if len(spec)>2:
                n=var();args+= [var() for _ in range(n)]
            code.append((spec[0],args))
        f['code']=code;return f
    objs=[]
    for _ in range(p.u16()):
        o={'name':S[p.u16()]};sz=p.u32();o['parent']=S[p.u16()];o['doc']=S[p.u16()];o['const']=p.u8();o['uflags']=p.u32();o['auto']=S[p.u16()]
        o['structs']=[]
        for _ in range(p.u16()):
            nm=S[p.u16()];mem=[]
            for _ in range(p.u16()):
                mem.append((S[p.u16()],S[p.u16()],p.u32(),var(),p.u8(),S[p.u16()]))
            o['structs'].append((nm,mem))
        o['vars']=[(S[p.u16()],S[p.u16()],p.u32(),var(),p.u8()) for _ in range(p.u16())]
        props=[]
        for _ in range(p.u16()):
            pr={'name':S[p.u16()],'type':S[p.u16()],'doc':S[p.u16()],'uflags':p.u32(),'flags':p.u8()}
            if pr['flags']&4: pr['auto']=S[p.u16()]
            else:
                if pr['flags']&1: pr['read']=func()
                if pr['flags']&2: pr['write']=func()
            props.append(pr)
        o['props']=props;states=[]
        for _ in range(p.u16()):
            sn=S[p.u16()];fs=[]
            for _ in range(p.u16()): fs.append((S[p.u16()],func()))
            states.append((sn,fs))
        o['states']=states;objs.append(o)
    out['objects']=objs;assert p.i==len(p.b),(p.i,len(p.b));return out
def fmt(a):
    if isinstance(a,tuple): return a[1] if a[0]=='id' else repr(a[1])
    return repr(a)
def dis(path,only=None):
    m=load(path)
    for o in m['objects']:
        print('object',o['name'],'extends',o['parent'])
        for sn,fs in o['states']:
            for fn,f in fs:
                if only and not any(x.lower() in fn.lower() for x in only): continue
                print('\n function %s(%s) [state %r]'%(fn,', '.join('%s %s'%(t,n) for n,t in f['params']),sn))
                for i,(op,args) in enumerate(f['code']): print('  %3d %s %s'%(i,op,' '.join(map(fmt,args))))
if __name__=='__main__': dis(sys.argv[1],sys.argv[2:] or None)
