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
def tes4(masters,nrec,desc,next_id=0xB00):
    d=sub('HEDR',struct.pack('<fII',1.0,nrec,next_id))
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

# --- Phase 1 systems (v0.3) ---
PH1_ID=0x802;WAITQ_ID=0x803;TIER_ID=0x804;IMPATIENT_ID=0x805;WAITNOTE_ID=0x806;FINALNOTE_ID=0x807
VAULT_ANCHOR=0x0006FA30          # MQ102SpouseCorpseFemaleREF: floor in front of Nora's pod (disabled by Nora Spouse, position still valid)
SPOUSE_POD=0x0004A012            # MQPlayerSpousePodREF
SANDBOX_CURRENT=0x00089605       # DefaultSandboxCurrentLocation
FOLLOWERS=0x000289E4
WAIT_NOTE_TEXT="I waited. I understand.\r\n\r\nI'm going to find my own way to be useful.\r\n\r\nTake care of her."
FINAL_NOTE_TEXT=("I'm not a real person, am I? I've come to accept this. I know my husband, if I can call him that, is still out there with the real me. "
 "I hope they can find happiness in this horrid world.\r\n\r\nI won't stop looking for my son. Even though I know he isn't my organic son, he is still mine in my heart, "
 "or whatever I have. I've acquired some new gear and have been tracking some of the disappearances and other synth sightings related to the Institute. "
 "If I've mapped out the sightings and disappearances right, the next one will be a local farm's wife. Connie, out at Abernathy Farm.\r\n\r\n"
 "Not again. I won't let them do it to another family like the half-assed try they did to mine. I'm going to stop them. "
 "They will regret messing with my family and all the others they have destroyed.\r\n\r\nI'm coming for you, Institute, if it's the last thing I do.")
def zs(t): return t.encode('cp1252')+b'\0'
def glob(fid,edid,val): return record('GLOB',fid,0,sub('EDID',zs(edid))+sub('FLTV',struct.pack('<f',val)))
def stages(nums): return b''.join(sub('INDX',struct.pack('<HBB',n,0,0))+sub('QSDT',b'\0') for n in nums)
def book(fid,edid,title,text,ns_path,vmad=None):
    # template: Nora Spouse's own note (NorasJournal): paper-note model, sounds and inventory art are vanilla forms
    tmpl=[x for x in load(ns_path) if x[0]=='BOOK'][0]
    out=b''
    for k,x in subs(tmpl[3]):
        if k=='EDID':
            out+=sub(k,zs(edid))
            if vmad: out+=sub('VMAD',vmad)
            continue
        elif k=='FULL': x=zs(title)
        elif k=='DESC': x=zs(text)
        out+=sub(k,x)
    return record('BOOK',fid,0,out)
def phase1_records(own,sl_idx,ns_path):
    O=lambda i:(own<<24)|i
    props=[('SynthNoraRef',vm_obj((sl_idx<<24)|SL_NORA_REF)),('Followers',vm_obj(FOLLOWERS)),('WaitQuest',vm_obj(O(WAITQ_ID))),
           ('VaultAnchor',vm_obj(VAULT_ANCHOR)),('RelationTier',vm_obj(O(TIER_ID))),('Impatient',vm_obj(O(IMPATIENT_ID))),
           ('WaitNote',vm_obj(O(WAITNOTE_ID))),('NoteAnchor',vm_obj(SPOUSE_POD))]
    vm=struct.pack('<hhH',6,2,1)+ws('NN_Phase1Script')+struct.pack('<BH',0,len(props))+b''.join(ws(n)+b for n,b in props)
    ph1=record('QUST',O(PH1_ID),0,sub('EDID',zs('NN_Phase1'))+sub('VMAD',vm)+sub('DNAM',bytes.fromhex('110100000000000000000000'))
               +sub('NEXT',b'')+stages([100,200,300,400,410,420,430])+sub('ANAM',struct.pack('<I',0)))
    alias=(sub('ALST',struct.pack('<I',0))+sub('ALID',zs('SynthNora'))+sub('FNAM',struct.pack('<I',0x282))
           +sub('ALFR',struct.pack('<I',(sl_idx<<24)|SL_NORA_REF))+sub('ALPC',struct.pack('<I',SANDBOX_CURRENT))
           +sub('VTCK',struct.pack('<I',0))+sub('ALED',b''))
    waitq=record('QUST',O(WAITQ_ID),0,sub('EDID',zs('NN_SynthNoraWaits'))+sub('DNAM',bytes(12))
                 +sub('NEXT',b'')+sub('ANAM',struct.pack('<I',1))+alias)
    globs=[glob(O(TIER_ID),'NN_NoraRelationTier',0.0),glob(O(IMPATIENT_ID),'NN_SynthNoraImpatient',0.0)]
    books=[book(O(WAITNOTE_ID),'NN_SynthNoraWaitNote','Note on a Cryo Pod',WAIT_NOTE_TEXT,ns_path),
           book(O(FINALNOTE_ID),'NN_SynthNoraFinalWish',"Nora's Final Wish",FINAL_NOTE_TEXT,ns_path,
                vmad=struct.pack('<hhH',6,2,1)+ws('NN_FinalWishScript')+struct.pack('<BH',0,1)+ws('Phase1')+vm_obj(O(PH1_ID)))]
    return globs,[ph1,waitq],books

