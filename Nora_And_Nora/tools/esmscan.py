"""Fast targeted scans of Fallout4.esm."""
import struct,zlib,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from esp import subs,z
class ESM:
    def __init__(s,p): s.b=open(p,'rb').read()
    def records(s,types=None,cells=None):
        """yield (type,fid,flags,data,parent_cell) ; types: set of top-level labels to descend; cells: set of cell fids to descend into children."""
        b=s.b
        def walk(st,e,cell):
            i=st
            while i<e:
                t=b[i:i+4];sz=struct.unpack_from('<I',b,i+4)[0]
                if t==b'GRUP':
                    lab=b[i+8:i+12];gt=struct.unpack_from('<I',b,i+12)[0]
                    if gt==0:
                        if types is None or lab.decode('latin1') in types: yield from walk(i+24,i+sz,cell)
                    elif gt in(6,8,9,10):   # cell/world children (persistent, temporary)
                        cf=struct.unpack_from('<I',b,i+8)[0]
                        if cells is None or cf in cells: yield from walk(i+24,i+sz,cf)
                    else: yield from walk(i+24,i+sz,cell)
                    i+=sz;continue
                fl,fid=struct.unpack_from('<II',b,i+8);d=b[i+24:i+24+sz]
                if fl&0x40000: d=zlib.decompress(d[4:])
                yield t.decode('latin1'),fid,fl,d,cell
                i+=24+sz
        yield from walk(0,len(b),None)
def edid(d): return next((z(x) for k,x in subs(d) if k=='EDID'),'')
