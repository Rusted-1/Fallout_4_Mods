import sys, struct; sys.path.insert(0,'tools')
from build import *
EN,RAD=0x60A81,0x60A85
PARTS=['Helm','ArmLeft','ArmRight','LegLeft','LegRight','Torso']
def ptype(p): return 'Helm' if p=='Helm' else 'Torso' if p=='Torso' else 'Limb'
# target stats: (AR, ER, HP, value or None)
TARGET={
 'rr':{'Helm':(105,55,50,None),'Limb':(55,30,50,None),'Torso':(210,110,100,None)},
 'cw':{'Helm':(110,60,50,None),'Limb':(60,30,50,None),'Torso':(220,130,200,None)},
 'rk':{'Helm':(125,75,70,80),'Limb':(70,45,70,120),'Torso':(240,140,280,170)},
}
ARMO_EDID={'rr':'Armor_Power_Scrapper_','rk':'Armor_Power_RaiderBrute_','cw':'00RaidT45Armor_Power_RaidT45_'}
out={'ARMO':[],'MISC':[],'OMOD':[],'COBJ':[],'INNR':[]}
nextid=[0x800]
def newfid():
    f=(SELF<<24)|nextid[0]; nextid[0]+=1; return f
log=[]
# ---- ARMO overrides
for k in ('rr','cw','rk'):
    f=remapper(k); S=SRC[k]
    for p in PARTS:
        r=S['byedid'][ARMO_EDID[k]+p]
        subs=remap_subs('ARMO',r['subs'],f)
        ar,er,hp,val=TARGET[k][ptype(p)]
        new=[]; first_full=True
        for t,v in subs:
            if t=='FNAM': v=struct.pack('<H',ar)+v[2:]
            elif t=='DATA':
                ov,w,oh=struct.unpack_from('<ifI',v); v=struct.pack('<ifI',val if val is not None else ov,w,hp)+v[12:]
            elif t=='DAMA':
                d=[(a,b) for a,b in struct.iter_unpack('<II',v)]
                d=[(a,er if a==EN else b) for a,b in d]; v=b''.join(struct.pack('<II',a,b) for a,b in d)
            elif t=='FULL' and first_full:
                first_full=False
                if k in ('rr','rk'):
                    s=esp.zs(v); 
                    if not s.startswith('['): v=zstr('[PA_Raider]'+s)
            new.append((t,v))
        out['ARMO'].append(rec('ARMO',r['flags'],f(r['fid']),new))
        log.append((k,p,ar,er,hp))
# ---- Brute linings: rework B, add C-F
LV='BCDEF'
NAMES={'B':'Welded Plate','C':'Riveted Plate','D':'Reinforced Plate','E':'Hardened Plate','F':'Rust King Plate'}
BPART={'Helmet':'Helmet','Arm':'Arm','Leg':'Leg','Torso':'Torso'}
fk=remapper('rk'); RK=SRC['rk']
def vanilla(edid):
    ks=[k for k,v in V.items() if v==edid]; assert len(ks)==1,edid; return VR[ks[0]]
def props_raw(data):
    inc,pc=struct.unpack_from('<II',data,0); return data[:len(data)-pc*24], data[len(data)-pc*24:], pc
