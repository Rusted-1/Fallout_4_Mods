"""Phase 3: Synth Nora reacts to synth-related moments in the vanilla game (docs/script/phase3-script.md, sections 1-4).

Quest NN_Phase3 (0xE02, start game enabled) with NN_Phase3Script. Three ways in, all without editing vanilla records:
1. Vanilla dialogue reaction points: CompanionAffinityEventQuestScript sends the custom event CompanionAffinityEvent
   with (quest, sender, eventID) for every flagged player line. Synthetic Love has no handlers for them; we do, for
   the five lines in section 1 (event IDs from the game data, docs/analysis/08).
2. FollowersScript's AffinityEvent: the Nuclear Option evacuation keywords (CA__CustomEvent_MQ302[DoNot]EvacuateInstitute).
   Synthetic Love already reacts to evacuating, so that one only gets her line; not evacuating gets a Dislike too.
3. Quest stages (remote OnStageSet) for Institutionalized, faction joins and endings, and the synth-hunting quests.
Each moment plays once (its NN_Phase3 stage marks it done) and only if synth Nora is a current companion and near.
Reaction: FollowersScript.SendAffinityEvent with Synthetic Love's keyword (shows "Synth Nora liked that."); then her
line via Say, then Organic Nora's reply if she is a companion and near. The Shaun talk waits until synth Nora is with you.
Line INFO IDs come from docs/script/phase3-voice-sheet.csv (0xE10-0xE2F); topics 0xE30+."""
import sys,os,struct,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from build import sub,record,zs,vm_obj
from scenes_lib import Dialogue,cond,GetIsID,GetGlobalValue,emotion_for,parse_script,voice_ids,ws
from pexasm import Script,S
import pexw
HERE=os.path.dirname(os.path.abspath(__file__))
P3Q=0xE02; TOPIC_FIRST=0xE30; NEXT_FREE=0xE60
QS='NN_Phase3Script'
SL_NORA_REF=0x000FB3; SL_NORA_NPC=0x000F99; NS_NORA_REF=0x001735; NS_NORA_NPC=0x000F9A
SL_KW={'Likes':0x26CD,'Loves':0x26CE,'Dislikes':0x26CB,'Hates':0x26CC}
CURRENT_COMPANION=0x00023C01; TIER=0x804; HURT=0xB08
CAEQ=0x001C5099
EVAC,NOEVAC=0x0019B647,0x0019B648
Q={'BunkerHill':0x00019955,'MQ105':0x000229E6,'MQ201':0x000229E8,'RR101':0x000459D2,'RR102':0x0006FA37,
   'MQ207':0x000229EC,'MinRecruit00':0x0011B36E,'MQ302Min':0x0010C64A,'MQ302RR':0x0010C64C,'MQ302BoS':0x0010C64B,
   'BoS101':0x0006F5C1,'Inst308':0x000BAD00,'MinDestBoS':0x000DFB3C,'RR303':0x00043275,'Inst307':0x000BACFF,
   'BoS302':0x000B9F9D,'MS17':0x00022A08,'Inst301':0x000E2058}
# name: (own stage, reaction, line IDs, then-play moment, wait for her)
M={'SP001':(10,'Dislikes',['P3-SP-001'],None,False),'SP010':(20,'Hates',['P3-SP-010'],None,False),
   'SP011':(30,'Hates',['P3-SP-011'],None,False),'SP020':(40,'Loves',['P3-SP-020'],None,False),
   'SP021':(50,'Loves',['P3-SP-021'],None,False),'SP030':(60,None,['P3-SP-030'],None,False),
   'SP031':(70,'Dislikes',['P3-SP-031'],None,False),
   'SH':(100,None,['P3-SH-001','P3-SH-002','P3-SH-003','P3-SH-004'],None,True),
   'FC001':(200,'Likes',['P3-FC-001'],None,False),'FC002':(210,'Loves',['P3-FC-002','P3-FC-003'],'INSTD',False),
   'FC010':(220,'Loves',['P3-FC-010'],None,False),'FC011':(230,'Loves',['P3-FC-011','P3-FC-012'],'INSTD',False),
   'FC020':(240,'Dislikes',['P3-FC-020','P3-FC-021'],None,False),'FC022':(250,'Dislikes',['P3-FC-022','P3-FC-023'],'INSTD',False),
   'FC030':(260,'Likes',['P3-FC-030','P3-FC-031'],None,False),'FC040':(270,'Likes',['P3-FC-040','P3-FC-041'],None,False),
   'INSTD':(280,None,['P3-FC-050','P3-FC-051'],None,False),
   'HU001':(300,'Loves',['P3-HU-001'],None,False),'HU002':(310,'Hates',['P3-HU-002'],None,False),
   'HU010':(320,'Loves',['P3-HU-010'],None,False),'HU011':(330,'Hates',['P3-HU-011'],None,False),
   'HU020':(340,'Dislikes',['P3-HU-020'],None,False)}
