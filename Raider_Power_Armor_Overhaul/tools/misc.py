import sys, struct; sys.path.insert(0,'tools'); import esp
from db import EDID as V, REC as VR
from armo import armo
def load(p):
    recs=esp.load(p); m=[esp.zs(d) for t,d in recs[0]['subs'] if t=='MAST']
    E={r['fid']:esp.zs(dict(r['subs']).get('EDID',b'')) for r in recs}
    def name(x):
        hi=x>>24
        if hi==len(m): return '%08X:%s'%(x,E.get(x,'?'))
        if m[hi]=='DLCNukaWorld.esm': return '%08X:%s'%(x,V.get((x&0xFFFFFF)|0x06000000,'?'))
        return '%08X:%s'%(x,V.get(x&0xFFFFFF,'?'))
    return recs,m,E,name
