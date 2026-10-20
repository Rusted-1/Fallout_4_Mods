"""Check a built NoraAndNora plugin: structure, script properties vs compiled .pex, and that referenced forms exist."""
import sys,os,struct
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from esp import load,subs,z
from vmad import parse
import pex
def check(plugin,scripts_dir,master_paths):
    b=open(plugin,'rb').read()
    def walk(s,e):
        i=s;n=0
        while i<e:
            t=b[i:i+4];sz=struct.unpack_from('<I',b,i+4)[0]
            if t==b'GRUP': n+=walk(i+24,i+sz);i+=sz
            else: i+=24+sz;n+=1
        assert i==e,'bad group sizes';return n
    walk(0,len(b))
    R=load(plugin);masters=[z(d) for t,d in subs(R[0][3]) if t=='MAST'];own=len(masters)
    forms={}
    from esmscan import ESM
    for i,m in enumerate(masters):
        if m in master_paths:
            E=ESM(master_paths[m]);mo=None
            for t,fid,fl,d,c in E.records():
                if t=='TES4': mo=len([1 for k,x in subs(d) if k=='MAST']);continue
                if fid>>24==mo: forms[(i,fid&0xFFFFFF)]=t
    for t,fid,fl,d in R[1:]:
        if fid>>24==own: forms[(own,fid&0xFFFFFF)]=t
    def kind(fid): return forms.get((fid>>24,fid&0xFFFFFF),'MISSING')
    expect={'referencealias':{'QUST'},'formlist':{'FLST'},'actorbase':{'NPC_'},'form':None,'quest':{'QUST'},'globalvariable':{'GLOB'},'objectreference':{'REFR','ACHR'},'actorvalue':{'AVIF'},'book':{'BOOK'},'followersscript':{'QUST'},'actor':{'ACHR'}}
    problems=0;report=[]
    for t,fid,fl,d in R[1:]:
        s=dict(subs(d))
        if t=='QUST':
            for k,x in subs(d):
                if k in('ALFR','ALPC'):
                    v=struct.unpack('<I',x[:4])[0];report.append('  %s %s -> %08X %s'%(z(s['EDID']),k,v,kind(v)))
                    if kind(v)=='MISSING' or (k=='ALPC' and kind(v)!='PACK'): problems+=1
        if t=='FLST':
            for k,x in subs(d):
                if k!='LNAM': continue
                v=struct.unpack('<I',x)[0];report.append('  %s LNAM -> %08X %s'%(z(s['EDID']),v,kind(v)));problems+=kind(v)=='MISSING'
        if t=='SMQN':
            for k in('PNAM','NNAM'):
                v=struct.unpack('<I',s[k])[0];report.append('  %s %s -> %08X %s'%(z(s['EDID']),k,v,kind(v)));problems+=kind(v)=='MISSING'
        for k,x in subs(d):
            if k=='CTDA' and struct.unpack_from('<H',x,8)[0]==59:   # GetStageDone(quest, stage)
                v,st=struct.unpack_from('<II',x,12);report.append('  %s CTDA GetStageDone %08X(%s) stage %d == %g'%(z(s.get('EDID',b'?')),v,kind(v),st,struct.unpack_from('<f',x,4)[0]));problems+=kind(v)!='QUST'
        if 'VMAD' not in s or fid==0x289E4: continue
        sc,_=parse(s['VMAD'])
        for name,props in sc.items():
            pp=os.path.join(scripts_dir,name+'.pex')
            if not os.path.exists(pp): report.append('  (%s: not our script, %d properties not checked against a .pex)'%(name,len(props)));continue
            m=pex.load(pp);ptypes={p['name'].lower():p['type'].lower() for p in m['objects'][0]['props']}
            for pn,(pt,v) in props.items():
                st=ptypes.get(pn.lower())
                if st is None: report.append('  !! %s.%s not a script property'%(name,pn));problems+=1;continue
                if pt==1:
                    k=kind(int(v[1],16));e=expect.get(st,{k});ok=(k!='MISSING') if e is None else k in e
                    if st=='referencealias': k+=' alias %d'%v[2]
                    report.append('  %s.%s (%s) = %s %s%s'%(name,pn,st,v[1],k,'' if ok else '  !! wrong kind'));problems+=0 if ok else 1
                else: report.append('  %s.%s (%s) = %r'%(name,pn,st,v))
            missing=set(ptypes)-{p.lower() for p in props}
            if missing: report.append('  !! unset properties on %s: %s'%(name,missing));problems+=1
    print(os.path.basename(plugin),masters,'records',len(R)-1,'| problems:',problems);print('\n'.join(report))
    return problems
if __name__=='__main__':
    plugin,scripts=sys.argv[1:3];mp=dict(a.split('=',1) for a in sys.argv[3:])
    sys.exit(1 if check(plugin,scripts,mp) else 0)
