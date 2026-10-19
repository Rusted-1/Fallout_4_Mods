import sys, struct; sys.path.insert(0,'tools')
from build import *
from armo import armo
pr=esp.load(sys.argv[1]); hdr=pr[0]; masters=[esp.zs(v) for t,v in hdr['subs'] if t=='MAST']
print('flags',hex(hdr['flags']),'HEDR',struct.unpack('<fII',dict(hdr['subs'])['HEDR']),'masters',masters)
PE={r['fid']:esp.zs(dict(r['subs']).get('EDID',b'')) for r in pr[1:]}
MODE={OUTMAST[2]:SRC['cw']['E'],OUTMAST[3]:SRC['rk']['E'],OUTMAST[4]:SRC['rr']['E']}
def resolve(x, mlist, selfE):
    if x==0: return 'NULL'
    hi=x>>24; lo=x&0xFFFFFF
    mn = mlist[hi] if hi<len(mlist) else None
    if mn=='Fallout4.esm': e=V.get(lo)
    elif mn=='DLCNukaWorld.esm': e=V.get(lo|0x06000000)
    elif mn in MODE: e=MODE[mn].get((MODE_FID[mn]<<24)|lo)
    elif hi==len(mlist): e=selfE.get(x)
    else: e=None
    if e is None: raise Exception('UNRESOLVED %08X in %s'%(x,mn))
    return (mn or 'self')+':'+e
MODE_FID={OUTMAST[2]:1,OUTMAST[3]:2,OUTMAST[4]:2}
def fids(rtype,subs):
    out=[]
    for t,v in subs:
        if t in FID_SUBS.get(rtype,()) : out.append((t,u32(v)))
        elif t in ('KWDA','APPR') or (rtype=='OMOD' and t=='MNAM'): out+= [(t,x) for x in struct.unpack('<%dI'%(len(v)//4),v)]
        elif t in ('DAMA','FVPA'): out+=[(t,a) for a,b in struct.iter_unpack('<II',v)]
        elif t=='CTDA': out.append((t,u32(v,12)))
        elif t=='OBTS':
            inc,pc=struct.unpack_from('<II',v,0); nk=v[15]; o=16
            for _ in range(nk): out.append((t,u32(v,o))); o+=4
            o+=2
            for _ in range(inc): out.append((t,u32(v,o))); o+=7
            for _ in range(pc):
                if v[o] in (4,6): out.append((t,u32(v,o+12)))
                o+=24
        elif rtype=='OMOD' and t=='DATA':
            inc,pc=struct.unpack_from('<II',v,0); o=16; out.append((t,u32(v,o))); o+=4
            n=u32(v,o); o+=4
            for _ in range(n): out.append((t,u32(v,o))); o+=4
            o+=4
            for _ in range(inc): out.append((t,u32(v,o))); o+=7
            for _ in range(pc):
                if v[o] in (4,6): out.append((t,u32(v,o+12)))
                o+=24
    return out
errs=0; checked=0
for r in pr[1:]:
    try:
        res=[(t,resolve(x,masters,PE)) for t,x in fids(r['type'],r['subs'])]; checked+=len(res)
    except Exception as e: print('ERR',r['type'],'%08X'%r['fid'],PE[r['fid']],e); errs+=1; continue
    hi=r['fid']>>24
    if hi<len(masters) and masters[hi] in MODE:   # override: compare resolved refs with original
        k={OUTMAST[2]:'cw',OUTMAST[3]:'rk',OUTMAST[4]:'rr'}[masters[hi]]
        orig=[o for o in SRC[k]['recs'] if o['fid']==((MODE_FID[masters[hi]]<<24)|(r['fid']&0xFFFFFF))][0]
        ores=[(t,resolve(x,SRC[k]['m'],{})) if False else (t,x) for t,x in fids(orig['type'],orig['subs'])]
        om=SRC[k]['m']
        def res2(x):
            mn=om[x>>24]; lo=x&0xFFFFFF
            return mn+':'+(V.get(lo) if mn=='Fallout4.esm' else V.get(lo|0x06000000) if mn=='DLCNukaWorld.esm' else SRC[k]['E'][x])
        ores=[(t,res2(x)) for t,x in ores]
        same=[(a,b) for a,b in zip(ores,res) if a!=b]
        if r['type']=='OMOD':   # linings B: props replaced, compare non-DATA refs only
            ores=[x for x in ores if x[0]!='DATA']; res_=[x for x in res if x[0]!='DATA']; same=[(a,b) for a,b in zip(ores,res_) if a!=b]
        if same or (r['type']!='OMOD' and len(ores)!=len(res)) or [t for t,v in orig['subs']]!=[t for t,v in r['subs']]:
            if r['type']=='INNR' and not same: pass
            else: print('DIFF',r['type'],PE.get(r['fid']),same[:3],len(ores),len(res)); errs+=1
print('formID refs checked',checked,'errors',errs)
