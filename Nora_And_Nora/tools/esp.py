import struct,zlib,sys,collections
def subs(data):
    i=0;out=[];big=None
    while i+6<=len(data):
        t=data[i:i+4].decode('latin1');sz=struct.unpack_from('<H',data,i+4)[0];i+=6
        if t=='XXXX': big=struct.unpack_from('<I',data,i)[0];i+=sz;continue
        if big is not None: sz=big;big=None
        out.append((t,data[i:i+sz]));i+=sz
    return out
def walk(buf,start,end,recs,grp=None):
    i=start
    while i<end:
        t=buf[i:i+4].decode('latin1');sz=struct.unpack_from('<I',buf,i+4)[0]
        if t=='GRUP':
            walk(buf,i+24,i+sz,recs,buf[i+8:i+12]);i+=sz;continue
        flags,fid=struct.unpack_from('<II',buf,i+8);d=buf[i+24:i+24+sz]
        if flags&0x40000: d=zlib.decompress(d[4:])
        recs.append((t,fid,flags,d));i+=24+sz
def load(p):
    b=open(p,'rb').read();recs=[];walk(b,0,len(b),recs);return recs
def z(b):
    return b.split(b'\0')[0].decode('cp1252','replace')
if __name__=='__main__':
    recs=load(sys.argv[1]);h=recs[0]
    print('MASTERS',[z(d) for t,d in subs(h[3]) if t=='MAST'])
    print('flags %x'%h[2])
    c=collections.Counter(r[0] for r in recs);print(dict(c))
    for want in sys.argv[2:]:
        for t,fid,fl,d in recs:
            if t==want:
                s=subs(d);ed=next((z(x) for k,x in s if k=='EDID'),'');fu=next((z(x) for k,x in s if k=='FULL'),'')
                print(want,'%08X'%fid,ed,'|',fu if len(fu)<60 else '')
