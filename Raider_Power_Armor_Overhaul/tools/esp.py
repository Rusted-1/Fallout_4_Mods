import struct, zlib, sys
def subrecords(data):
    i=0; big=None; out=[]
    while i < len(data):
        t=data[i:i+4].decode('latin1'); sz=struct.unpack_from('<H',data,i+4)[0]; i+=6
        if t=='XXXX': big=struct.unpack_from('<I',data,i)[0]; i+=sz; continue
        if big is not None: sz=big; big=None
        out.append((t,data[i:i+sz])); i+=sz
    return out
def records(buf, start=0, end=None, path=()):
    i=start; end=len(buf) if end is None else end
    while i<end:
        t=buf[i:i+4].decode('latin1')
        if t=='GRUP':
            sz,label,gt=struct.unpack_from('<I4si',buf,i+4)
            yield from records(buf,i+24,i+sz,path+(label,))
            i+=sz; continue
        sz,flags,fid=struct.unpack_from('<III',buf,i+4)
        d=buf[i+24:i+24+sz]
        if flags & 0x40000: d=zlib.decompress(d[4:])
        yield dict(type=t,flags=flags,fid=fid,subs=subrecords(d))
        i+=24+sz
def load(p):
    buf=open(p,'rb').read()
    return list(records(buf))
def zs(b): return b.split(b'\0')[0].decode('cp1252','replace')
