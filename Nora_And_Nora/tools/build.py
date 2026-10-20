"""Build NoraAndNora.esp patch plugins.
Usage: python3 -I build.py <sl_esp> <ns_esm> <eff_esp> <outdir>"""
import sys,struct,os,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from esp import load,subs,z
import vmad as V

FOLLOWERS=0x000289E4
PLUGIN='NoraAndNora.esp'

def find_prop(vm,script,prop):
    """Return (count_offset, elem_spans) for an array-of-struct property."""
    r=V.R(vm);r.i16();r.i16();n=r.u16()
    for _ in range(n):
        nm=r.ws();r.u8();pc=r.u16()
        for _ in range(pc):
            pn=r.ws();t=r.u8();r.u8()
            if nm.lower()==script.lower() and pn==prop:
                assert t==17
                co=r.i;cnt=r.u32();spans=[]
                for _ in range(cnt):
                    s=r.i;V.struct_(r);spans.append((s,r.i))
                return co,spans
            V.val(r,t)
    raise KeyError(prop)

def remap_struct(b,mapping):
    """Remap formIDs inside one serialized struct (objects: u16 unused,i16 alias,u32 fid)."""
    r=V.R(b);out=bytearray(b);n=r.u32()
    for _ in range(n):
        r.ws();t=r.u8();r.u8()
        if t==1:
            r.u16();r.i16();pos=r.i;fid=r.u32()
            hi=fid>>24
            if fid!=0 and hi in mapping: struct.pack_into('<I',out,pos,(mapping[hi]<<24)|(fid&0xFFFFFF))
        else: V.val(r,t)
    return bytes(out)

def sub(t,data):
    if len(data)>0xFFFF:
        return b'XXXX'+struct.pack('<HI',4,len(data))+t.encode()+struct.pack('<H',0)+data
    return t.encode()+struct.pack('<H',len(data))+data
def record(t,fid,flags,data,fv=131):
    return t.encode()+struct.pack('<IIIIHH',len(data),flags,fid,0,fv,0)+data
def grup(label,content):
    return b'GRUP'+struct.pack('<I',24+len(content))+label.encode()+struct.pack('<IHHHH',0,0,0,0,0)+content
def tes4(masters,nrec,desc):
    d=sub('HEDR',struct.pack('<fII',1.0,nrec,0x800))
    d+=sub('CNAM',b'Rusted-1\0')+sub('SNAM',desc.encode('cp1252')+b'\0')
    for m in masters: d+=sub('MAST',m.encode()+b'\0')+sub('DATA',b'\0'*8)
    return record('TES4',0,0x200,d)  # ESL-flagged ESP (light plugin)

def own_index(recs):
    return len([1 for t,d in subs(recs[0][3]) if t=='MAST'])

def followers_merge(sl,eff,idx_sl,idx_eff):
    """UCF's Followers override + Synthetic Love's 4 custom affinity events."""
    slr=load(sl);effr=load(eff)
    sl_own=own_index(slr);eff_own=own_index(effr)
    slvm=dict(subs([x for x in slr if x[1]==FOLLOWERS][0][3]))['VMAD']
    erec=[x for x in effr if x[1]==FOLLOWERS][0]
    es=subs(erec[3]);evm=dict(es)['VMAD']
    _,slspans=find_prop(slvm,'followersscript','AffinityEvents')
    co,espans=find_prop(evm,'followersscript','AffinityEvents')
    assert len(slspans)==len(espans)+4, (len(slspans),len(espans))
    extra=b''.join(remap_struct(slvm[s:e],{sl_own:idx_sl}) for s,e in slspans[-4:])
    cnt=struct.unpack_from('<I',evm,co)[0]
    newvm=bytearray(evm[:co]+struct.pack('<I',cnt+4)+evm[co+4:espans[-1][1]]+extra+evm[espans[-1][1]:])
    # remap UCF's own formID(s) in the record (ExtensionHooks property)
    eff_ids={fid for t,fid,fl,d in effr if fid>>24==eff_own}
    out=b''
    for t,x in es:
        if t=='VMAD': x=bytes(newvm)
        x=bytearray(x)
        for i in range(len(x)-3):
            v=struct.unpack_from('<I',x,i)[0]
            if v in eff_ids: struct.pack_into('<I',x,i,(idx_eff<<24)|(v&0xFFFFFF))
        out+=sub(t,bytes(x))
    return record('QUST',FOLLOWERS,erec[2]&~0x40000,out)

def build(sl,ns,eff,outdir,ucf):
    masters=['Fallout4.esm','NoraSpouse.esm','p865_SyntheticLove.esp']+(['EFF.esp'] if ucf else [])
    recs=[]
    if ucf: recs.append(followers_merge(sl,eff,2,3))
    body=grup('QUST',b''.join(recs)) if recs else b''
    desc='Nora & Nora - compatibility patch for Nora Spouse + Synthetic Love'+(' + UCF' if ucf else '')
    os.makedirs(outdir,exist_ok=True)
    p=os.path.join(outdir,PLUGIN)
    open(p,'wb').write(tes4(masters,len(recs),desc)+body)
    return p

if __name__=='__main__':
    sl,ns,eff,out=sys.argv[1:5]
    print(build(sl,ns,eff,os.path.join(out,'UCF'),True))
    print(build(sl,ns,eff,os.path.join(out,'NoUCF'),False))
