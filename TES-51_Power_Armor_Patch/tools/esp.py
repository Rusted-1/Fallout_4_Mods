import struct, zlib, sys
def subrecs(data):
    i=0; big=None
    while i+6<=len(data):
        t=data[i:i+4].decode('latin1'); sz=struct.unpack_from('<H',data,i+4)[0]; i+=6
        if t=='XXXX': big=struct.unpack_from('<I',data,i)[0]; i+=4; continue
        if big is not None: sz=big; big=None
        yield t,data[i:i+sz]; i+=sz
def records(buf, off=0, end=None):
    end=len(buf) if end is None else end
    while off<end:
        t=buf[off:off+4].decode('latin1'); sz=struct.unpack_from('<I',buf,off+4)[0]
        if t=='GRUP':
            yield from records(buf, off+24, off+sz); off+=sz; continue
        flags,fid=struct.unpack_from('<II',buf,off+8)
        data=buf[off+24:off+24+sz]
        if flags&0x40000: data=zlib.decompress(data[4:])
        yield t,fid,flags,data; off+=24+sz
def load(path):
    buf=open(path,'rb').read()
    return list(records(buf))
def header(path):
    buf=open(path,'rb').read(); sz=struct.unpack_from('<I',buf,4)[0]
    flags=struct.unpack_from('<I',buf,8)[0]
    masters=[d[:-1].decode('latin1') for t,d in subrecs(buf[24:24+sz]) if t=='MAST']
    return flags,masters
