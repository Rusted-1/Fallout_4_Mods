import struct,zlib,sys,os
def read(p,out=None,filt=None):
    f=open(p,'rb');h=f.read(24);mag,ver,typ,n,nt=struct.unpack('<4sI4sIQ',h)
    if ver in(2,3): f.read(8 if ver==2 else 12)
    ents=[struct.unpack('<IIIIQIII',f.read(36)) for _ in range(n)] if typ==b'GNRL' else []
    f.seek(nt);names=[]
    for _ in range(n):
        l=struct.unpack('<H',f.read(2))[0];names.append(f.read(l).decode('latin1'))
    if typ!=b'GNRL': return names
    for nm,e in zip(names,ents):
        if filt and not any(nm.lower().endswith(x) for x in filt): continue
        if out:
            f.seek(e[4]);d=f.read(e[5] or e[6]);d=zlib.decompress(d) if e[5] else d
            op=os.path.join(out,nm.replace('\\','/'));os.makedirs(os.path.dirname(op),exist_ok=True);open(op,'wb').write(d)
    return names
if __name__=='__main__':
    for n in read(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None,['.pex','.psc','.txt']): print(n)
