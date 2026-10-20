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
    d=sub('HEDR',struct.pack('<fII',1.0,nrec,0x802))
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

# --- Kellogg gate (v0.2): new forms, ESL range 0x800+ ---
GLOB_ID=0x800;QUST_ID=0x801
SL_NORA_REF=0x000FB3            # Synthetic Love's placed Nora (ACHR)
MQ106=0x000229E7;CA_AFFINITY=0x000A1B80;CA_T2_ADMIRATION=0x0004B1C5
def vm_obj(fid): return struct.pack('<BBHhI',1,1,0,-1,fid)
def ws(s): return struct.pack('<H',len(s))+s.encode()
def kellogg_records(own,sl_idx):
    g=record('GLOB',(own<<24)|GLOB_ID,0,sub('EDID',b'NN_SynthNora_AdmirationAllowed\0')+sub('FLTV',struct.pack('<f',0.0)))
    props=[('MQ106',vm_obj(MQ106)),('KelloggDeadStage',struct.pack('<BBi',3,1,902)),
           ('AdmirationAllowed',vm_obj((own<<24)|GLOB_ID)),('SynthNoraRef',vm_obj((sl_idx<<24)|SL_NORA_REF)),
           ('CA_Affinity',vm_obj(CA_AFFINITY)),('CA_T2_Admiration',vm_obj(CA_T2_ADMIRATION))]
    vm=struct.pack('<hhH',6,2,1)+ws('NN_KelloggGateScript')+struct.pack('<BH',0,len(props))+b''.join(ws(n)+b for n,b in props)
    q=(sub('EDID',b'NN_KelloggGate\0')+sub('VMAD',vm)+sub('DNAM',bytes.fromhex('110100000000000000000000'))
       +sub('NEXT',b'')+sub('ANAM',struct.pack('<I',0)))
    return g,record('QUST',(own<<24)|QUST_ID,0,q)

def build(sl,ns,eff,outdir,ucf):
    masters=['Fallout4.esm','NoraSpouse.esm','p865_SyntheticLove.esp']+(['EFF.esp'] if ucf else [])
    own=len(masters);glob,gate=kellogg_records(own,2)
    qrecs=[gate]
    if ucf: qrecs.insert(0,followers_merge(sl,eff,2,3))
    body=grup('GLOB',glob)+grup('QUST',b''.join(qrecs))
    recs=[glob]+qrecs
    desc='Nora & Nora 0.2.0 - Nora Spouse + Synthetic Love patch'+(' + UCF' if ucf else '')
    os.makedirs(outdir,exist_ok=True)
    p=os.path.join(outdir,PLUGIN)
    open(p,'wb').write(tes4(masters,len(recs),desc)+body)
    return p

if __name__=='__main__':
    sl,ns,eff,out=sys.argv[1:5]
    print(build(sl,ns,eff,os.path.join(out,'UCF'),True))
    print(build(sl,ns,eff,os.path.join(out,'NoUCF'),False))
