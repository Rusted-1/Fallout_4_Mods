"""Phase 1 dialogue: quest NN_P1Scenes with greetings, scenes S1 (Diamond City), S1C (first time together),
S2 (Vault 111, breakdown + choice), SK (after the hostile kill), SNT (note read), and idle chatter.
Text comes from docs/script/phase1-script.md; spoken lines use the INFO IDs reserved in the voice sheet."""
import sys,os,struct
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from build import sub,record,zs,vm_obj
from scenes_lib import Dialogue,Scene,cond,GetStage,GetStageDone,GetInFaction,GetIsID,RUN_REF,frag_vmad,emotion_for,parse_script,voice_ids,EMO,ws
from pexasm import Script,S
import pexw

QUEST=0x808
SL_QUEST=0x000F9B; SL_NORA_NPC=0x000F99; SL_NORA_REF=0x000FB3
NS_NORA_REF=0x001735; NS_FIRSTMEET=0x001F48
COMPANION_FACTION=0x00023C01; STAY_PACKAGE=0x00019AA2
PH1=0x802
A_SYNTH,A_NORA=0,1
TIF='NN_P1S_TIF'
# affinity events: Synthetic Love's keywords (registered in Followers by SL) and Nora Spouse's (registered at runtime by NS)
SL_KW={'Likes':0x26CD,'Loves':0x26CE,'Dislikes':0x26CB,'Hates':0x26CC}
NS_KW={'Likes':0x1F32,'Loves':0x1F35,'Dislikes':0x1F33,'Hates':0x1F34}
# what each choice fragment sends (from the Effect column of phase1-script.md)
AFF={31:[('Nora','Likes'),('Synth','Loves')],41:[('Nora','Likes'),('Synth','Loves')],
     33:[('Nora','Dislikes'),('Synth','Hates')],43:[('Nora','Dislikes'),('Synth','Hates')],
     44:[('Nora','Likes'),('Synth','Dislikes')]}
AFF_FRAGS={'Aff_S2_010':[('Synth','Likes')],'Aff_S2_011':[('Synth','Dislikes')],
           'Aff_NT_010':[('Nora','Likes')],'Aff_NT_011':[('Nora','Dislikes')],'Aff_NT_012':[('Nora','Dislikes')]}
# Diamond City choices come before synth Nora is recruited: held as stages, sent once she has joined
PENDING={51:('Synth','Dislikes'),52:('Synth','Likes'),53:('Synth','Dislikes')}
FRAGS=['Frag_51','Frag_52','Frag_53','Aff_S2_010','Aff_S2_011','Aff_NT_010','Aff_NT_011','Aff_NT_012','Frag_31','Frag_32','Frag_33','Frag_34','Frag_41','Frag_42','Frag_43','Frag_44','Frag_73','Frag_13',
       'Frag_Met','Frag_MetAlone','Frag_AtVault','Frag_Out100','Frag_Out200','Frag_Out300','Frag_Out400']

