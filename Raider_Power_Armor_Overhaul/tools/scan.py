import struct, zlib, sys, pickle; sys.path.insert(0,'tools'); import esp
def scan(path, types):
    buf=open(path,'rb').read(); out={t:[] for t in types}
    i=struct.unpack_from('<I',buf,4)[0]+24
    hdr=list(esp.records(buf,0,i))[0]
    while i<len(buf):
        assert buf[i:i+4]==b'GRUP'
        sz,label=struct.unpack_from('<I4s',buf,i+4); label=label.decode('latin1')
        if label in types: out[label]=list(esp.records(buf,i+24,i+sz))
        i+=sz
    return hdr,out
if __name__=='__main__':
    src,dst=sys.argv[1],sys.argv[2]; types=sys.argv[3].split(',')
    pickle.dump(scan(src,types),open(dst,'wb'))