TIER3_ONLY={'P3-FC-023'}
BUMPS=[('BunkerHill',1,'SP001'),('MQ105',1,'SP010'),('MQ201',1,'SP011'),('MQ201',5,'SP011'),('RR101',1,'SP020'),('RR102',8,'SP021')]
STAGES=[('MQ207',150,'SH'),('MQ207',180,'SH'),('MinRecruit00',50,'FC001'),('MQ302Min',1900,'FC002'),('RR102',800,'FC010'),
        ('MQ302RR',900,'FC011'),('BoS101',555,'FC020'),('MQ302BoS',900,'FC022'),('Inst308',200,'FC030'),
        ('MinDestBoS',500,'FC040'),('RR303',1150,'FC040'),('Inst307',200,'FC040'),('BoS302',120,'HU001'),('BoS302',90,'HU002'),
        ('BoS302',170,'HU002'),('MS17',500,'HU010'),('MS17',600,'HU010'),('MS17',740,'HU011'),('Inst301',500,'HU020')]
STAGE_QUESTS=sorted({q for q,_,_ in STAGES})
T_SHAUN=1
def load_lines(script_md):
    L,_=parse_script(script_md);return L
def quest_script(out,script_md):
    L=load_lines(script_md);dur=json.load(open(os.path.join(HERE,'phase3_durations.json')))
    sc=Script(QS,'Quest','Nora and Nora: Phase 3, synth Nora on synth-related moments.')
    SYN=sc.prop('SynthNoraRef','objectreference');NOR=sc.prop('NoraRef','objectreference');FAC=sc.prop('CompanionFaction','faction')
    TIERG=sc.prop('Tier','globalvariable');CA=sc.prop('CompanionAffinity','companionaffinityeventquestscript')
    KW={k:sc.prop('Synth'+k,'keyword') for k in SL_KW};EV=sc.prop('EvacuateKW','keyword');NEV=sc.prop('DoNotEvacuateKW','keyword')
    QP={k:sc.prop('Q_'+k,'quest') for k in Q}
    TP={lid:sc.prop('T_'+lid.replace('-','_'),'topic') for m in M.values() for lid in m[2]}
    PENDING=sc.var('ShaunPending','Bool',False)
    f=sc.func('Ready',[('akRef','objectreference')],'Bool')
    a=f.cast('akRef','actor');d=f.call(a,'IsDead');f.jmpt(d,'no')
    x=f.call(a,'IsInFaction',FAC);f.jmpf(x,'no')
    pl=f.callstatic('game','GetPlayer');po=f.cast(pl,'objectreference');dist=f.call('akRef','GetDistance',po);c=f.cmp('cmp_lt',dist,3000.0);f.ret(c)
    f.label('no');f.ret(False)
    f=sc.func('React',[('akEvent','keyword')])
    so=f.cast('self','ScriptObject');f.callstatic('followersscript','SendAffinityEvent',so,'akEvent',None,None,True,True,False,0.0)
    f=sc.func('Speak',[('akRef','objectreference'),('akTopic','topic'),('afSeconds','Float')])
    f.call('akRef','Say','akTopic',None,False,None);f.callstatic('utility','Wait','afSeconds')
    order=['INSTD']+[k for k in M if k!='INSTD']
    for name in order:
        st,react,lids,then,wait=M[name]
        f=sc.func('M_'+name)
        d=f.call('self','GetStageDone',st);f.jmpt(d,'end')
        r=f.callself('Ready',SYN);f.jmpt(r,'go')
        if wait: f.op('assign',PENDING,True);f.call('self','StartTimerGameTime',0.1,T_SHAUN)
        f.ret()
        f.label('go');f.call('self','SetStage',st)
        if react: f.callself('React',KW[react]);f.callstatic('utility','Wait',1.5)
        for i,lid in enumerate(lids):
            who=SYN if L[lid]['speaker']=='SYNTH' else NOR
            skip='s%d'%i
            if who is NOR: nr=f.callself('Ready',NOR);f.jmpf(nr,skip)
            if lid in TIER3_ONLY: t=f.call(TIERG,'GetValue');c=f.cmp('cmp_ge',t,3.0);f.jmpf(c,skip)
            f.callself('Speak',who,TP[lid],float(dur[lid])+0.4)
            f.label(skip)
        if then: f.callself('M_'+then)
        f.label('end')
    f=sc.func('OnInit')
    so=f.cast(CA,'ScriptObject');f.call('self','RegisterForCustomEvent',so,S('companionaffinityeventquestscript_CompanionAffinityEvent'))
    fs=f.callstatic('followersscript','GetScript');so2=f.cast(fs,'ScriptObject');f.call('self','RegisterForCustomEvent',so2,S('followersscript_AffinityEvent'))
    for k in STAGE_QUESTS:
        so3=f.cast(QP[k],'ScriptObject');f.call('self','RegisterForRemoteEvent',so3,S('OnStageSet'))
    f=sc.func('::remote_CompanionAffinityEventQuestScript_CompanionAffinityEvent',[('akSender','companionaffinityeventquestscript'),('akArgs','Var[]')])
    v0=f.tmp('Var');f.op('array_getelement',v0,'akArgs',0);q=f.cast(v0,'quest')
    v2=f.tmp('Var');f.op('array_getelement',v2,'akArgs',2);eid=f.cast(v2,'Int')
    for i,(qk,ev,name) in enumerate(BUMPS):
        c=f.cmp('cmp_eq',q,QP[qk]);f.jmpf(c,'b%d'%i);c2=f.cmp('cmp_eq',eid,ev);f.jmpf(c2,'b%d'%i);f.callself('M_'+name);f.ret();f.label('b%d'%i)
    f=sc.func('::remote_FollowersScript_AffinityEvent',[('akSender','followersscript'),('akArgs','Var[]')])
    v0=f.tmp('Var');f.op('array_getelement',v0,'akArgs',0);kw=f.cast(v0,'keyword')
    c=f.cmp('cmp_eq',kw,EV);f.jmpf(c,'n1');f.callself('M_SP030');f.ret();f.label('n1')
    c=f.cmp('cmp_eq',kw,NEV);f.jmpf(c,'n2');f.callself('M_SP031');f.label('n2')
    f=sc.func('::remote_Quest_OnStageSet',[('akSender','quest'),('auiStageID','Int'),('auiItemID','Int')])
    for i,(qk,stg,name) in enumerate(STAGES):
        c=f.cmp('cmp_eq','akSender',QP[qk]);f.jmpf(c,'s%d'%i);c2=f.cmp('cmp_eq','auiStageID',stg);f.jmpf(c2,'s%d'%i);f.callself('M_'+name);f.ret();f.label('s%d'%i)
    f=sc.func('OnTimerGameTime',[('aiTimerID','Int')])
    f.jmpf(PENDING,'end')
    r=f.callself('Ready',SYN);f.jmpf(r,'again')
    pl=f.callstatic('game','GetPlayer');cb=f.call(pl,'IsInCombat');f.jmpt(cb,'again')
    f.op('assign',PENDING,False);f.callself('M_SH');f.ret()
    f.label('again');f.call('self','StartTimerGameTime',0.1,T_SHAUN)
    f.label('end')
    pexw.write(sc.module(),out);return sc
