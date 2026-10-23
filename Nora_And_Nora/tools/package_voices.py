"""Copy the voice files a built NoraAndNora plugin needs into the FOMOD's Voices folder.
Usage: python3 -I package_voices.py <plugin.esp> <Voices/Sound/Voice/<plugin>/PlayerVoiceFemale01 out dir> <voice sheets, comma separated> <fuz source dir> [more source dirs]
Every voiced line (voice sheet "File name") is copied as-is. Greetings that repeat a recorded line have their own INFO ID
(no voice sheet row): they are matched to the recorded line by text and get a copy of that .fuz under their own ID."""
import sys,os,csv,shutil
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from esp import load,subs,z
def main(plugin,out,sheets,*srcs):
    rows=[r for vc in sheets.split(',') for r in csv.DictReader(open(vc,encoding='utf-8-sig'))]
    voiced={int(r['File name'][:8],16):r['Text'] for r in rows}
    by_text={}
    for i,t in voiced.items(): by_text.setdefault(t.strip(),i)
    R=load(plugin);own=len([1 for k,x in subs(R[0][3]) if k=='MAST'])
    need={}
    for t,fid,fl,d in R[1:]:
        if t!='INFO' or fid>>24!=own: continue
        s=dict(subs(d));low=fid&0xFFFFFF
        if 'RNAM' in s: continue                                   # player line (text only)
        if low in voiced: need[low]=low;continue
        src=by_text.get(z(s.get('NAM1',b'')).strip())
        if src is not None: need[low]=src
    def find(i):
        for d in srcs:
            p=os.path.join(d,'%08X_1.fuz'%i)
            if os.path.exists(p): return p
    os.makedirs(out,exist_ok=True);missing=[]
    for dst,src in sorted(need.items()):
        p=find(src)
        if not p: missing.append('%08X'%src);continue
        shutil.copyfile(p,os.path.join(out,'%08X_1.fuz'%dst))
    print('voice files: %d (%d copies of recorded lines)'%(len(need)-len(missing),sum(1 for a,b in need.items() if a!=b)),'missing:',missing)
    return 1 if missing else 0
if __name__=='__main__': sys.exit(main(*sys.argv[1:]))