for part in ('Helmet','Arm','Leg','Torso'):
    tmpl=RK['byedid']['PA_RaiderBrute_%s_Lining_B'%part]
    tsubs=remap_subs('OMOD',tmpl['subs'],fk); td=dict(tsubs)
    hdr,_,_=props_raw(td['DATA'])
    misc_t=RK['byedid']['pa_comp_RaiderBrute_%s_Lining_B'%part]
    msubs=remap_subs('MISC',misc_t['subs'],fk)
    cobj_t=RK['byedid']['co_PA_RaiderBrute_%s_Lining_B'%part]
    for L in LV:
        van=dict(vanilla('PA_T51_%s_Lining_%s'%(part,L))['subs'])
        _,vprops,vpc=props_raw(van['DATA'])
        data=bytearray(hdr); struct.pack_into('<I',data,4,vpc); data=bytes(data)+vprops
        if L=='B':
            ofid=fk(tmpl['fid']); mfid=u32(td['LNAM'])
            subs=[(t,(data if t=='DATA' else v)) for t,v in tsubs]
            out['OMOD'].append(rec('OMOD',tmpl['flags'],ofid,subs)); continue
        ofid=newfid(); mfid=newfid(); cfid=newfid()
        name=NAMES[L]
        subs=[]
        for t,v in tsubs:
            if t=='EDID': v=zstr('RPA_PA_RaiderBrute_%s_Lining_%s'%(part,L))
            elif t=='FULL': v=zstr(name)
            elif t=='DATA': v=data
            elif t=='LNAM': v=p32(mfid)
            subs.append((t,v))
        out['OMOD'].append(rec('OMOD',0,ofid,subs))
        ms=[]
        for t,v in msubs:
            if t=='EDID': v=zstr('RPA_pa_comp_RaiderBrute_%s_Lining_%s'%(part,L))
            elif t=='FULL': v=zstr(esp.zs(v).replace('Welded Plate',name))
            elif t=='DATA':
                mul={'C':1.5,'D':2.0,'E':2.5,'F':3.0}[L]; val,w=struct.unpack('<if',v); v=struct.pack('<if',int(val*mul),w)
            ms.append((t,v))
        out['MISC'].append(rec('MISC',0,mfid,ms))
        vc=vanilla('co_PA_T51_%s_Lining_%s'%(part,L))['subs']
        cs=[('EDID',zstr('RPA_co_PA_RaiderBrute_%s_Lining_%s'%(part,L)))]
        for t,v in vc:
            if t=='EDID': continue
            if t=='DESC': v=b'\0'
            if t=='CNAM': v=p32(ofid)
            cs.append((t,v))   # vanilla FVPA/CTDA formIDs are Fallout4.esm -> index 00 unchanged
        out['COBJ'].append(rec('COBJ',0,cfid,cs))
# ---- CW INNR: prepend FIS tag ruleset
fc=remapper('cw'); CW=SRC['cw']
innr=[r for r in CW['recs'] if r['type']=='INNR'][0]
isubs=remap_subs('INNR',innr['subs'],fc)
dnT45=[k for k,v in V.items() if v=='dn_PowerArmor_T45'][0]
yn=[v for t,v in isubs if t=='YNAM'][0]
tag=[('VNAM',p32(1)),('WNAM',zstr('[PA_Raider]')),('KSIZ',p32(1)),('KWDA',p32(dnT45)),('YNAM',yn)]
i=[n for n,(t,v) in enumerate(isubs) if t=='VNAM'][0]
isubs=isubs[:i]+tag+isubs[i:]
# keep ruleset count: drop one trailing empty VNAM 00000000 if present
out['INNR'].append(rec('INNR',innr['flags'],fc(innr['fid']),isubs))
# ---- header + file
nrec=sum(len(v) for v in out.values())
hsubs=[('HEDR',struct.pack('<fII',1.0,nrec,nextid[0])),('CNAM',zstr('RPA_Fixes')),('SNAM',zstr('Raider power armor ladder: Raider < Scrapper < Raider T-45 < Brute. Brute gets T-51 style lining B-F. FIS raider icon tags.'))]
for mname in OUTMAST: hsubs+= [('MAST',zstr(mname)),('DATA',b'\0'*8)]
tes4=rec('TES4',0x200,0,hsubs)
tes4=tes4[:20]+struct.pack('<HH',0,0)  + tes4[24:] if False else tes4
body=tes4+grup('ARMO',out['ARMO'])+grup('MISC',out['MISC'])+grup('COBJ',out['COBJ'])+grup('OMOD',out['OMOD'])+grup('INNR',out['INNR'])
open(sys.argv[1],'wb').write(body)
print('records',{k:len(v) for k,v in out.items()},'next id',hex(nextid[0]),'bytes',len(body))
