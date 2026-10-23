"""Cross-check the dialogue (Phase 1 and Phase 2) inside a built NoraAndNora.esp.
Usage: python3 -I verify_dialogue.py <scripts dir> <voice sheet.csv>[,<voice sheet 2.csv>...] <plugin> [...]"""
import sys,os,struct,csv,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from esp import load,subs,z
import pex
def check(plugin,scripts_dir,voice_csv):
    R=load(plugin);masters=[z(d) for t,d in subs(R[0][3]) if t=='MAST'];own=len(masters)
    probs=[];by={}
    ids=collections.Counter(fid for t,fid,fl,d in R[1:])
    probs+=['duplicate form id %08X'%f for f,c in ids.items() if c>1]
    probs+=['%s %08X outside light-plugin range'%(t,fid) for t,fid,fl,d in R[1:] if fid>>24==own and not 0x800<=(fid&0xFFFFFF)<=0xFFF]
    for t,fid,fl,d in R[1:]: by[fid]=(t,subs(d))
    dial_infos=collections.defaultdict(list);cur=None
    for t,fid,fl,d in R[1:]:
        if t=='DIAL': cur=fid
        if t=='INFO' and fid>>24==own: dial_infos[cur].append(fid)
    for f,(t,s) in by.items():
        if t=='DIAL' and f>>24==own:
            tifc=struct.unpack('<I',dict(s)['TIFC'])[0]
            if tifc!=len(dial_infos[f]): probs.append('DIAL %08X TIFC %d but %d infos'%(f,tifc,len(dial_infos[f])))
    QST={f:{struct.unpack_from('<H',x)[0] for k,x in s if k=='INDX'} for f,(t,s) in by.items()
         if t=='QUST' and z(dict(s).get('EDID',b'')) in ('NN_P1Scenes','NN_Phase2','NN_Phase4')}
    qstages=set().union(*QST.values())
    TIFS={}
    for fn_ in os.listdir(scripts_dir):
        if not fn_.endswith('.pex'): continue
        o=pex.load(os.path.join(scripts_dir,fn_))['objects'][0]
        if o['parent'].lower()=='topicinfo':
            TIFS[o['name']]=({fn for sn,fs in o['states'] for fn,_ in fs},{p['name'] for p in o['props']})
    def stage_bad(x):
        quest=struct.unpack_from('<I',x,12)[0];st=struct.unpack_from('<I',x,16)[0]
        return quest in QST and st not in QST[quest],st
    scenes={};nsc=0
    for f,(t,s) in by.items():
        if t!='SCEN' or f>>24!=own: continue
        nsc+=1;phases=[z(x) for k,x in s if k=='NAM0'];
        # phase names are the NAM0 entries between HNAM pairs
        names=[];i=0
        while i<len(s):
            if s[i][0]=='HNAM' and i+1<len(s) and s[i+1][0]=='NAM0': names.append(z(s[i+1][1]));i+=2;continue
            i+=1
        scenes[f]=names;n=len(names)
        for k,x in s:
            if k in('SNAM','ENAM') and len(x)==4:
                v=struct.unpack('<I',x)[0]
                if v>=n: probs.append('%s phase index %d >= %d'%(z(dict(s)['EDID']),v,n))
            if k in('DATA','PTOP','NTOP','NETO','QTOP','NPOT','NNGT','NNUT','NQUT') and len(x)==4:
                v=struct.unpack('<I',x)[0]
                if v and (v not in by or by[v][0]!='DIAL' or not dial_infos[v]): probs.append('%s %s -> %08X not a topic with lines'%(z(dict(s)['EDID']),k,v))
            if k=='CTDA' and struct.unpack_from('<H',x,8)[0]==59:
                bad,st=stage_bad(x)
                if bad: probs.append('condition on missing stage %d'%st)
    voiced={int(r['File name'][:8],16) for vc in voice_csv.split(',') for r in csv.DictReader(open(vc,encoding='utf-8-sig'))}
    placed=set();frags=collections.Counter()
    for f,(t,s) in by.items():
        if t!='INFO' or f>>24!=own: continue
        low=f&0xFFFFFF;d=dict(s)
        if low in voiced: placed.add(low)
        for k,x in s:
            if k=='CTDA' and struct.unpack_from('<H',x,8)[0]==59:
                bad,st=stage_bad(x)
                if bad: probs.append('INFO %08X condition on missing stage %d'%(f,st))
        if 'TSCE' in d:
            sc=struct.unpack('<I',d['TSCE'])[0];ph=z(d['NAM0'])
            if sc>>24!=own: pass                      # another plugin's scene (checked by verify_refs)
            elif sc not in scenes: probs.append('INFO %08X starts missing scene'%f)
            elif ph not in scenes[sc]: probs.append('INFO %08X starts at unknown phase %r'%(f,ph))
        if 'VMAD' in d:
            v=d['VMAD'];i=6+2;n=struct.unpack_from('<H',v,i)[0];name=v[i+2:i+2+n].decode();i+=2+n
            i+=1;pc=struct.unpack_from('<H',v,i)[0];i+=2
            for _ in range(pc):
                n=struct.unpack_from('<H',v,i)[0];pn=v[i+2:i+2+n].decode();i+=2+n+2+8
                if name in TIFS and pn not in TIFS[name][1]: probs.append('INFO %08X sets unknown property %s'%(f,pn))
            i+=1;n=struct.unpack_from('<H',v,i)[0];i+=2+n;n=struct.unpack_from('<H',v,i)[0];fn=v[i+2:i+2+n].decode();i+=2+n
            if i!=len(v): probs.append('INFO %08X VMAD length mismatch'%f)
            if name not in TIFS or fn not in TIFS[name][0]: probs.append('INFO %08X fragment %s.%s missing'%(f,name,fn))
            frags[fn]+=1
    missing=voiced-placed
    if missing: probs.append('voiced lines not placed: %s'%sorted('%X'%m for m in missing))
    print(os.path.basename(os.path.dirname(plugin)),'| scenes',nsc,'| voiced lines placed %d/%d'%(len(placed),len(voiced)),'| quest stages',sorted(qstages))
    print('  fragments used:',dict(frags))
    print('  problems:',len(probs));[print('   ',p) for p in probs[:30]]
    return len(probs)
if __name__=='__main__':
    bad=sum(check(p,sys.argv[1],sys.argv[2]) for p in sys.argv[3:]);sys.exit(1 if bad else 0)
