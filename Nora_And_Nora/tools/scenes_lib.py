"""Helpers to write Fallout 4 dialogue: DIAL topics, INFO lines (with optional fragment scripts), SCEN scenes.
Layouts copied from Synthetic Love's own scenes (30_NC_Talk, 10_NC_Recruit) and greetings."""
import struct,time,re,csv
from build import sub,record,grup,zs
EMO={'neutral':0x000D755D,'happy':0x000FA847,'sad':0x000FA848,'angry':0x000FA84A,'fear':0x000FA84B,'surprise':0x000C8672,
     'stern':0x000FA849,'disgust':0x000C8674,'relieved':0x000FA863,'grateful':0x000FA84F,'pleading':0x00111073,'suspicious':0x000FA854,
     'disbelief':0x000FA853,'worried':0x000FA852,'somber':0x0017B499,'defiant':0x00114CC3,'tired':0x000FA850,'puzzled':0x000C8673,'irritated':0x000C8670}
DELIVERY_EMO=[('pleading','begging|pleading|desperate, beg'),('disbelief','disbelief|stunned whisper'),('grateful','gratitude|grateful'),
              ('relieved','relief'),('stern','cold|flat|clipped|final word|controlled anger'),('disgust','disgust|appalled'),
              ('suspicious','suspicio|testing|challenge'),('somber','grim|somber|quiet, guilty|regret'),('defiant','defiant|insisting'),
              ('worried','uneasy|unsettled|troubled|concern'),('tired','tired'),('puzzled','puzzled|confused')]
def emotion_for(delivery,base):
    d=delivery.lower();best=None
    for e,p in DELIVERY_EMO:
        m=re.search(p,d)
        if m and (best is None or m.start()<best[0]): best=(m.start(),e)
    return EMO[best[1]] if best else EMO.get(base,EMO['neutral'])
FILETIME=struct.pack('<Q',int((time.time()+11644473600)*1e7))
# condition helpers  (op: '==' '!=' '>' '>=' '<' '<=')
OPS={'==':0x00,'!=':0x20,'>':0x40,'>=':0x60,'<':0x80,'<=':0xA0}
RUN_SUBJECT,RUN_REF=0,2
def cond(fn,p1=0,p2=0,op='==',val=1.0,run=RUN_SUBJECT,ref=0,OR=False):
    return sub('CTDA',struct.pack('<B3xfH2xIIIIi',OPS[op]|(1 if OR else 0),val,fn,p1,p2,run,ref,-1))
GetStage,GetStageDone,GetInFaction,GetIsID,GetGlobalValue=58,59,71,72,74
def ws(s): b=s.encode('cp1252');return struct.pack('<H',len(b))+b
def frag_vmad(script,func,props):
    """INFO VMAD with an End fragment (layout from Synthetic Love's TIF_p865_COMNoraTalk_01001764)."""
    p=b''.join(ws(n)+v for n,v in props)
    return struct.pack('<hhH',6,2,0)+bytes([3,2])+ws(script)+struct.pack('<BH',0,len(props))+p+bytes([1])+ws(script)+ws(func)
class Dialogue:
    def __init__(s,quest_fid):
        s.quest=quest_fid;s.topics=[];s.scenes=[]
    def topic(s,fid,kind,infos,edid=None,priority=50.0):
        """kind: SCEN | GREE | IDLE. infos: list of INFO record bytes."""
        data={'SCEN':bytes([0,2,0x11,0]),'GREE':bytes([0,7,0x76,0]),'IDLE':bytes([0,7,0x68,0])}[kind]
        d=(sub('EDID',zs(edid)) if edid else b'')+sub('PNAM',struct.pack('<f',priority))+sub('QNAM',struct.pack('<I',s.quest))
        d+=sub('DATA',data)+sub('SNAM',kind.encode())+sub('TIFC',struct.pack('<I',len(infos)))
        s.topics.append((fid,record('DIAL',fid,0,d),infos));return fid
    def info(s,fid,text,emotion=EMO['neutral'],prompt=None,conds=b'',vmad=None,flags=0,start_scene=None,start_phase=''):
        d=(sub('VMAD',vmad) if vmad else b'')+sub('ENAM',struct.pack('<HH',flags,0))+sub('PNAM',struct.pack('<I',0))
        d+=sub('TRDA',struct.pack('<IB3xIii',emotion,1,0,-1,-1))+sub('NAM1',zs(text))+sub('NAM2',b'\0')+sub('NAM3',b'\0')+sub('NAM4',b'\0')
        d+=sub('NAM9',FILETIME)+(sub('RNAM',zs(prompt)) if prompt is not None else b'')+conds
        if start_scene: d+=sub('TSCE',struct.pack('<I',start_scene))
        d+=sub('NAM0',zs(start_phase))+sub('INAM',struct.pack('<I',1))
        return record('INFO',fid,0,d)
    def records(s):
        """QUST child group content: DIAL + their INFO groups, then SCENs."""
        out=b''
        for fid,dial,infos in s.topics:
            out+=dial+(b'GRUP'+struct.pack('<I',24+sum(len(i) for i in infos))+struct.pack('<I',fid)+struct.pack('<IHHHH',7,0,0,0,0)+b''.join(infos))
        return out+b''.join(s.scenes)
