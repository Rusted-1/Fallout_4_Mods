import sys, struct
sys.path.insert(0,'/home/claude/tools'); from esp import *
p=sys.argv[1]; typ=sys.argv[2]; filt=sys.argv[3] if len(sys.argv)>3 else ''
recs=load(p)
for t,fid,f,d in recs:
    if t!=typ: continue
    s=list(subrecs(d)); ed=[x for a,x in s if a=='EDID']; ed=ed[0][:-1].decode('latin1') if ed else '?'
    if filt and filt.lower() not in ed.lower(): continue
    print('==',t,hex(fid),hex(f),ed)
    for a,x in s:
        if a in('EDID','FULL','DESC') : print('  ',a,repr(x[:-1].decode('latin1','replace'))[:200])
        elif a=='CTDA':
            op,=struct.unpack_from('<B',x,0); cv=struct.unpack_from('<f',x,4)[0]; fn=struct.unpack_from('<H',x,8)[0]; p1=struct.unpack_from('<I',x,12)[0]
            print('   CTDA op',hex(op),'cmp',cv,'func',fn,'p1',hex(p1),x.hex())
        elif a=='FVPA': print('   FVPA',[(hex(struct.unpack_from('<I',x,i)[0]),struct.unpack_from('<I',x,i+4)[0]) for i in range(0,len(x),8)])
        else: print('  ',a,len(x),x.hex()[:120])
