import sys, struct; sys.path.insert(0,'tools'); import esp
PROPS={0:'Enchantments',1:'BashImpact',2:'BlockMaterial',3:'Keywords',4:'Weight',5:'Value',6:'Rating',7:'AddonIndex',8:'BodyPart',9:'DamageTypeValue',10:'ActorValues',11:'Health',12:'ColorRemap',13:'MaterialSwaps'}
FN={0:'SET',1:'MUL+ADD',2:'ADD'}
def parse(v):
    inc,pc=struct.unpack_from('<II',v,0); o=8+2; ftype=v[o:o+4].decode('latin1'); o+=4
    maxrank,lvl=v[o],v[o+1]; o+=2
    ap=struct.unpack_from('<I',v,o)[0]; o+=4
    n=struct.unpack_from('<I',v,o)[0]; o+=4; slots=struct.unpack_from('<%dI'%n,v,o); o+=4*n
    n=struct.unpack_from('<I',v,o)[0]; o+=4; o+=8*n
    incs=[]
    for _ in range(inc): incs.append(struct.unpack_from('<IBBB',v,o)); o+=7
    props=[]
    for _ in range(pc):
        vt,fn,prop=v[o],v[o+4],struct.unpack_from('<H',v,o+8)[0]
        a,b,step=v[o+12:o+16],v[o+16:o+20],struct.unpack_from('<f',v,o+20)[0]
        if vt==1: val=(struct.unpack('<f',a)[0],)
        elif vt in (4,6): val=('%08X'%struct.unpack('<I',a)[0], struct.unpack('<I',b)[0] if vt==6 else struct.unpack('<f',b)[0])
        else: val=(struct.unpack('<i',a)[0],)
        props.append((PROPS.get(prop,prop),FN.get(fn,fn),vt,val)); o+=24
    return dict(ftype=ftype,ap=ap,slots=slots,incs=incs,props=props,rest=len(v)-o)
if __name__=='__main__':
 for p in sys.argv[1:]:
     recs=esp.load(p); m=[esp.zs(d) for t,d in recs[0]['subs'] if t=='MAST']
     edid={r['fid']:esp.zs(dict(r['subs']).get('EDID',b'')) for r in recs}
     print('=====',p.split('/')[-1])
     for r in recs:
         if r['type']!='OMOD': continue
         d=dict(r['subs']); x=parse(d['DATA'])
         if x['ftype']!='ARMO': continue
         print('%08X %-45s %-35s ap=%08X:%s'%(r['fid'],esp.zs(d.get('EDID',b'')),esp.zs(d.get('FULL',b'')),x['ap'],edid.get(x['ap'],'')), 'rest',x['rest'])
         for pr in x['props']: print('      ',pr)
 