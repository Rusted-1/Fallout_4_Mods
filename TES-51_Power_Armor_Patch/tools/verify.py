import sys, struct, glob, os
sys.path.insert(0,'/home/claude/tools'); from esp import *
from omod2 import parse
U="/mnt/user-data/uploads/Fallout_4_TES_Power_Armor"
BASES={'SkyrimInspiredPowerArmor.esl':f"{U}/4estGimp - TES-51 Power Armor - ESL-85030--97-1721491482/data/SkyrimInspiredPowerArmor.esl",
       'SkyrimInspiredPowerArmor.esp':f"{U}/TES-51 PA Update 1.2 HOT FIX-17956-1-2HOTFIX/SkyrimInspiredPowerArmor.esp"}
def ids(path):
    return {fid:(t,dict(subrecs(d)).get('EDID',b'?\0')[:-1].decode('latin1')) for t,fid,f,d in load(path)}
ok=True
def bad(*a):
    global ok; ok=False; print('  FAIL',*a)
for p in sorted(glob.glob('/home/claude/build/FOMOD/*/*.esp')):
    fl,m=header(p); r=load(p); print(os.path.relpath(p,'/home/claude/build/FOMOD'), 'ESL' if fl&0x200 else 'ESP', m, len(r)-1,'records')
    base=ids(BASES[m[1]]); own={fid:x for t,fid,f,d in r for x in [None]}
    buf=open(p,'rb').read(); hed=struct.unpack_from('<fiI',buf,30)
    if hed[1]!=len(r)-1: bad('HEDR count',hed)
    for t,fid,f,d in r[1:]:
        if fid>>24 >= len(m)+1: bad('bad index',hex(fid))
        if fid>>24 == len(m) and not (0x800 <= fid&0xFFFFFF <= 0xFFF) and fid&0xFFFFFF>6: bad('ESL range',hex(fid))
        if fid>>24==1 and fid not in base: bad('override of missing base record',t,hex(fid))
        if t=='OMOD' and b'_Tier_' in d[:60]:
            s=dict(subrecs(d)); ap,sl,inc,pr=parse(s['DATA'])
            mn=struct.unpack('<3I',s['MNAM'])
            for k in mn:
                if k>>24==1 and k not in base: bad('MNAM unresolved',hex(k))
            if ap!=0x17daa9: bad('attach point',hex(ap))
            ln=struct.unpack('<I',s['LNAM'])[0]
            if ln not in [x[1] for x in r]: bad('LNAM missing')
        if t=='COBJ' and b'_Tier_' in d[:60]:
            s=dict(subrecs(d)); c=struct.unpack('<I',s['CNAM'])[0]
            if c not in [x[1] for x in r]: bad('CNAM missing')
        if t=='INNR':
            for a,x in subrecs(d):
                if a=='KWDA':
                    for i in range(0,len(x),4):
                        k=struct.unpack_from('<I',x,i)[0]
                        if k>>24==1 and k not in base: bad('INNR kw unresolved',hex(k))
            vn=[struct.unpack('<I',x)[0] for a,x in subrecs(d) if a=='VNAM']
            first=[x for a,x in subrecs(d) if a=='WNAM'][0]
            print('   INNR',hex(fid),'rulesets',len(vn),vn,'first name',first)
print('ALL OK' if ok else 'PROBLEMS')
