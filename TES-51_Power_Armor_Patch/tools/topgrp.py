import struct, zlib, sys
sys.path.insert(0,'/home/claude/tools'); from esp import records, subrecs
def group(path, label):
    buf=open(path,'rb').read()
    off=struct.unpack_from('<I',buf,4)[0]+24
    while off<len(buf):
        sz=struct.unpack_from('<I',buf,off+4)[0]; lab=buf[off+8:off+12].decode('latin1')
        if lab==label: return list(records(buf,off+24,off+sz))
        off+=sz
