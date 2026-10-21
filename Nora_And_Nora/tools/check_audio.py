"""Check voice WAVs against the voice sheet: format, length vs text, level, clipping, silence."""
import sys,wave,csv,os,numpy as np,re
d,sheet=sys.argv[1:3]
rows={r['File name'][:8]:r for r in csv.DictReader(open(sheet,encoding='utf-8-sig'))}
out=[];fmt=set()
for fid,r in sorted(rows.items()):
    p=os.path.join(d,fid+'_1.wav')
    if not os.path.exists(p): out.append((fid,'MISSING'));continue
    w=wave.open(p);sr,ch,sw,n=w.getframerate(),w.getnchannels(),w.getsampwidth(),w.getnframes()
    x=np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float32)/32768.0
    if ch>1: x=x.reshape(-1,ch).mean(1)
    fmt.add((sr,ch,sw*8))
    dur=n/sr;peak=float(np.abs(x).max());rms=float(np.sqrt((x**2).mean()))
    a=np.abs(x);thr=0.02;idx=np.where(a>thr)[0]
    lead=idx[0]/sr if len(idx) else dur;trail=(n-idx[-1])/sr if len(idx) else dur
    words=len(re.findall(r"[A-Za-z']+",r['Text']))
    wps=words/max(dur-lead-trail,0.01)
    clip=int((np.abs(x)>=0.999).sum())
    flags=[]
    if clip>10: flags.append('clipping(%d)'%clip)
    if peak<0.2: flags.append('quiet')
    if lead>0.5: flags.append('lead silence %.1fs'%lead)
    if trail>0.8: flags.append('trail silence %.1fs'%trail)
    if wps>4.5: flags.append('fast %.1f w/s'%wps)
    if wps<1.2 and words>3: flags.append('slow %.1f w/s'%wps)
    out.append((fid,r['Line ID'],r['Speaker'][:5],'%.2fs'%dur,'peak %.2f'%peak,'rms %.3f'%rms,'%.1f w/s'%wps,' '.join(flags),r['Text'][:45]))
print('formats:',fmt)
for o in out: print(*o,sep=' | ')