def build_records(own,ns_idx,sl_idx,script_md,voice_csv):
    O=lambda i:(own<<24)|i
    L=load_lines(script_md);V=voice_ids(voice_csv)
    D=Dialogue(O(P3Q));nxt=[TOPIC_FIRST];topics={}
    who={'SYNTH':cond(GetIsID,(sl_idx<<24)|SL_NORA_NPC,0,'==',1.0),'NORA':cond(GetIsID,(ns_idx<<24)|NS_NORA_NPC,0,'==',1.0)}
    for m in M.values():
        for lid in m[2]:
            ln=L[lid];iid,emo=V[lid];assert iid&0xFFFFFF<TOPIC_FIRST
            info=D.info(O(iid&0xFFFF),ln['text'],emotion_for(ln['delivery'],emo),conds=who[ln['speaker']])
            tid=O(nxt[0]);nxt[0]+=1;assert nxt[0]<=NEXT_FREE
            topics[lid]=D.topic(tid,'SCEN',[info],edid='NN_P3_'+lid.replace('-','_'))
    props=[('SynthNoraRef',vm_obj((sl_idx<<24)|SL_NORA_REF)),('NoraRef',vm_obj((ns_idx<<24)|NS_NORA_REF)),('CompanionFaction',vm_obj(CURRENT_COMPANION)),
           ('Tier',vm_obj(O(TIER))),('CompanionAffinity',vm_obj(CAEQ)),('EvacuateKW',vm_obj(EVAC)),('DoNotEvacuateKW',vm_obj(NOEVAC))]
    props+=[('Synth'+k,vm_obj((sl_idx<<24)|v)) for k,v in SL_KW.items()]+[('Q_'+k,vm_obj(v)) for k,v in Q.items()]
    props+=[('T_'+lid.replace('-','_'),vm_obj(t)) for lid,t in topics.items()]
    vm=struct.pack('<hhH',6,2,1)+ws(QS)+struct.pack('<BH',0,len(props))+b''.join(ws(n)+v for n,v in props)
    q=sub('EDID',zs('NN_Phase3'))+sub('VMAD',vm)+sub('FULL',zs(''))
    q+=sub('DNAM',struct.pack('<HBBII',0x0011,60,0,0,0))+sub('NEXT',b'')
    q+=b''.join(sub('INDX',struct.pack('<HBB',m[0],0,0))+sub('QSDT',b'\0') for m in sorted(M.values()))
    q+=sub('ANAM',struct.pack('<I',0))
    quest=record('QUST',O(P3Q),0,q)
    child=D.records()
    group=b'GRUP'+struct.pack('<I',24+len(child))+struct.pack('<I',O(P3Q))+struct.pack('<IHHHH',10,0,0,0,0)+child
    n=1+len(D.topics)+sum(len(i) for _,_,i in D.topics)
    return quest+group,n,{'topics':len(D.topics),'lines':sum(len(i) for _,_,i in D.topics)}
if __name__=='__main__':
    quest_script(os.path.join(sys.argv[1],QS+'.pex'),sys.argv[2]);print('phase 3 script ok')