def tif_script(out):
    """One shared TopicInfo fragment script; each INFO points at one function."""
    sc=Script(TIF,'TopicInfo','Nora and Nora: Phase 1 dialogue fragments.')
    PH=sc.prop('Phase1','quest');SLQ=sc.prop('SLQuest','quest')
    KW={(who,k):sc.prop(who+k,'keyword') for who in ('Synth','Nora') for k in ('Likes','Loves','Dislikes','Hates')}
    f=sc.func('React',[('akEvent','keyword')])          # shows "<name> liked that." and changes affinity
    so=f.cast('self','ScriptObject');f.callstatic('followersscript','SendAffinityEvent',so,'akEvent',None,None,True,True,False,1.0)
    def react(f,lst):
        for who,k in lst: f.callself('React',KW[(who,k)])
    for st in (31,32,33,34,41,42,43,44,73,13,51,52,53):
        f=sc.func('Frag_%d'%st,[('akSpeakerRef','objectreference')])
        react(f,AFF.get(st,[]))
        q=f.call('self','GetOwningQuest');f.call(q,'SetStage',st)
    for name,lst in AFF_FRAGS.items():
        f=sc.func(name,[('akSpeakerRef','objectreference')]);react(f,lst)
    def met(f,stage):
        q=f.call('self','GetOwningQuest')
        f.call(SLQ,'SetStage',10);f.call(SLQ,'SetStage',20)                    # Synthetic Love's own recruit stages
        f.call(SLQ,'SetObjectiveDisplayed',20,False,False)                    # hide "...examine the corpse"
        f.call(q,'SetStage',stage);f.call(q,'SetObjectiveDisplayed',10,True,False)   # show "Travel with Nora to Vault 111"
        f.callstatic('utility','Wait',2.0)                                    # let her join the companion system first
        for st,(who,k) in PENDING.items():
            d=f.call(q,'GetStageDone',st);f.jmpf(d,'skip%d'%st);f.callself('React',KW[(who,k)]);f.label('skip%d'%st)
    f=sc.func('Frag_Met',[('akSpeakerRef','objectreference')]);met(f,100)
    f=sc.func('Frag_MetAlone',[('akSpeakerRef','objectreference')]);met(f,110)
    f=sc.func('Frag_AtVault',[('akSpeakerRef','objectreference')]);q=f.call('self','GetOwningQuest');f.call(q,'SetStage',150)
    for oc in (100,200,300,400):
        f=sc.func('Frag_Out%d'%oc,[('akSpeakerRef','objectreference')])
        q=f.call('self','GetOwningQuest')
        f.call(SLQ,'SetObjectiveCompleted',20,True);f.call(SLQ,'SetStage',40)  # complete Cold Comfort
        f.call(q,'SetObjectiveCompleted',10,True);f.call(q,'SetStage',500)
        f.call(PH,'SetStage',oc)
    pexw.write(sc.module(),out)

def quest_script(out):
    """NN_P1ScenesScript: starts S1C when the two Noras first get close, SK after the kill, SNT after the note."""
    sc=Script('NN_P1ScenesScript','Quest','Nora and Nora: Phase 1 scene starter.')
    SYN=sc.prop('SynthNoraRef','objectreference');NOR=sc.prop('NoraRef','objectreference');PH=sc.prop('Phase1','quest')
    FAC=sc.prop('CompanionFaction','faction');S1C=sc.prop('SceneFirstTogether','scene');SK=sc.prop('SceneAfterKill','scene');SNT=sc.prop('SceneNote','scene')
    EX=[sc.prop('SceneExchange%d'%i,'scene') for i in (1,2,3)];NEXT=sc.var('NextExchange','Int',0)
    f=sc.func('NoraWithPlayer',[],'Bool')
    a=f.cast(NOR,'actor');r=f.call(a,'IsInFaction',FAC);f.ret(r)
    f=sc.func('OnQuestInit')
    so=f.cast(PH,'ScriptObject');f.call('self','RegisterForRemoteEvent',so,S('OnStageSet'))
    f=sc.func('OnStageSet',[('auiStageID','Int'),('auiItemID','Int')])
    c=f.cmp('cmp_eq','auiStageID',100);f.jmpf(c,'not100')
    f.call('self','StartTimerGameTime',20.0,1);f.ret()                   # road exchanges: about once a game day
    f.label('not100')
    c=f.cmp('cmp_eq','auiStageID',110);f.jmpf(c,'end')
    o1=f.cast(SYN,'ScriptObject');o2=f.cast(NOR,'ScriptObject');f.call('self','RegisterForDistanceLessThanEvent',o1,o2,1000.0)
    f.label('end')
    f=sc.func('OnDistanceLessThan',[('akObj1','objectreference'),('akObj2','objectreference'),('afDistance','Float')])
    d=f.call('self','GetStageDone',100);f.jmpt(d,'stop')
    p=f.call(S1C,'IsPlaying');f.jmpt(p,'end');f.call(S1C,'Start')
    f.label('stop');o1=f.cast(SYN,'ScriptObject');o2=f.cast(NOR,'ScriptObject');f.call('self','UnregisterForDistanceEvents',o1,o2)
    f.label('end')
    f=sc.func('::remote_Quest_OnStageSet',[('akSender','quest'),('auiStageID','Int'),('auiItemID','Int')])
    c=f.cmp('cmp_eq','auiStageID',300);f.jmpf(c,'n300')
    a=f.cast(SYN,'actor');so=f.cast(a,'ScriptObject');f.call('self','RegisterForRemoteEvent',so,S('OnDeath'));f.ret()
    f.label('n300');c=f.cmp('cmp_eq','auiStageID',430);f.jmpf(c,'end')
    w=f.callself('NoraWithPlayer');f.jmpf(w,'end');f.call(SNT,'Start')
    f.label('end')
    # Event OnTimerGameTime: play the next road exchange if still on the way to the vault and both Noras are along
    f=sc.func('OnTimerGameTime',[('aiTimerID','Int')])
    d=f.call('self','GetStageDone',150);f.jmpt(d,'end')
    c=f.cmp('cmp_gt',NEXT,2);f.jmpt(c,'end')
    w=f.callself('NoraWithPlayer');f.jmpf(w,'again')
    for i in range(3):
        c=f.cmp('cmp_eq',NEXT,i);f.jmpf(c,'ex%d'%(i+1));f.call(EX[i],'Start');f.jmp('bump')
        f.label('ex%d'%(i+1))
    f.label('bump');f.op('iadd',NEXT,NEXT,1)
    f.label('again');f.call('self','StartTimerGameTime',20.0,1)
    f.label('end')
    f=sc.func('::remote_Actor_OnDeath',[('akSender','actor'),('akKiller','actor')])
    w=f.callself('NoraWithPlayer');f.jmpf(w,'end');f.call(SK,'Start')
    f.label('end')
    pexw.write(sc.module(),out)