def build_impatient(outdir):
    """FOMOD option 'Synth Nora leaves after a while': flips NN_SynthNoraImpatient to 1."""
    masters=['Fallout4.esm','NoraAndNora.esp']
    g=glob((1<<24)|IMPATIENT_ID,'NN_SynthNoraImpatient',1.0)
    os.makedirs(outdir,exist_ok=True);p=os.path.join(outdir,'NoraAndNora - Impatient.esp')
    open(p,'wb').write(tes4(masters,1,'Nora & Nora option: synth Nora leaves Vault 111 after 7 days')+grup('GLOB',g));return p

SCRIPT_MD=None;VOICE_CSV=None          # set by __main__ (phase 1 dialogue source files)
P2_SCRIPT_MD=None;P2_VOICE_CSV=None;P2_INFO=None
def build(sl,ns,eff,outdir,ucf):
    masters=['Fallout4.esm','NoraSpouse.esm','p865_SyntheticLove.esp']+(['EFF.esp'] if ucf else [])
    own=len(masters);kglob,gate=kellogg_records(own,2)
    pglobs,pquests,books=phase1_records(own,2,ns)
    qrecs=[gate]+pquests
    if ucf: qrecs.insert(0,followers_merge(sl,eff,2,3))
    nscene=0
    if SCRIPT_MD:
        import phase1_scenes
        blob,nscene,info=phase1_scenes.build_records(own,1,2,SCRIPT_MD,VOICE_CSV)
        qrecs.append(blob);print('  phase 1 dialogue:',info)
    import names
    msgs,nq=names.records(own,2);qrecs.append(nq)
    import affinity_setup
    qrecs.append(affinity_setup.record_(own,2))
    import cold_comfort
    qrecs.append(cold_comfort.record_(sl,2))
    import institute
    qrecs.append(institute.record_(own,2))
    globs=[kglob]+pglobs;flsts=[];p2count=0
    if P2_SCRIPT_MD:
        import phase2
        r=phase2.build_records(own,1,2,P2_SCRIPT_MD,P2_VOICE_CSV,SCRIPT_MD,VOICE_CSV,ns)
        qrecs+=[r['quest'],r['walk']];globs+=r['globs'];flsts=r['flsts'];msgs+=r['msgs'];books+=r['books'];p2count=r['qcount']
        global P2_INFO;P2_INFO=r['info'];print('  phase 2:',{k:v for k,v in r['info'].items() if k!='copies'},'voice copies',len(r['info']['copies']))
    body=grup('GLOB',b''.join(globs))+(grup('FLST',b''.join(flsts)) if flsts else b'')+grup('MESG',b''.join(msgs))+grup('QUST',b''.join(qrecs))+grup('BOOK',b''.join(books))
    recs=globs+flsts+msgs+qrecs+books+[b'']*max(nscene-1,0)+[b'']*max(p2count-1,0)
    desc='Nora & Nora 0.6.5 - Nora Spouse + Synthetic Love patch'+(' + UCF' if ucf else '')
    os.makedirs(outdir,exist_ok=True)
    p=os.path.join(outdir,PLUGIN)
    open(p,'wb').write(tes4(masters,len(recs),desc,next_id=0xE00)+body)
    return p

if __name__=='__main__':
    sl,ns,eff,out=sys.argv[1:5]
    if len(sys.argv)>6: SCRIPT_MD,VOICE_CSV=sys.argv[5:7]
    if len(sys.argv)>8: P2_SCRIPT_MD,P2_VOICE_CSV=sys.argv[7:9]
    print(build(sl,ns,eff,os.path.join(out,'UCF'),True))
    print(build(sl,ns,eff,os.path.join(out,'NoUCF'),False))
    print(build_impatient(os.path.join(out,'Impatient')))
