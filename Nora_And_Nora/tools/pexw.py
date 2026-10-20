"""Minimal Fallout 4 .pex writer (no debug info). Takes the structure produced by pex.load()."""
import struct,time
from pex import OPS
OPN={v[0]:(k,v) for k,v in OPS.items()}
def write(m,path=None):
    S=[];idx={}
    def si(s):
        if s not in idx: idx[s]=len(S);S.append(s)
        return idx[s]
    def ws(s): b=s.encode('latin1');return struct.pack('<H',len(b))+b
    def var(v):
        if v is None: return b'\0'
        if isinstance(v,tuple): return struct.pack('<BH',1 if v[0]=='id' else 2,si(v[1]))
        if isinstance(v,bool): return struct.pack('<BB',5,int(v))
        if isinstance(v,int): return struct.pack('<Bi',3,v)
        if isinstance(v,float): return struct.pack('<Bf',4,v)
        raise TypeError(v)
    def func(f):
        b=struct.pack('<HHIB',si(f['ret']),si(f['doc']),f['uflags'],f['flags'])
        b+=struct.pack('<H',len(f['params']))+b''.join(struct.pack('<HH',si(n),si(t)) for n,t in f['params'])
        b+=struct.pack('<H',len(f['locals']))+b''.join(struct.pack('<HH',si(n),si(t)) for n,t in f['locals'])
        b+=struct.pack('<H',len(f['code']))
        for op,args in f['code']:
            code,spec=OPN[op];fixed=spec[1];b+=struct.pack('<B',code)
            b+=b''.join(var(a) for a in args[:fixed])
            if len(spec)>2:
                rest=args[fixed:];b+=var(len(rest))+b''.join(var(a) for a in rest)
            else: assert len(args)==fixed,(op,args)
        return b
    objs=b''
    for o in m['objects']:
        d=struct.pack('<HHBIH',si(o['parent']),si(o['doc']),o['const'],o['uflags'],si(o['auto']))
        d+=struct.pack('<H',len(o['structs']))
        for nm,mem in o['structs']:
            d+=struct.pack('<HH',si(nm),len(mem))
            for n,t,uf,v,c,doc in mem: d+=struct.pack('<HHI',si(n),si(t),uf)+var(v)+struct.pack('<BH',c,si(doc))
        d+=struct.pack('<H',len(o['vars']))+b''.join(struct.pack('<HHI',si(n),si(t),uf)+var(v)+struct.pack('<B',c) for n,t,uf,v,c in o['vars'])
        d+=struct.pack('<H',len(o['props']))
        for p in o['props']:
            d+=struct.pack('<HHHIB',si(p['name']),si(p['type']),si(p['doc']),p['uflags'],p['flags'])
            if p['flags']&4: d+=struct.pack('<H',si(p['auto']))
            else:
                if p['flags']&1: d+=func(p['read'])
                if p['flags']&2: d+=func(p['write'])
        d+=struct.pack('<H',len(o['states']))
        for sn,fs in o['states']:
            d+=struct.pack('<HH',si(sn),len(fs))+b''.join(struct.pack('<H',si(fn))+func(f) for fn,f in fs)
        objs+=struct.pack('<HI',si(o['name']),len(d)+4)+d
    uflags=m.get('userflags',[])
    dbg=b''
    nf=0
    for o in m['objects']:
        for sn,fs in o['states']:
            for fn,f in fs:
                n=len(f['code']);dbg+=struct.pack('<HHHBH',si(o['name']),si(sn),si(fn),0,n)+b''.join(struct.pack('<H',i+1) for i in range(n));nf+=1
    debug=struct.pack('<BQH',1,m.get('time',int(time.time())),nf)+dbg+struct.pack('<HH',0,0)
    body=debug+struct.pack('<H',len(uflags))+b''.join(struct.pack('<HB',si(n),i) for n,i in uflags)+struct.pack('<H',len(m['objects']))+objs
    head=struct.pack('<IBBHQ',0xFA57C0DE,3,9,2,m.get('time',int(time.time())))+ws(m['src'])+ws(m['user'])+ws(m['machine'])
    out=head+struct.pack('<H',len(S))+b''.join(ws(s) for s in S)+body
    if path: open(path,'wb').write(out)
    return out
