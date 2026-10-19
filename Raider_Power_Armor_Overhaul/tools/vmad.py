import struct
def rd_str(v,o):
    n=struct.unpack_from('<H',v,o)[0]; return v[o+2:o+2+n].decode('latin1'), o+2+n
def rd_val(v,o,t):
    if t==1: oid=struct.unpack_from('<HhI',v,o); return ('obj','%08X'%oid[2]),o+8
    if t==2: return rd_str(v,o)
    if t==3: return struct.unpack_from('<i',v,o)[0],o+4
    if t==4: return struct.unpack_from('<f',v,o)[0],o+4
    if t==5: return v[o],o+1
    if t==6: return ('var',),o
    if t==7:
        n=struct.unpack_from('<I',v,o)[0]; o+=4; out=[]
        for _ in range(n):
            mn,o=rd_str(v,o); tt=v[o]; st=v[o+1]; o+=2; val,o=rd_val(v,o,tt); out.append((mn,val))
        return dict(out),o
    if t>=11:
        n=struct.unpack_from('<I',v,o)[0]; o+=4; out=[]
        for _ in range(n): val,o=rd_val(v,o,t-10); out.append(val)
        return out,o
    raise Exception('type %d'%t)
def parse(v):
    ver,objf,n=struct.unpack_from('<hhH',v,0); o=6; scripts=[]
    for _ in range(n):
        name,o=rd_str(v,o); st=v[o]; o+=1; pc=struct.unpack_from('<H',v,o)[0]; o+=2; props={}
        for _ in range(pc):
            pn,o=rd_str(v,o); t=v[o]; s=v[o+1]; o+=2; val,o=rd_val(v,o,t); props[pn]=val
        scripts.append((name,props))
    return scripts
