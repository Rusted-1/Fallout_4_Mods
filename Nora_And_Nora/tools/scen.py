"""Dump a SCEN record in readable form."""
import sys,struct,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from esp import load,subs,z
ATYPE={0:'Dialogue',1:'Package',2:'Timer',3:'PlayerDialogue',4:'StartScene',5:'NPCResponse',6:'Radio'}
def dump(R,name):
    ed={fid:next((z(x) for k,x in subs(d) if k=='EDID'),'') for t,fid,fl,d in R}
    par={};cur=None;texts={}
    for t,fid,fl,d in R:
        if t=='DIAL': cur=fid
        if t=='INFO':
            s=subs(d);texts.setdefault(cur,[]).append((' / '.join(z(x) for k,x in s if k=='NAM1'),' '.join(z(x) for k,x in s if k=='RNAM')))
    for t,fid,fl,d in R:
        if t=='SCEN' and ed[fid]==name:
            s=subs(d);i=0;print('SCEN',name,'%08X'%fid)
            for k,x in s:
                v=struct.unpack('<I',x[:4])[0] if len(x)==4 else None
                if k=='ANAM' and len(x)==2: print('  ACTION type',ATYPE.get(struct.unpack('<H',x)[0]))
                elif k in('PTOP','NTOP','NETO','QTOP','NPOT','NNGT','NNUT','NQUT','DATA') and v:
                    print('    %s %08X'%(k,v),texts.get(v,[])[:3])
                elif k=='NAM0': print('  NAM0',z(x))
                elif k in('ALID','INAM','SNAM','ENAM','LNAM','DNAM','FNAM','PNAM','WNAM','XNAM'): print('   ',k,'%X'%v if v is not None else x.hex(), ed.get(v,'') if v else '')
                elif k=='CTDA':
                    fn=struct.unpack_from('<H',x,8)[0];p1,p2=struct.unpack_from('<II',x,12);print('    CTDA fn',fn,'%08X'%p1,ed.get(p1,''),p2,struct.unpack_from('<f',x,4)[0])
                else: print('   ',k,x.hex()[:40])
if __name__=='__main__':
    R=load(sys.argv[1])
    for n in sys.argv[2:]: dump(R,n)
