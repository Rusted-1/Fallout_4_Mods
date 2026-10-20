import sys,struct
sys.path.insert(0,'/home/claude/tools')
from esp import load,subs,z
recs=load(sys.argv[1]);want=sys.argv[2:]
q={}
for t,fid,fl,d in recs:
    if t=='QUST': q[fid]=next((z(x) for k,x in subs(d) if k=='EDID'),'')
cur=None
for t,fid,fl,d in recs:
    s=subs(d)
    if t=='DIAL':
        qn=next((struct.unpack('<I',x[:4])[0] for k,x in s if k=='QNAM'),0);cur=q.get(qn,'%08X'%qn)
    elif t=='INFO' and cur in want:
        for k,x in s:
            if k=='NAM1': print(cur,'|',z(x))
            if k=='RNAM': print(cur,'  [player] ',z(x))
