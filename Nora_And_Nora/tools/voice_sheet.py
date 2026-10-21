"""Build the AI voice sheet (CSV) from a script markdown file.
Usage: python3 -I voice_sheet.py <phaseN-script.md> <out.csv> <first INFO id hex> [<existing sheet.csv>]
With an existing sheet, lines keep their file names; new lines get numbers after the highest one; cut lines retire theirs.
Each voiced NORA/SYNTH line gets a reserved INFO form ID (ESL range); the file name is <ID>_1.wav."""
import sys,csv,re
src,out,first=sys.argv[1],sys.argv[2],int(sys.argv[3],16)
KEEP={}
if len(sys.argv)>4:
    for r in csv.DictReader(open(sys.argv[4],encoding='utf-8-sig')): KEEP[r['Line ID']]=int(r['File name'][:8],16)
    first=max([first-1]+list(KEEP.values()))+1
EMO=[('angry',r'angr|cold|hard|sharp|rage|scream|disgust|clipped|challenge|bitter'),
     ('sad',r'sob|cry|tears|hurt|hollow|breaking down|wounded|sad|resign|regret|guilt|quiet|small|tired|whisper'),
     ('fear',r'panic|fright|scared|terror|horror|hyperventil|desperate|shak|urgent|stunned|breath'),
     ('happy',r'joy|happy|relie|grati|laugh|trusting|triumph|hopeful|smile'),
     ('surprise',r'disbelief|confus|surprise|puzzled|startl')]
def emotion(d):
    d=d.lower();best=None
    for e,p in EMO:                      # the emotion named first in the delivery note wins
        m=re.search(p,d)
        if m and (best is None or m.start()<best[0]): best=(m.start(),e)
    return best[1] if best else 'neutral'
# hand corrections where the keyword guess reads wrong
OVERRIDE={'P1-S1-002':'happy','P1-S1-033':'angry','P1-S1-061':'angry','P1-S1-075':'happy','P1-AM-032':'sad',
          'P1-S2-009':'sad','P1-S2-020':'sad','P1-S3-051':'sad','P1-NT-001':'surprise','P1-NT-002':'sad'}
rows=[];scene='';nid=first
for line in open(src,encoding='utf-8'):
    if line.startswith('## ') or line.startswith('### '): scene=line.strip('# \n')
    m=re.match(r'\|\s*(P\d-[A-Z0-9-]+)\s*\|\s*(NORA|SYNTH)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$',line)
    if not m: continue
    lid,spk,text,deliv=m.groups()
    if text.startswith('(Note') or not re.search('[A-Za-z]',text): continue   # written or silent, not spoken
    plain=re.sub(r'\*(.*?)\*',r'\1',text)
    emph=re.findall(r'\*(.*?)\*',text)
    if emph: deliv+='; stress: '+', '.join(emph)
    fid=KEEP.get(lid)
    if fid is None: fid=nid;nid+=1
    rows.append({'File name':'%08X_1.wav'%fid,'Line ID':lid,'Speaker':'Organic Nora' if spk=='NORA' else 'Synth Nora',
                 'Text':plain,'Emotion':OVERRIDE.get(lid) or emotion(deliv),'Delivery':deliv,'Scene':scene})
with open(out,'w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(len(rows),'lines; new IDs from %08X, next free %08X'%(first,nid))
