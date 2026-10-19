import sys, struct; sys.path.insert(0,'tools'); import esp, glob
def fid(x): return '%08X'%x
for p in sys.argv[1:]:
    recs=esp.load(p); h=recs[0]; m=[esp.zs(d) for t,d in h['subs'] if t=='MAST']
    edid={r['fid']:esp.zs(dict(r['subs']).get('EDID',b'')) for r in recs}
    print('=====',p.split('/')[-1],'masters',m)
    for r in recs:
        if r['type']!='ARMO': continue
        S=r['subs']; d=dict(S)
        own='NEW' if r['fid']>>24==len(m) else 'OVERRIDE of '+m[r['fid']>>24]
        print('\n--',fid(r['fid']),own,esp.zs(d.get('EDID',b'')),'|',esp.zs(d.get('FULL',b'')))
        for t,v in S:
            if t=='KWDA': print('  KWDA',[fid(x)+(':'+edid[x] if x in edid else '') for x in struct.unpack('<%dI'%(len(v)//4),v)])
            elif t=='DATA': print('  DATA value,weight,health',struct.unpack_from('<ifI',v))
            elif t=='FNAM': print('  FNAM AR=%d baseAddon=%d stagger=%d'%struct.unpack_from('<HHB',v), v.hex())
            elif t=='DAMA': print('  DAMA',[(fid(a)+(':'+edid[a] if a in edid else ''),b) for a,b in struct.iter_unpack('<II',v)])
            elif t in ('RNAM','INRD','BIDS','BAMT','TNAM','EITM','ETYP','BIPL','PTRN'): print(' ',t,fid(struct.unpack('<I',v[:4])[0]))
            elif t=='BOD2': print('  BOD2 biped=%08X'%struct.unpack_from('<I',v)[0])
            elif t in ('OBTE','OBTS','OBND','MODL','MOD2','MOD4','INDX','MODT','MO2T','MO4T','MODS','MO2S','MO4S','MODC','MO2C','MO4C','MOD3','MOD5','ZNAM','YNAM','DESC','EDID','FULL','MODF','STOP','STCP','OBTF','FULL'): 
                if t=='OBTS':
                    n,mods,_=struct.unpack_from('<IIB',v); 
                    print('  OBTS combo: mods',[fid(x)+(':'+edid[x] if x in edid else '') for x in struct.unpack_from('<%dI'%0,v)] if False else v[:40].hex())
                elif t=='FULL' and S.index((t,v))>0: print('  FULL(obt?)',esp.zs(v))
            else: print(' ',t,len(v),v[:24].hex())
