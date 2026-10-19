import sys, struct
sys.path.insert(0,'/home/claude/tools'); from esp import *
PROP={0:'Ench',1:'Bash',2:'BlockMat',3:'KW',4:'Weight',5:'Value',6:'DR',7:'AddonIdx',8:'BodyPart',9:'DmgType',10:'AV',11:'Health',12:'ColorIdx',13:'MSWP'}
FN={0:'SET',1:'MULADD',2:'ADD',3:'REM',4:'?',5:'?'}
def parse(D):
    inc,pc=struct.unpack_from('<II',D,0); o=8+2+4+2  # unk2, formtype, maxrank/lvl
    ap=struct.unpack_from('<I',D,o)[0]; o+=4
    ns=struct.unpack_from('<I',D,o)[0]; o+=4; slots=list(struct.unpack_from('<%dI'%ns,D,o)); o+=4*ns
    ni=struct.unpack_from('<I',D,o)[0]; o+=4; o+=8*ni  # items
    incs=[]
    for i in range(inc): incs.append(struct.unpack_from('<IBBB',D,o)); o+=7
    props=[]
    for i in range(pc):
        vt,fn,pr=D[o],D[o+4],struct.unpack_from('<H',D,o+8)[0]
        a=D[o+12:o+16]; b=D[o+16:o+20]
        if vt==1: v=round(struct.unpack('<f',a)[0],3)
        elif vt in(0,2): v=struct.unpack('<i',a)[0]
        elif vt==6: v=(hex(struct.unpack('<I',a)[0]),round(struct.unpack('<f',b)[0],2))
        else: v=(hex(struct.unpack('<I',a)[0]),struct.unpack('<i',b)[0])
        props.append((PROP.get(pr,pr),FN.get(fn,fn),v)); o+=24
    return ap,slots,incs,props
if __name__=='__main__':
    p=sys.argv[1]; filt=sys.argv[2] if len(sys.argv)>2 else ''
    for t,fid,f,d in load(p):
        if t!='OMOD': continue
        s={}
        for a,x in subrecs(d): s.setdefault(a,x)
        ed=s.get('EDID',b'?\0')[:-1].decode('latin1')
        if filt and filt.lower() not in ed.lower(): continue
        ap,sl,inc,pr=parse(s['DATA'])
        print(hex(fid),ed,'|',s.get('FULL',b'\0')[:-1].decode('latin1','replace'),'|',pr)
