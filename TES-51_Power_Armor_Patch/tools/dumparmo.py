import sys, struct
sys.path.insert(0,'/home/claude/tools'); from esp import *
p=sys.argv[1]; print(header(p))
recs=load(p)
ed={fid:None for t,fid,f,d in recs}
names={}
for t,fid,f,d in recs:
    for st,sd in subrecs(d):
        if st=='EDID': names[fid]=sd[:-1].decode('latin1')
for t,fid,f,d in recs:
    if t!='ARMO': continue
    o={}; kw=[]
    for st,sd in subrecs(d):
        if st in('EDID','FULL'): o[st]=sd[:-1].decode('latin1','replace') if st=='EDID' else sd
        if st=='KWDA': kw=[struct.unpack_from('<I',sd,i)[0] for i in range(0,len(sd),4)]
        if st=='INRD': o['INRD']=hex(struct.unpack('<I',sd)[0])
        if st=='BOD2': o['BOD2']=hex(struct.unpack_from('<I',sd)[0])
        if st=='DATA': o['DATA']=struct.unpack_from('<iff',sd) if len(sd)>=12 else sd.hex()
        if st=='FNAM': o['FNAM']=struct.unpack_from('<HH',sd) if len(sd)>=4 else sd.hex()
    print(hex(fid),o.get('EDID'),'FULL',o.get('FULL'),'INRD',o.get('INRD'),'BOD2',o.get('BOD2'),'FNAM',o.get('FNAM'),'DATA',o.get('DATA'),'KW',[names.get(k,hex(k)) for k in kw])