class Scene:
    """phases: list of (name, cond_bytes). actions added with line()/choice()/package()."""
    def __init__(s,fid,edid,quest,actors,optional=()):
        s.fid=fid;s.edid=edid;s.quest=quest;s.actors=actors;s.optional=set(optional);s.phases=[];s.actions=[];s.n=1
    def phase(s,name,conds=b''):
        s.phases.append((name,conds));return len(s.phases)-1
    def _act(s,atype,alias,flags,sp,ep,body):
        s.actions.append(sub('ANAM',struct.pack('<H',atype))+sub('NAM0',b'\0')+sub('ALID',struct.pack('<i',alias))+sub('INAM',struct.pack('<I',s.n))
                         +(sub('FNAM',struct.pack('<I',flags)) if flags is not None else b'')+sub('SNAM',struct.pack('<I',sp))+sub('ENAM',struct.pack('<I',ep))+body+sub('ANAM',b''))
        s.n+=1
    def line(s,alias,topic,ph):
        s._act(0,alias,0x29000,ph,ph,sub('DATA',struct.pack('<I',topic))+sub('DMAX',struct.pack('<f',10.0))+sub('DMIN',struct.pack('<f',1.0)))
    def choice(s,alias,ph,player,npc=(0,0,0,0)):
        """player/npc: (positive Y, negative B, neutral X, question A) topic fids."""
        b=b''.join(sub(k,struct.pack('<I',v)) for k,v in zip(('PTOP','NTOP','NETO','QTOP'),player))
        b+=b''.join(sub(k,struct.pack('<I',v)) for k,v in zip(('NPOT','NNGT','NNUT','NQUT'),npc))+sub('DTGT',struct.pack('<I',0))
        s._act(3,alias,0x229000,ph,ph,b)
    def package(s,alias,pack,sp,ep):
        s._act(1,alias,None,sp,ep,sub('PNAM',struct.pack('<I',pack)))
    def build(s):
        d=sub('EDID',zs(s.edid))+sub('FNAM',struct.pack('<I',0x24))
        for name,c in s.phases:
            d+=sub('HNAM',b'')+sub('NAM0',zs(name))+c+sub('NEXT',b'')+sub('NEXT',b'')+sub('WNAM',struct.pack('<I',0x15E))+sub('HNAM',b'')
        for a in s.actors:
            fl=4|(2 if a in s.optional else 0)              # 0x2 = optional actor (scene can run without them)
            d+=sub('ALID',struct.pack('<i',a))+sub('LNAM',struct.pack('<I',fl))+sub('DNAM',struct.pack('<I',0xA))
        d+=b''.join(s.actions)
        d+=sub('PNAM',struct.pack('<I',s.quest))+sub('INAM',struct.pack('<I',s.n))+sub('VNAM',struct.pack('<4I',3,3,3,3))+sub('XNAM',struct.pack('<I',0))
        return record('SCEN',s.fid,0,d)
def parse_script(path):
    """Lines from phase1-script.md: id -> dict(speaker,text,delivery) and choices id -> dict(button,label,line)."""
    lines={};choices={}
    for l in open(path,encoding='utf-8'):
        m=re.match(r'\|\s*(P\d-[A-Z0-9-]+)\s*\|\s*(NORA|SYNTH|NATE)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$',l)
        if m: lines[m.group(1)]={'speaker':m.group(2),'text':re.sub(r'\*(.*?)\*',r'\1',m.group(3)),'delivery':m.group(4)};continue
        m=re.match(r'\|\s*(P\d-[A-Z0-9-]+)\s*\|\s*([YBXA])\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$',l)
        if m: choices[m.group(1)]={'button':m.group(2),'label':m.group(3),'line':m.group(4)}
    return lines,choices
def voice_ids(csv_path):
    return {r['Line ID']:(int(r['File name'][:8],16),r['Emotion']) for r in csv.DictReader(open(csv_path,encoding='utf-8-sig'))}
