import sys, struct
sys.path.insert(0,'/home/claude/tools'); from esp import *
p=sys.argv[1]; filt=sys.argv[2] if len(sys.argv)>2 else ''
print(header(p))
for t,fid,f,d in load(p):
    if t!='INNR': continue
    s=list(subrecs(d)); ed=[x for a,x in s if a=='EDID']
    ed=ed[0][:-1].decode() if ed else '?'
    if filt and filt.lower() not in ed.lower(): continue
    print('==',hex(fid),ed)
    for a,x in s:
        if a in('WNAM',): print('  WNAM',x[:-1].decode('latin1','replace') if x[-1:]==b'\0' else x.hex())
        elif a=='KWDA': print('   KW',[hex(struct.unpack_from('<I',x,i)[0]) for i in range(0,len(x),4)])
        elif a=='VNAM': print(' VNAM',x.hex())
        elif a not in('EDID',): print(' ',a,x.hex()[:60])