def build_records(own,ns_idx,sl_idx,script_md,voice_csv):
    O=lambda i:(own<<24)|i
    L,C=parse_script(script_md);V=voice_ids(voice_csv)
    Q=O(QUEST);D=Dialogue(Q)
    nxt={'topic':0x809,'nate':0xA00,'scene':0x8E0}
    def alloc(k): v=nxt[k];nxt[k]+=1;return O(v)
    props=[('Phase1',vm_obj(O(PH1))),('SLQuest',vm_obj((sl_idx<<24)|SL_QUEST))]
    props+=[('Synth'+k,vm_obj((sl_idx<<24)|v)) for k,v in SL_KW.items()]+[('Nora'+k,vm_obj((ns_idx<<24)|v)) for k,v in NS_KW.items()]
    def fr(func): return frag_vmad(TIF,func,props)
    npc_topic={}
    def npc(lid,frag=None):
        """Topic with one spoken line (reused if already made)."""
        key=(lid,frag)
        if key in npc_topic: return npc_topic[key]
        ln=L[lid];iid,emo=V[lid]
        info=D.info(O(iid&0xFFFF),ln['text'],emotion_for(ln['delivery'],emo),vmad=fr(frag) if frag else None)
        t=D.topic(alloc('topic'),'SCEN',[info]);npc_topic[key]=t;return t
    def player(cid,frag=None):
        c=C[cid];info=D.info(alloc('nate'),c['line'],EMO['neutral'],prompt=c['label'],vmad=fr(frag) if frag else None)
        return D.topic(alloc('topic'),'SCEN',[info])
    nora_with=cond(GetInFaction,COMPANION_FACTION,0,'==',1.0,RUN_REF,(ns_idx<<24)|NS_NORA_REF)
    nora_away=cond(GetInFaction,COMPANION_FACTION,0,'==',0.0,RUN_REF,(ns_idx<<24)|NS_NORA_REF)
    done=lambda st,val=1.0,OR=False: cond(GetStageDone,Q,st,'==',val,OR=OR)
    scenes=[]
    def new_scene(edid,actors=(A_SYNTH,A_NORA),optional=()): s=Scene(alloc('scene'),edid,Q,list(actors),optional);scenes.append(s);return s
    def say(s,alias,lid,cnd=b'',frag=None,name=None):
        ph=s.phase(name or lid,cnd);s.line(alias,npc(lid,frag),ph);return ph
    SY,NO=A_SYNTH,A_NORA
    # ---------- Scene S1 / S1C: the confrontation (shared phases) ----------
    def confrontation(s,first_cond,end_frag):
        say(s,NO,'P1-S1-030',first_cond)
        for lid,al in [('P1-S1-031',SY),('P1-S1-032',SY),('P1-S1-033',NO),('P1-S1-034',SY),('P1-S1-035',NO),('P1-S1-036',SY),('P1-S1-037',NO),('P1-S1-038',SY)]:
            say(s,al,lid,first_cond)
        ph=s.phase('Choice2',first_cond);s.choice(SY,ph,[player('P1-S1-040'),player('P1-S1-041','Frag_51'),player('P1-S1-042'),player('P1-S1-043')],[npc(x) for x in ('P1-S1-050','P1-S1-051','P1-S1-052','P1-S1-053')])
        for lid,al in [('P1-S1-060',SY),('P1-S1-061',NO),('P1-S1-062',SY)]: say(s,al,lid,first_cond)
        ph=s.phase('Choice3',first_cond)
        s.choice(SY,ph,[player('P1-S1-070','Frag_52'),player('P1-S1-071','Frag_53'),player('P1-S1-072'),player('P1-S1-073','Frag_73')],[npc('P1-S1-075'),npc('P1-S1-075'),npc('P1-S1-075'),0])
        say(s,NO,'P1-S1-074',first_cond+done(73),name='AskNora')
        say(s,SY,'P1-S1-075',first_cond+done(73),name='AskNoraThanks')
        say(s,NO,'P1-S1-076',first_cond,frag=end_frag)
    s1=new_scene('NN_P1_S1_DiamondCity',optional=(A_NORA,))                 # real Nora may not be with you (1B)
    say(s1,SY,'P1-S1-002',name='Start');say(s1,SY,'P1-S1-003')
    ph=s1.phase('Choice1',nora_with)
    s1.choice(SY,ph,[player(x) for x in ('P1-S1-010','P1-S1-011','P1-S1-012','P1-S1-013')],[npc(x) for x in ('P1-S1-020','P1-S1-021','P1-S1-022','P1-S1-023')])
    confrontation(s1,nora_with,'Frag_Met')
    # 1B: real Nora not with you
    def nate_line(lid,frag=None):
        ln=L[lid];info=D.info(alloc('nate'),ln['text'],EMO['neutral'],prompt=ln['text'],vmad=fr(frag) if frag else None)
        return D.topic(alloc('topic'),'SCEN',[info])
    ph=s1.phase('Alone1',nora_away);s1.choice(SY,ph,[nate_line('P1-S1B-001'),0,0,0],[npc('P1-S1B-002'),0,0,0])
    ph=s1.phase('Alone2',nora_away);s1.choice(SY,ph,[nate_line('P1-S1B-003'),0,0,0],[npc('P1-S1B-004','Frag_MetAlone'),0,0,0])
    s1.package(SY,STAY_PACKAGE,0,len(s1.phases)-1);s1.package(NO,STAY_PACKAGE,0,len(s1.phases)-1)
    # S1C: first time together after meeting alone
    s1c=new_scene('NN_P1_S1C_FirstTogether')
    say(s1c,SY,'P1-S1C-001',name='Start');say(s1c,SY,'P1-S1C-002')
    confrontation(s1c,b'','Frag_Met')
    s1c.package(SY,STAY_PACKAGE,0,len(s1c.phases)-1);s1c.package(NO,STAY_PACKAGE,0,len(s1c.phases)-1)
    # ---------- Scene S2: Vault 111 ----------
    s2=new_scene('NN_P1_S2_Vault111')
    say(s2,SY,'P1-S2-002',name='Start')
    for lid,al in [('P1-S2-003',SY),('P1-S2-004',NO),('P1-S2-005',NO),('P1-S2-006',NO),('P1-S2-007',SY),('P1-S2-008',SY),('P1-S2-009',SY)]: say(s2,al,lid)
    ph=s2.phase('Comfort');s2.choice(SY,ph,[player('P1-S2-010','Aff_S2_010'),player('P1-S2-011','Aff_S2_011'),player('P1-S2-012'),player('P1-S2-013')])
    for lid,al in [('P1-S2-020',SY),('P1-S2-021',SY),('P1-S2-022',SY),('P1-S2-030',NO),('P1-S2-031',NO),('P1-S2-032',NO),('P1-S2-033',NO),('P1-S2-034',NO),('P1-S3-001',SY)]: say(s2,al,lid)
    ph=s2.phase('TheChoice')
    s2.choice(SY,ph,[player('P1-S3-010','Frag_31'),player('P1-S3-012','Frag_33'),player('P1-S3-013','Frag_34'),player('P1-S3-011','Frag_32')])
    # choice 4: plead, then confirm (X confirms; anything else switches)
    say(s2,SY,'P1-S3-050',done(34),name='Plead');say(s2,SY,'P1-S3-051',done(34))
    ph=s2.phase('Confirm',done(34))
    s2.choice(SY,ph,[player('P1-S3-010','Frag_41'),player('P1-S3-012','Frag_43'),player_confirm(C,D,alloc,fr) ,player('P1-S3-011','Frag_42')])
    c1=done(31,OR=True)+done(41);c2=done(32,OR=True)+done(42);c3=done(33,OR=True)+done(43);c4=done(44)
    say(s2,SY,'P1-S3-020',c1,name='C1');say(s2,NO,'P1-S3-021',c1);say(s2,SY,'P1-S3-022',c1,frag='Frag_Out100')
    say(s2,SY,'P1-S3-030',c2,name='C2');say(s2,NO,'P1-S3-031',c2,frag='Frag_Out200')
    say(s2,NO,'P1-S3-040',c3,name='C3');say(s2,SY,'P1-S3-041',c3,frag='Frag_Out300')
    say(s2,NO,'P1-S3-060',c4,name='C4');say(s2,SY,'P1-S3-061',c4,frag='Frag_Out400')
    s2.package(SY,STAY_PACKAGE,0,len(s2.phases)-1);s2.package(NO,STAY_PACKAGE,0,len(s2.phases)-1)
    # ---------- After the kill / after the note ----------
    exch=[]
    for i,seq in enumerate([[('P1-AM-030',A_SYNTH),('P1-AM-031',A_NORA),('P1-AM-032',A_SYNTH)],
                            [('P1-AM-040',A_SYNTH),('P1-AM-041',A_NORA)],
                            [('P1-AM-050',A_SYNTH),('P1-AM-051',A_NORA),('P1-AM-052',A_SYNTH),('P1-AM-053',A_NORA)]]):
        sx=new_scene('NN_P1_SX%d_RoadExchange'%(i+1))
        for j,(lid,al) in enumerate(seq): say(sx,al,lid,name='Start' if j==0 else None)
        exch.append(sx)
    sk=new_scene('NN_P1_SK_AfterKill',actors=(A_NORA,));say(sk,NO,'P1-S3-045',name='Start');say(sk,NO,'P1-S3-046')
    snt=new_scene('NN_P1_SNT_Note',actors=(A_NORA,))
    say(snt,NO,'P1-NT-001',name='Start');say(snt,NO,'P1-NT-002');say(snt,NO,'P1-NT-003')
    ph=snt.phase('Answer');snt.choice(NO,ph,[player('P1-NT-010','Aff_NT_010'),player('P1-NT-011','Aff_NT_011'),player('P1-NT-012','Aff_NT_012'),player('P1-NT-013','Frag_13')])
    say(snt,NO,'P1-NT-020',done(13),name='Regret')
    # ---------- Greetings (quest priority 90 beats Synthetic Love's 71) ----------
    syn_is=cond(GetIsID,(sl_idx<<24)|SL_NORA_NPC,0,'==',1.0)
    nora_found=cond(GetStageDone,(ns_idx<<24)|NS_FIRSTMEET,20,'==',1.0)
    g1=D.info(O(V['P1-S1-001'][0]&0xFFFF),L['P1-S1-001']['text'],emotion_for(L['P1-S1-001']['delivery'],V['P1-S1-001'][1]),
              conds=syn_is+cond(GetStage,(sl_idx<<24)|SL_QUEST,0,'<',10.0)+nora_found+done(100,0.0)+done(110,0.0),start_scene=s1.fid,start_phase='Start')
    g2=D.info(O(V['P1-S2-001'][0]&0xFFFF),L['P1-S2-001']['text'],emotion_for(L['P1-S2-001']['delivery'],V['P1-S2-001'][1]),
              conds=syn_is+cond(GetStage,(sl_idx<<24)|SL_QUEST,0,'==',30.0)+done(100)+done(150,0.0)+nora_with,
              vmad=fr('Frag_AtVault'),start_scene=s2.fid,start_phase='Start')
    D.topic(alloc('topic'),'GREE',[g1,g2],edid='NN_P1_Greetings',priority=100.0)
    # ---------- Idle chatter on the road to the vault ----------
    idles=[]
    road=done(100)+done(150,0.0)
    for lid in ['P1-AM-001','P1-AM-002','P1-AM-003','P1-AM-004','P1-AM-005','P1-AM-010','P1-AM-011','P1-AM-012','P1-AM-013','P1-AM-014']:
        idles.append(D.info(O(V[lid][0]&0xFFFF),L[lid]['text'],emotion_for(L[lid]['delivery'],V[lid][1]),conds=syn_is+road,flags=0x0002))
    nora_is=cond(GetIsID,(ns_idx<<24)|0x000F9A,0,'==',1.0)
    for lid in ['P1-AM-020','P1-AM-021','P1-AM-022','P1-AM-023','P1-AM-024']:
        idles.append(D.info(O(V[lid][0]&0xFFFF),L[lid]['text'],emotion_for(L[lid]['delivery'],V[lid][1]),conds=nora_is+road,flags=0x0002))
    D.topic(alloc('topic'),'IDLE',idles,edid='NN_P1_RoadIdles')
    D.scenes=[s.build() for s in scenes]
    # ---------- Quest ----------
    qprops=[('SynthNoraRef',vm_obj((sl_idx<<24)|SL_NORA_REF)),('NoraRef',vm_obj((ns_idx<<24)|NS_NORA_REF)),('Phase1',vm_obj(O(PH1))),
            ('CompanionFaction',vm_obj(COMPANION_FACTION)),('SceneFirstTogether',vm_obj(s1c.fid)),('SceneAfterKill',vm_obj(sk.fid)),('SceneNote',vm_obj(snt.fid))]+[('SceneExchange%d'%(i+1),vm_obj(x.fid)) for i,x in enumerate(exch)]
    vm=struct.pack('<hhH',6,2,1)+ws('NN_P1ScenesScript')+struct.pack('<BH',0,len(qprops))+b''.join(ws(n)+v for n,v in qprops)
    stages=[13,31,32,33,34,41,42,43,44,51,52,53,73,100,110,150,500]
    q=sub('EDID',zs('NN_P1Scenes'))+sub('VMAD',vm)+sub('FULL',zs('Two Noras'))
    q+=sub('DNAM',struct.pack('<HBBII',0x0111,90,0,0,7))+sub('NEXT',b'')
    q+=b''.join(sub('INDX',struct.pack('<HBB',n,0,0))+sub('QSDT',b'\0') for n in stages)
    q+=sub('QOBJ',struct.pack('<H',10))+sub('FNAM',struct.pack('<I',0))+sub('NNAM',zs('Travel with Nora to Vault 111'))+sub('QSTA',struct.pack('<iII',A_SYNTH,0,0))
    q+=sub('ANAM',struct.pack('<I',2))
    for aid,name,ref in [(A_SYNTH,'SynthNora',(sl_idx<<24)|SL_NORA_REF),(A_NORA,'Nora',(ns_idx<<24)|NS_NORA_REF)]:
        q+=sub('ALST',struct.pack('<I',aid))+sub('ALID',zs(name))+sub('FNAM',struct.pack('<I',0x282))+sub('ALFR',struct.pack('<I',ref))+sub('VTCK',struct.pack('<I',0))+sub('ALED',b'')
    quest=record('QUST',Q,0,q)
    child=D.records()
    group=b'GRUP'+struct.pack('<I',24+len(child))+struct.pack('<I',Q)+struct.pack('<IHHHH',10,0,0,0,0)+child
    count=1+len(D.topics)+sum(len(i) for _,_,i in D.topics)+len(D.scenes)
    return quest+group,count,{'scenes':[(s.edid,s.fid,len(s.phases)) for s in scenes],'topics':len(D.topics),'nate':nxt['nate']-0xA00}

def player_confirm(C,D,alloc,fr):
    c=C['P1-S3-013'];info=D.info(alloc('nate'),"I'm sorry. I've made up my mind.",EMO['neutral'],prompt="I'm sure.",vmad=fr('Frag_44'))
    return D.topic(alloc('topic'),'SCEN',[info])
if __name__=='__main__':
    d=sys.argv[1];tif_script(os.path.join(d,TIF+'.pex'));quest_script(os.path.join(d,'NN_P1ScenesScript.pex'));print('scripts ok')
