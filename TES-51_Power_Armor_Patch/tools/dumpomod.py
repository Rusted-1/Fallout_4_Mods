import sys, struct
sys.path.insert(0,'/home/claude/tools'); from esp import *
p=sys.argv[1]; filt=sys.argv[2] if len(sys.argv)>2 else ''
recs=load(p)
names={}
for t,fid,f,d in recs:
    for st,sd in subrecs(d):
        if st=='EDID': names[fid]=sd[:-1].decode('latin1')
def n(x): return names.get(x,hex(x))
for t,fid,f,d in recs:
    if t!='OMOD': continue
    s=dict(); full=''
    for a,x in subrecs(d):
        s.setdefault(a,x)
    ed=s.get('EDID',b'?\0')[:-1].decode('latin1')
    if filt and filt.lower() not in ed.lower(): continue
    full=s.get('FULL',b'')
    D=s.get('DATA',b'')
    # OMOD DATA: includeCount u32, propCount u32, unk u8 x2, formType u32, maxRank u8, lvlTierScaledOffset u8, attachPoint u32, attachParentSlots count u32 + list, items..., includes, properties
    o=0; inc,pc=struct.unpack_from('<II',D,o); o+=8; o+=2; ftype=D[o:o+4]; o+=4; o+=2
    ap=struct.unpack_from('<I',D,o)[0]; o+=4
    nslots=struct.unpack_from('<I',D,o)[0]; o+=4; slots=[struct.unpack_from('<I',D,o+4*i)[0] for i in range(nslots)]; o+=4*nslots
    o+=0
    props=[]
    # includes: 7 bytes each (formid u32, minlvl u8, optional u8, notuserealized u8)
    incs=[]
    for i in range(inc): incs.append(n(struct.unpack_from('<I',D,o)[0])); o+=7
    for i in range(pc):
        vt,_,fn,pid=struct.unpack_from('<BBBB',D,o)[0:4] if False else (D[o],0,D[o+4],0)
        valtype=D[o]; func=D[o+4]; prop=struct.unpack_from('<H',D,o+8)[0]
        v1=D[o+12:o+16]; v2=D[o+16:o+20]
        if valtype in (1,): v1=struct.unpack('<f',v1)[0]
        elif valtype in (0,): v1=struct.unpack('<i',v1)[0]
        else: v1=n(struct.unpack('<I',v1)[0])
        v2f=struct.unpack('<f',v2)[0]
        props.append((prop,valtype,func,v1,round(v2f,3)))
        o+=24
    print(hex(fid),ed,full[:-1].decode('latin1','replace') if full else '', 'AP',n(ap),'slots',[n(x) for x in slots],'inc',incs,'props',props, 'rest',len(D)-o)
