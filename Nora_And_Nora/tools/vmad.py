import struct
class R:
    def __init__(s,b,i=0): s.b=b;s.i=i
    def u8(s): v=s.b[s.i];s.i+=1;return v
    def i16(s): v=struct.unpack_from('<h',s.b,s.i)[0];s.i+=2;return v
    def u16(s): v=struct.unpack_from('<H',s.b,s.i)[0];s.i+=2;return v
    def u32(s): v=struct.unpack_from('<I',s.b,s.i)[0];s.i+=4;return v
    def i32(s): v=struct.unpack_from('<i',s.b,s.i)[0];s.i+=4;return v
    def f(s): v=struct.unpack_from('<f',s.b,s.i)[0];s.i+=4;return v
    def ws(s): n=s.u16();v=s.b[s.i:s.i+n].decode('latin1');s.i+=n;return v
def obj(r): r.u16();al=r.i16();fid=r.u32();return ('obj','%08X'%fid,al)
def val(r,t):
    if t==1: return obj(r)
    if t==2: return r.ws()
    if t==3: return r.i32()
    if t==4: return round(r.f(),4)
    if t==5: return r.u8()
    if t==6:
        vt=r.u8(); return ('var',vt,val(r,vt)) if vt else ('var',0)
    if t==7: return struct_(r)
    if t>=11 and t<=17:
        n=r.u32(); return [val(r,t-10) for _ in range(n)]
    raise ValueError('type %d'%t)
def struct_(r):
    n=r.u32();out={}
    for _ in range(n):
        nm=r.ws();t=r.u8();st=r.u8();out[nm]=val(r,t)
    return out
def scripts(r,n):
    out={}
    for _ in range(n):
        nm=r.ws();st=r.u8();pc=r.u16();props={}
        for _ in range(pc):
            pn=r.ws();t=r.u8();ps=r.u8();props[pn]=(t,val(r,t))
        out[nm]=props
    return out
def parse(b):
    r=R(b);ver=r.i16();of=r.i16();n=r.u16()
    return scripts(r,n),r
