import pickle, struct, sys; sys.path.insert(0,'tools'); import esp
fo4=pickle.load(open('fo4.pkl','rb'))[1]; nw=pickle.load(open('nw.pkl','rb'))[1]
fo4.update(pickle.load(open('fo4b.pkl','rb'))[1]); nw.update(pickle.load(open('nwb.pkl','rb'))[1])
EDID={}; REC={}
for g,shift in ((fo4,0),(nw,1)):
    for t,rs in g.items():
        for r in rs:
            f=r['fid']
            if shift and f>>24==1: f=(f&0xFFFFFF)|0x06000000  # NW new records -> show as 06xxxxxx
            d=dict(r['subs']); EDID[f]=esp.zs(d.get('EDID',b'')); REC.setdefault(f,r); r['_t']=t
def fid(x): return '%08X:%s'%(x,EDID.get(x,'?'))
def find(sub):
    return [(k,v) for k,v in EDID.items() if sub.lower() in v.lower()]
