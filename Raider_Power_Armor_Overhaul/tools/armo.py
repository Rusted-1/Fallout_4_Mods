import struct, sys; sys.path.insert(0,'tools'); import esp
from omod import parse as parse_omod
def obts(v):
    inc,pc=struct.unpack_from('<II',v,0); lmin,lmax=v[8],v[10]; addon=struct.unpack_from('<h',v,12)[0]; default=v[14]; nk=v[15]; o=16
    kws=struct.unpack_from('<%dI'%nk,v,o); o+=4*nk; o+=2
    incs=[]
    for _ in range(inc): incs.append(struct.unpack_from('<I',v,o)[0]); o+=7
    props=[]
    for _ in range(pc): props.append(v[o:o+24]); o+=24
    return dict(lmin=lmin,lmax=lmax,default=default,kws=kws,incs=incs,props=props,rest=len(v)-o)
def armo(r):
    S=r['subs']; d=dict(S); out=dict(edid=esp.zs(d.get('EDID',b'')))
    out['kw']=struct.unpack('<%dI'%(len(d['KWDA'])//4),d['KWDA']) if 'KWDA' in d else ()
    out['value'],out['weight'],out['health']=struct.unpack_from('<ifI',d['DATA'])
    out['ar']=struct.unpack_from('<H',d['FNAM'])[0]
    out['dama']={a:b for a,b in struct.iter_unpack('<II',d['DAMA'])} if 'DAMA' in d else {}
    out['inrd']=struct.unpack('<I',d['INRD'])[0] if 'INRD' in d else None
    out['combos']=[obts(v) for t,v in S if t=='OBTS']
    return out
