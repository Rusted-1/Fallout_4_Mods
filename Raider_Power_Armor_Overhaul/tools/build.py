import sys, struct; sys.path.insert(0,'tools'); import esp
from misc import load, V, VR
from omod import parse as parse_omod
OUTMAST=['Fallout4.esm','DLCNukaWorld.esm','CWRaidPAT45.esp','DesRustKing-RaiderBrutePowerArmor.esp','DesRivetsAndRage-AScrappyRaiderArmorPack.esp']
SELF=len(OUTMAST)
P={'cw':'ex/cw/CWRaidPAT45.esp','rk':'ex/rk/Rust King - Brute Power Armor - BA2/DesRustKing-RaiderBrutePowerArmor.esp','rr':'ex/rr/Rivets And Rage - A Scrappy Raider Armor Pack - BA2/DesRivetsAndRage-AScrappyRaiderArmorPack.esp'}
SRC={}
for k,p in P.items():
    recs,m,E,name=load(p); fn=p.split('/')[-1]
    SRC[k]=dict(recs=recs,m=m+[fn],E=E,name=name,byedid={E[r['fid']]:r for r in recs if r['type']!='TES4'})
def remapper(k):
    m=SRC[k]['m']
    def f(x):
        if x==0: return 0
        return (OUTMAST.index(m[x>>24])<<24)|(x&0xFFFFFF)
    return f
def u32(v,o=0): return struct.unpack_from('<I',v,o)[0]
def p32(x): return struct.pack('<I',x)
def remap_list(v,f): return b''.join(p32(f(x)) for x in struct.unpack('<%dI'%(len(v)//4),v))
def remap_obts(v,f):
    v=bytearray(v); inc,pc=struct.unpack_from('<II',v,0); nk=v[15]; o=16
    for _ in range(nk): v[o:o+4]=p32(f(u32(v,o))); o+=4
    o+=2
    for _ in range(inc): v[o:o+4]=p32(f(u32(v,o))); o+=7
    for _ in range(pc):
        if v[o] in (4,6): v[o+12:o+16]=p32(f(u32(v,o+12)))
        o+=24
    assert o==len(v),(o,len(v)); return bytes(v)
def remap_omod_data(v,f):
    v=bytearray(v); inc,pc=struct.unpack_from('<II',v,0); o=16
    v[o:o+4]=p32(f(u32(v,o))); o+=4
    n=u32(v,o); o+=4
    for _ in range(n): v[o:o+4]=p32(f(u32(v,o))); o+=4
    n=u32(v,o); o+=4; assert n==0; 
    for _ in range(inc): v[o:o+4]=p32(f(u32(v,o))); o+=7
    for _ in range(pc):
        if v[o] in (4,6): v[o+12:o+16]=p32(f(u32(v,o+12)))
        o+=24
    assert o==len(v); return bytes(v)
FID_SUBS={'ARMO':{'PTRN','RNAM','INRD','MODL','MO2S','EITM','ETYP','BIDS','BAMT','TNAM'},
          'MISC':{'PTRN'},'OMOD':{'LNAM'},'COBJ':{'CNAM','BNAM'},'INNR':set()}
LIST_SUBS={'KWDA','APPR','MNAM','FNAM_COBJ'}
def remap_subs(rtype,subs,f):
    out=[]
    for t,v in subs:
        if t in FID_SUBS.get(rtype,()): v=p32(f(u32(v)))
        elif t in ('KWDA','APPR') or (rtype=='OMOD' and t=='MNAM'): v=remap_list(v,f)
        elif t=='DAMA': v=b''.join(p32(f(a))+p32(b) for a,b in struct.iter_unpack('<II',v))
        elif t=='OBTS': v=remap_obts(v,f)
        elif rtype=='OMOD' and t=='DATA': v=remap_omod_data(v,f)
        elif t=='FVPA': v=b''.join(p32(f(a))+p32(b) for a,b in struct.iter_unpack('<II',v))
        elif t=='CTDA': raise Exception('CTDA remap not needed here')
        out.append((t,v))
    return out
def zstr(s): return s.encode('cp1252')+b'\0'
# ---------- record writers
def sub(t,v):
    assert len(v)<65536; return t.encode()+struct.pack('<H',len(v))+v
def rec(t,flags,fid,subs):
    data=b''.join(sub(a,b) for a,b in subs)
    return t.encode()+struct.pack('<IIIIHH',len(data),flags&~0x40000,fid,0,131,0)+data
def grup(label,recs):
    body=b''.join(recs); return b'GRUP'+struct.pack('<I4siHHI',24+len(body),label.encode(),0,0,0,0)+body
