"""Phase 2: relationship tiers 1-3 between the two Noras (docs/script/phase2-script.md).

Quest NN_Phase2 (0xB03) runs the tiers; NN_SynthNoraWalksBack (0xB04) walks synth Nora back to Vault 111.
Scripts:
  NN_Phase2Script  quest script: tier timers, gifts, talk queue, exchanges, stimpak aid, vault/leave outcomes, test-tape hooks
  NN_P2S_TIF       one TopicInfo script: choice fragments (globals, affinity reactions) that call NN_Phase2Script functions
Line IDs come from docs/script/phase2-voice-sheet.csv. Greetings that repeat a recorded line get their own INFO IDs;
build_records() returns which voice file each one copies (packaging duplicates the .fuz)."""
import sys,os,struct
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from build import sub,record,grup,zs,vm_obj,glob,book
from scenes_lib import Dialogue,Scene,cond,GetStage,GetStageDone,GetGlobalValue,GetIsID,frag_vmad,emotion_for,parse_script,voice_ids,EMO,ws
from pexasm import Script,S
import pexw

# ---------- form IDs (own plugin) ----------
P2Q=0xB03; WALKQ=0xB04
G={'CheckIn':0xB05,'Cruel':0xB06,'Stutter':0xB07,'Hurt':0xB08,'GiftType':0xB09,'T3Adjust':0xB0A,'T4Adjust':0xB0B,
   'Waiting':0xB0D,'GiftCount':0xB0E,'NextEventDay':0xB0F}
FL_AMMO,FL_JUNK,FL_RARE=0xB10,0xB11,0xB12
MSG_RETURNED,LEAVE_NOTE,MSG_NOTHING=0xB13,0xB14,0xB15
GREET_FIRST=0xBC0; SCENE_FIRST=0xBE0; TOPIC_FIRST=0xC00; NATE_FIRST=0xD00
NEXT_FREE=0xE00
# from Phase 1 (build.py)
PH1=0x802; TIER=0x804; IMPATIENT=0x805; WAITNOTE=0x806
VAULT_ANCHOR=0x0006FA30; SPOUSE_POD=0x0004A012; FOLLOWERS=0x000289E4
# other mods / vanilla
SL_NORA_REF=0x000FB3; SL_NORA_NPC=0x000F99; NS_NORA_REF=0x001735; NS_NORA_NPC=0x000F9A
SL_KW={'Likes':0x26CD,'Loves':0x26CE,'Dislikes':0x26CB,'Hates':0x26CC}
NS_KW={'Likes':0x1F32,'Loves':0x1F35,'Dislikes':0x1F33,'Hates':0x1F34}
CA_SIZE_SMALL=0x00018D00
TRAVEL_LINK02=0x00157AC9; LINK_CUSTOM02=0x0005D5E7; STAY_PACKAGE=0x00019AA2
HEALTH=0x000002D4; STIMPAK=0x00023736; RADAWAY=0x00023742; CAPS=0x0000000F
AMMO=[0x0001F276,0x0001F278,0x0001F673,0x000C1897,0x0001F66C,0x0009221C,0x0018ABDF]   # 10mm 5.56 shells fusion 5mm .44 2mmEC
SCREWS,SPRINGS,GEARS,CIRCUITRY,NUCLEAR,ADHESIVE=0x00069081,0x00069082,0x0006907E,0x0006907B,0x00069086,0x001BF72E
JUNK=[SCREWS,SPRINGS,0x0004D1F2,0x00059B25]            # screws, springs, duct tape, wonderglue
RARE=[GEARS,CIRCUITRY,NUCLEAR]
A_SYNTH,A_NORA=0,1
TIF='NN_P2S_TIF'; QS='NN_Phase2Script'
LEAVE_TEXT="Don't look for me.\r\n\r\nI know what I am to you. I'm going to go be something to somebody else.\r\n\r\nKeep her safe."
RETURNED_TEXT='Synth Nora has gone back to Vault 111.'
NOTHING_TEXT='Nothing more to advance yet. Tiers 4 and 5 come in a later phase.'

# timer IDs (game time unless noted)
T_GIFT,T_NGIFT,T_N1,T_TIER2,T_TIER3,T_EXCH,T_POLL,T_LEAVE,T_PATIENCE,T_VANISH=1,2,3,4,5,6,7,8,9,10
RT_AID,RT_THANKS=20,21          # real-time timers
POLL_H=0.1                      # 6 game minutes
# talk queue codes
Q_CK,Q_N1,Q_N2,Q_S3,Q_LV=1,2,3,4,5

def quest_script(out):
    sc=Script(QS,'Quest','Nora and Nora: Phase 2 relationship tiers 1-3.')
    P=lambda n,t: sc.prop(n,t)
    SYN=P('SynthNoraRef','objectreference');NOR=P('NoraRef','objectreference');PH=P('Phase1','quest');FOL=P('Followers','followersscript')
    GV={k:P(k,'globalvariable') for k in G};TIERG=P('Tier','globalvariable');IMP=P('Impatient','globalvariable')
    FA,FJ,FR=P('AmmoList','formlist'),P('JunkList','formlist'),P('RareJunkList','formlist')
    CAPSF,STIM,RAD=P('Caps','form'),P('Stimpak','form'),P('RadAway','form')
    SCREW,GEAR,CIRC,NUC,ADH=P('Screws','form'),P('Gears','form'),P('Circuitry','form'),P('NuclearMaterial','form'),P('Adhesive','form')
    WALK=P('WalkQuest','quest');ANCH=P('VaultAnchor','objectreference');POD=P('NoteAnchor','objectreference');LK=P('LinkKeyword','keyword')
    RET=P('ReturnedMsg','message');NOTHING=P('NothingMsg','message');LNOTE=P('LeaveNote','book');WNOTE=P('WaitNote','book');HP=P('HealthAV','actorvalue')
    SC={k:P('Scene'+k,'scene') for k in ('Gift','NoraGift','CheckIn','N1','N2','S3','Leave','AfterKill')}
    EX=[P('SceneEx%d'%i,'scene') for i in range(1,9)]      # tier1: 1-2, tier2: 3-5, tier3: 6-8
    TA,TN,THS,THN=P('TopicAidSynth','topic'),P('TopicAidNora','topic'),P('TopicThanksSynth','topic'),P('TopicThanksNora','topic')
    PEND=sc.var('Pending','Int',0);PG=sc.var('PendingGift','Bool',False);PNG=sc.var('PendingNoraGift','Bool',False)
    EXI=[sc.var('NextEx%d'%i,'Int',0) for i in (1,2,3)]
    AIDUSED=sc.var('AidUsed','Bool',False);NEXTAID=sc.var('NextAidTime','Float',0.0);LASTRECV=sc.var('LastAidReceiver','objectreference',None)

    def actor(f,r): return f.cast(r,'actor')
    def player(f): return f.callstatic('game','GetPlayer')
    # --- helpers ---
    f=sc.func('Near',[('akRef','objectreference')],'Bool')
    d=f.call('akRef','IsDisabled');f.jmpt(d,'no')
    a=f.cast('akRef','actor');x=f.call(a,'IsDead');f.jmpt(x,'no')
    pl=player(f);po=f.cast(pl,'objectreference');dist=f.call('akRef','GetDistance',po);c=f.cmp('cmp_lt',dist,1500.0);f.ret(c)
    f.label('no');f.ret(False)
    f=sc.func('CanTalk',[],'Bool')
    pl=player(f);c=f.call(pl,'IsInCombat');f.jmpt(c,'no')
    for r in (SYN,NOR):
        a=actor(f,r);x=f.call(a,'IsInScene');f.jmpt(x,'no')
    f.ret(True);f.label('no');f.ret(False)
    f=sc.func('Ended',[],'Bool')
    for st in (83,84,89,93,94):
        d=f.call('self','GetStageDone',st);f.jmpt(d,'yes')
    d=f.call(PH,'GetStageDone',410);f.jmpt(d,'yes');f.ret(False);f.label('yes');f.ret(True)
    f=sc.func('Timer',[('afHours','Float'),('aiID','Int')])          # start a timer and remember when it fires (test tape status)
    f.call('self','StartTimerGameTime','afHours','aiID')
    now=f.callstatic('utility','GetCurrentGameTime');d=f.tmp('Float');f.op('fdiv',d,'afHours',24.0);t=f.tmp('Float');f.op('fadd',t,now,d)
    f.call(GV['NextEventDay'],'SetValue',t)
    f=sc.func('Dismiss')
    a=actor(f,SYN);f.call(FOL,'DismissCompanion',a,False,True)
    f=sc.func('Release')
    f.callself('Dismiss');a=actor(f,SYN);f.call(a,'DisallowCompanion',True)
    f=sc.func('WalkBack')                                             # walk to the cryo pods (travel package to linked ref)
    f.call(SYN,'SetLinkedRef',ANCH,LK);f.call(WALK,'Start');a=actor(f,SYN);f.call(a,'EvaluatePackage',False)
    f.call(RET,'Show',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);f.call('self','SetObjectiveDisplayed',20,True,False)
    f=sc.func('StopWalk')
    f.call(WALK,'Stop');a=actor(f,SYN);f.call(a,'EvaluatePackage',False)
    # --- tier start ---
    f=sc.func('BeginTier1')
    d=f.call('self','GetStageDone',10);f.jmpt(d,'end')
    f.call('self','SetStage',10);f.call(TIERG,'SetValue',1.0)
    f.call('self','StartTimerGameTime',24.0,T_GIFT);f.call('self','StartTimerGameTime',20.0,T_EXCH);f.call('self','StartTimerGameTime',POLL_H,T_POLL)
    f.label('end')
    f=sc.func('TierTwo')
    f.call(TIERG,'SetValue',2.0);f.call('self','SetStage',40);f.op('assign',PEND,Q_N2)
    f=sc.func('TierThree')
    f.call(TIERG,'SetValue',3.0);f.call('self','SetStage',60);f.op('assign',PEND,Q_S3)
    # --- called by dialogue fragments ---
    f=sc.func('CheckInDone')
    f.call('self','SetStage',20);f.callself('Timer',48.0,T_N1)
    f=sc.func('N1Done')
    f.call('self','SetStage',30);f.callself('Timer',48.0,T_TIER2)
    v=f.call(GV['CheckIn'],'GetValue');c=f.cmp('cmp_eq',v,3.0);f.jmpf(c,'end')
    f.call('self','StartTimerGameTime',48.0,T_NGIFT);f.label('end')
    f=sc.func('N2Done')
    d=f.call('self','GetStageDone',50);f.jmpt(d,'end')
    f.call('self','SetStage',50)
    adj=f.call(GV['T3Adjust'],'GetValue');h=f.tmp('Float');f.op('fmul',h,adj,24.0);hh=f.tmp('Float');f.op('fadd',hh,h,72.0)
    c=f.cmp('cmp_lt',hh,24.0);f.jmpf(c,'go');f.op('assign',hh,24.0)
    f.label('go');f.callself('Timer',hh,T_TIER3)
    f.label('end')
    f=sc.func('S3Done')
    f.call('self','SetStage',70);f.call(GV['Stutter'],'SetValue',0.0)
    f=sc.func('HurtUp')                                               # a Hate from synth Nora in a Phase 2 scene
    v=f.call(GV['Hurt'],'Mod',1.0);c=f.cmp('cmp_ge',v,3.0);f.jmpf(c,'end')
    for st in (66,82,83,84):
        d=f.call('self','GetStageDone',st);f.jmpt(d,'end')
    f.call('self','SetStage',88);f.op('assign',PEND,Q_LV)
    f.label('end')
    f=sc.func('Outcome',[('aiCode','Int')])                           # Vault 111 choice re-opened: 81-84 (tier 3 talk), 91-94 (at the vault)
    f.call('self','SetStage','aiCode')
    d=f.call('self','GetStageDone',70);f.jmpt(d,'s');f.call('self','SetStage',70)
    f.label('s')
    m=f.tmp('Int');f.op('imod',m,'aiCode',10)
    c=f.cmp('cmp_eq',m,1);f.jmpt(c,'come');c=f.cmp('cmp_eq',m,2);f.jmpt(c,'time')
    c=f.cmp('cmp_eq',m,3);f.jmpt(c,'abom');c=f.cmp('cmp_eq',m,4);f.jmpt(c,'away');f.ret()
    f.label('come')
    w=f.call(GV['Waiting'],'GetValue');c=f.cmp('cmp_gt',w,0.0);f.jmpf(c,'end')
    f.call(GV['Waiting'],'SetValue',0.0);f.callself('StopWalk');f.call('self','CancelTimerGameTime',T_PATIENCE)
    f.call('self','SetObjectiveCompleted',20,True);a=actor(f,SYN);f.call(a,'SetCompanion',True,True);f.ret()
    f.label('time')
    w=f.call(GV['Waiting'],'GetValue');c=f.cmp('cmp_gt',w,0.0);f.jmpt(c,'end')       # already waiting there
    f.callself('Dismiss');f.call(GV['Waiting'],'SetValue',1.0);f.callself('WalkBack')
    v=f.call(IMP,'GetValue');c=f.cmp('cmp_gt',v,0.0);f.jmpf(c,'end');f.callself('Timer',168.0,T_PATIENCE);f.ret()
    f.label('abom')
    f.call(GV['Waiting'],'SetValue',0.0);f.callself('StopWalk');f.call('self','CancelTimerGameTime',T_PATIENCE);f.callself('Release')
    f.call('self','SetObjectiveDisplayed',20,False,False)
    a=actor(f,SYN);b=f.call(a,'GetActorBase');f.call(b,'SetEssential',False);f.call(b,'SetProtected',False)
    so=f.cast(a,'ScriptObject');f.call('self','RegisterForRemoteEvent',so,S('OnDeath'))
    f.call(a,'RemoveFromAllFactions');pl=player(f);f.call(a,'StartCombat',pl,True);f.ret()
    f.label('away')
    f.call(GV['Waiting'],'SetValue',0.0);f.call('self','CancelTimerGameTime',T_PATIENCE);f.callself('Release');f.callself('WalkBack')
    f.callself('Timer',72.0,T_LEAVE)
    f.label('end')
    f=sc.func('LeaveDone')                                            # hurt counter reached 3: she leaves on her own
    f.call('self','SetStage',89);f.callself('Release')
    pl=player(f);f.call(pl,'AddItem',LNOTE,1,False)
    f.call('self','StartTimerGameTime',1.0,T_VANISH);f.callself('Timer',72.0,T_LEAVE)
    # --- gifts ---
    f=sc.func('Give',[('akItem','form'),('aiCount','Int')])
    pl=player(f);f.call(pl,'AddItem','akItem','aiCount',False)
    f=sc.func('PickAmmo',[],'form')                                   # the ammo you carry most of (vanilla Papyrus can't read a weapon's ammo)
    best=f.local('best','form');bc=f.local('bc','Int');i=f.local('i','Int');n=f.call(FA,'GetSize')
    f.op('assign',bc,-1);f.op('assign',i,0);f.op('assign',best,None)
    f.label('loop');c=f.cmp('cmp_lt',i,n);f.jmpf(c,'done')
    it=f.call(FA,'GetAt',i);pl=player(f);k=f.call(pl,'GetItemCount',it);c2=f.cmp('cmp_gt',k,bc);f.jmpf(c2,'next')
    f.op('assign',bc,k);f.op('assign',best,it)
    f.label('next');f.op('iadd',i,i,1);f.jmp('loop')
    f.label('done');f.ret(best)
    f=sc.func('GiveGeneric',[('aiType','Int')])
    for t,lab in [(1,'g1'),(2,'g2'),(3,'g3'),(4,'g4'),(5,'g5')]:
        c=f.cmp('cmp_eq','aiType',t);f.jmpt(c,lab)
    f.ret()
    f.label('g1');a=f.callself('PickAmmo');r=f.callstatic('utility','RandomInt',10,25);f.callself('Give',a,r);f.ret()
    f.label('g2');r=f.callstatic('utility','RandomInt',0,1);c=f.cmp('cmp_eq',r,0);f.jmpf(c,'rad');f.callself('Give',STIM,2);f.ret()
    f.label('rad');f.callself('Give',RAD,1);f.ret()
    f.label('g3');r=f.callstatic('utility','RandomInt',15,40);f.callself('Give',CAPSF,r);f.ret()
    f.label('g4');f.callself('Give',SCREW,2);f.callself('Give',ADH,1);f.ret()
    f.label('g5');n=f.call(FR,'GetSize');m=f.tmp('Int');f.op('isub',m,n,1);r=f.callstatic('utility','RandomInt',0,m);it=f.call(FR,'GetAt',r);f.callself('Give',it,1)
    f=sc.func('GiveGift')
    ci=f.call(GV['CheckIn'],'GetValue')
    c=f.cmp('cmp_eq',ci,3.0);f.jmpt(c,'rare')
    t=f.callstatic('utility','RandomInt',1,5);tf=f.cast(t,'Float');f.call(GV['GiftType'],'SetValue',tf);f.callself('GiveGeneric',t);f.jmp('count')
    f.label('rare')                                                  # "favouring rare junk": type 6 = gears + circuitry, 7 = nuclear material
    r=f.callstatic('utility','RandomInt',6,7);rf=f.cast(r,'Float');f.call(GV['GiftType'],'SetValue',rf)
    c=f.cmp('cmp_eq',r,6);f.jmpf(c,'nuc');f.callself('Give',GEAR,2);f.callself('Give',CIRC,1);f.jmp('count')
    f.label('nuc');f.callself('Give',NUC,1)
    f.label('count')
    f.call(SC['Gift'],'Start')
    n=f.call(GV['GiftCount'],'Mod',1.0);c=f.cmp('cmp_ge',n,5.0);f.jmpf(c,'end')
    d=f.call('self','GetStageDone',20);f.jmpt(d,'end')
    c=f.cmp('cmp_eq',PEND,0);f.jmpf(c,'end');f.op('assign',PEND,Q_CK)
    f.label('end')
    # --- talk queue / poll ---
    f=sc.func('TryTalk',[],'Bool')
    for q,scene,who in [(Q_CK,'CheckIn',SYN),(Q_N1,'N1',NOR),(Q_N2,'N2',NOR),(Q_S3,'S3',SYN),(Q_LV,'Leave',SYN)]:
        c=f.cmp('cmp_eq',PEND,q);f.jmpf(c,'n%d'%q)
        nr=f.callself('Near',who);f.jmpf(nr,'no')
        f.call(SC[scene],'Start');f.op('assign',PEND,0);f.ret(True)
        f.label('n%d'%q)
    f.label('no');f.ret(False)
    f=sc.func('Poll')
    e=f.callself('Ended');f.jmpt(e,'end')
    f.call('self','StartTimerGameTime',POLL_H,T_POLL)
    ok=f.callself('CanTalk');f.jmpf(ok,'end')
    c=f.cmp('cmp_gt',PEND,0);f.jmpf(c,'gifts');f.callself('TryTalk');f.ret()
    f.label('gifts')
    w=f.call(GV['Waiting'],'GetValue');c=f.cmp('cmp_gt',w,0.0);f.jmpt(c,'end')
    f.jmpf(PG,'ngift');nr=f.callself('Near',SYN);f.jmpf(nr,'ngift');f.op('assign',PG,False);f.callself('GiveGift');f.ret()
    f.label('ngift')
    f.jmpf(PNG,'end');nr=f.callself('Near',NOR);f.jmpf(nr,'end');f.op('assign',PNG,False)
    f.callself('Give',SCREW,2);f.callself('Give',GEAR,1);f.call(SC['NoraGift'],'Start')
    f.label('end')
    f=sc.func('Exchange')
    e=f.callself('Ended');f.jmpt(e,'end')
    f.call('self','StartTimerGameTime',20.0,T_EXCH)
    ok=f.callself('CanTalk');f.jmpf(ok,'end')
    for r in (SYN,NOR):
        nr=f.callself('Near',r);f.jmpf(nr,'end')
    w=f.call(GV['Waiting'],'GetValue');c=f.cmp('cmp_gt',w,0.0);f.jmpt(c,'end')
    t=f.call(TIERG,'GetValue')
    for tier,(lo,cnt) in [(1,(0,2)),(2,(2,3)),(3,(5,3))]:
        c=f.cmp('cmp_eq',t,float(tier));f.jmpf(c,'t%d'%tier)
        idx=EXI[tier-1]
        for k in range(cnt):
            c2=f.cmp('cmp_eq',idx,k);f.jmpf(c2,'t%dk%d'%(tier,k));f.call(EX[lo+k],'Start');f.label('t%dk%d'%(tier,k))
        f.op('iadd',idx,idx,1);c3=f.cmp('cmp_ge',idx,cnt);f.jmpf(c3,'end');f.op('assign',idx,0);f.ret()
        f.label('t%d'%tier)
    f.label('end')
    # --- events ---
    f=sc.func('OnQuestInit')
    so=f.cast(PH,'ScriptObject');f.call('self','RegisterForRemoteEvent',so,S('OnStageSet'))
    for r in (SYN,NOR):
        a=actor(f,r);so=f.cast(a,'ScriptObject');f.call('self','RegisterForRemoteEvent',so,S('OnCombatStateChanged'))
    d=f.call(PH,'GetStageDone',100);f.jmpf(d,'end');f.callself('BeginTier1');f.label('end')
    f=sc.func('::remote_Quest_OnStageSet',[('akSender','quest'),('auiStageID','Int'),('auiItemID','Int')])
    c=f.cmp('cmp_eq','auiStageID',100);f.jmpf(c,'end');f.callself('BeginTier1');f.label('end')
    f=sc.func('::remote_Actor_OnDeath',[('akSender','actor'),('akKiller','actor')])
    nr=f.callself('Near',NOR);f.jmpf(nr,'end');f.call(SC['AfterKill'],'Start');f.label('end')
    f=sc.func('::remote_Actor_OnCombatStateChanged',[('akSender','actor'),('akTarget','actor'),('aeCombatState','Int')])
    c=f.cmp('cmp_eq','aeCombatState',0);f.jmpt(c,'end')
    t=f.call(TIERG,'GetValue');c=f.cmp('cmp_ge',t,3.0);f.jmpf(c,'end')
    f.op('assign',AIDUSED,False);f.call('self','StartTimer',2.0,RT_AID)
    f.label('end')
    f=sc.func('TryAid',[('akGiver','objectreference'),('akRecv','objectreference'),('akTopic','topic')],'Bool')
    f.jmpt(AIDUSED,'no')
    for r in ('akGiver','akRecv'):
        nr=f.callself('Near',r);f.jmpf(nr,'no')
    ra=f.cast('akRecv','actor');pc=f.call(ra,'GetValuePercentage',HP);c=f.cmp('cmp_lt',pc,0.35);f.jmpf(c,'no')
    k=f.call('akGiver','GetItemCount',STIM);c=f.cmp('cmp_gt',k,0);f.jmpf(c,'no')
    now=f.callstatic('utility','GetCurrentGameTime');c=f.cmp('cmp_lt',now,NEXTAID);f.jmpt(c,'no')
    f.call('akGiver','RemoveItem',STIM,1,True,'akRecv');f.call(ra,'EquipItem',STIM,False,True)
    f.call('akGiver','Say','akTopic',None,False,None)
    f.op('assign',AIDUSED,True);t=f.tmp('Float');f.op('fadd',t,now,0.0035);f.op('assign',NEXTAID,t)   # 5 game minutes
    f.op('assign',LASTRECV,'akRecv');f.call('self','StartTimer',2.5,RT_THANKS);f.ret(True)
    f.label('no');f.ret(False)
    f=sc.func('OnTimer',[('aiTimerID','Int')])
    c=f.cmp('cmp_eq','aiTimerID',RT_THANKS);f.jmpf(c,'aid')
    c=f.cmp('cmp_eq',LASTRECV,SYN);f.jmpf(c,'tn');f.call(SYN,'Say',THS,None,False,None);f.ret()
    f.label('tn');f.call(NOR,'Say',THN,None,False,None);f.ret()
    f.label('aid')
    sa=actor(f,SYN);na=actor(f,NOR);c1=f.call(sa,'IsInCombat');c2=f.call(na,'IsInCombat');o=f.tmp('Bool');f.op('assign',o,c1)
    f.jmpt(o,'go');f.op('assign',o,c2);f.jmpf(o,'end')
    f.label('go')
    r=f.callself('TryAid',SYN,NOR,TA);f.jmpt(r,'again');f.callself('TryAid',NOR,SYN,TN)
    f.label('again');f.call('self','StartTimer',2.0,RT_AID)
    f.label('end')
    f=sc.func('OnTimerGameTime',[('aiTimerID','Int')])
    for tid,lab in [(T_GIFT,'gift'),(T_NGIFT,'ngift'),(T_N1,'n1'),(T_TIER2,'t2'),(T_TIER3,'t3'),(T_EXCH,'ex'),(T_POLL,'poll'),(T_LEAVE,'leave'),(T_PATIENCE,'pat'),(T_VANISH,'van')]:
        c=f.cmp('cmp_eq','aiTimerID',tid);f.jmpt(c,lab)
    f.ret()
    f.label('gift');e=f.callself('Ended');f.jmpt(e,'end')
    ci=f.call(GV['CheckIn'],'GetValue');c=f.cmp('cmp_eq',ci,1.0);f.jmpt(c,'end')     # "actions, not things": gifts stop
    f.op('assign',PG,True);f.call('self','StartTimerGameTime',24.0,T_GIFT);f.ret()
    f.label('ngift');e=f.callself('Ended');f.jmpt(e,'end');f.op('assign',PNG,True);f.call('self','StartTimerGameTime',48.0,T_NGIFT);f.ret()
    f.label('n1');f.op('assign',PEND,Q_N1);f.ret()
    f.label('t2');f.callself('TierTwo');f.ret()
    f.label('t3');f.callself('TierThree');f.ret()
    f.label('ex');f.callself('Exchange');f.ret()
    f.label('poll');f.callself('Poll');f.ret()
    f.label('leave');f.callself('StopWalk');f.call('self','SetObjectiveDisplayed',20,False,False)
    f.call(PH,'SetStage',410);f.call(PH,'SetStage',420);f.ret()
    f.label('pat')
    w=f.call(GV['Waiting'],'GetValue');c=f.cmp('cmp_gt',w,0.0);f.jmpf(c,'end')
    f.call(POD,'PlaceAtMe',WNOTE,1,True,False,False);f.call(GV['Waiting'],'SetValue',0.0);f.callself('Release')
    f.call('self','SetStage',94);f.callself('Timer',72.0,T_LEAVE);f.ret()
    f.label('van');f.call(PH,'SetStage',410)
    f.label('end')
    # --- test tape ---
    f=sc.func('DebugAdvance',[],'Bool')
    d=f.call('self','GetStageDone',10);f.jmpt(d,'a1');f.callself('BeginTier1');f.ret(True)
    f.label('a1');d=f.call('self','GetStageDone',20);f.jmpt(d,'a2')
    f.call(GV['GiftCount'],'SetValue',5.0);f.op('assign',PEND,Q_CK);f.ret(True)
    f.label('a2');d=f.call('self','GetStageDone',30);f.jmpt(d,'a3');f.call('self','CancelTimerGameTime',T_N1);f.op('assign',PEND,Q_N1);f.ret(True)
    f.label('a3');d=f.call('self','GetStageDone',40);f.jmpt(d,'a4');f.call('self','CancelTimerGameTime',T_TIER2);f.callself('TierTwo');f.ret(True)
    f.label('a4');d=f.call('self','GetStageDone',50);f.jmpt(d,'a5');f.op('assign',PEND,Q_N2);f.ret(True)
    f.label('a5');d=f.call('self','GetStageDone',60);f.jmpt(d,'a6');f.call('self','CancelTimerGameTime',T_TIER3);f.callself('TierThree');f.ret(True)
    f.label('a6');d=f.call('self','GetStageDone',70);f.jmpt(d,'none');f.op('assign',PEND,Q_S3);f.ret(True)
    f.label('none');f.call(NOTHING,'Show',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);f.ret(False)
    f=sc.func('DebugSkipWait')
    w=f.call(GV['Waiting'],'GetValue');c=f.cmp('cmp_gt',w,0.0);f.jmpf(c,'lv')
    v=f.call(IMP,'GetValue');c=f.cmp('cmp_gt',v,0.0);f.jmpf(c,'adv')
    f.call('self','CancelTimerGameTime',T_PATIENCE);f.call('self','OnTimerGameTime',T_PATIENCE);f.ret()
    f.label('lv')
    for st in (84,89,94):
        d=f.call('self','GetStageDone',st);f.jmpt(d,'leave')
    f.jmp('adv')
    f.label('leave');d=f.call(PH,'GetStageDone',420);f.jmpt(d,'adv')
    f.call('self','CancelTimerGameTime',T_LEAVE);f.call('self','OnTimerGameTime',T_LEAVE);f.ret()
    f.label('adv');f.callself('DebugAdvance')
    f=sc.func('DebugSetTier',[('aiTier','Int')])
    f.callself('BeginTier1')
    c=f.cmp('cmp_ge','aiTier',2);f.jmpf(c,'set')
    ci=f.call(GV['CheckIn'],'GetValue');c=f.cmp('cmp_eq',ci,0.0);f.jmpf(c,'s2');f.call(GV['CheckIn'],'SetValue',2.0)
    f.label('s2')
    for st in (20,30,40,50): f.call('self','SetStage',st)
    for tid in (T_N1,T_TIER2,T_TIER3): f.call('self','CancelTimerGameTime',tid)
    f.op('assign',PEND,0)
    c=f.cmp('cmp_ge','aiTier',3);f.jmpt(c,'s3');f.callself('Timer',72.0,T_TIER3);f.jmp('set')
    f.label('s3')
    for st in (60,70): f.call('self','SetStage',st)
    f.label('set');tf=f.cast('aiTier','Float');f.call(TIERG,'SetValue',tf)
    f=sc.func('DebugBringBoth')
    pl=player(f);po=f.cast(pl,'objectreference')
    for r in (SYN,NOR): f.call(r,'MoveTo',po,0.0,0.0,0.0,True)
    f=sc.func('DebugReset')
    for k in ('CheckIn','Cruel','Stutter','Hurt','GiftType','T3Adjust','T4Adjust','GiftCount','NextEventDay'): f.call(GV[k],'SetValue',0.0)
    for tid in (T_GIFT,T_NGIFT,T_N1,T_TIER2,T_TIER3,T_EXCH,T_POLL): f.call('self','CancelTimerGameTime',tid)
    f.call(TIERG,'SetValue',1.0);f.call('self','Stop');f.call('self','Reset');f.call('self','Start')
    pexw.write(sc.module(),out);return sc

# reactions per choice fragment: (who, event, size) ; 'hurt' = also count toward her leaving
REACT={
 'CK_1':[('Synth','Likes'),('Nora','Loves')],'CK_2':[('Synth','Likes')],'CK_3':[('Synth','Loves'),('Nora','Loves')],'CK_4':[('Synth','Dislikes'),('Nora','Dislikes')],
 'N2_P1':[('Nora','Likes')],'N2_P2':[('Nora','Likes'),('Synth','Likes')],'N2_P3':[('Synth','Dislikes')],'N2_P4':[('Nora','Dislikes'),('Synth','Hates')],
 'S3_Rude':[('Synth','Dislikes','small')],
 'S3C_1':[('Nora','Likes'),('Synth','Loves')],'S3C_2':[('Nora','Likes'),('Synth','Loves')],'S3C_3':[('Nora','Dislikes'),('Synth','Hates')],'S3C_4':[('Nora','Dislikes'),('Synth','Hates')],
 'S3K_1':[('Nora','Likes'),('Synth','Likes')],'S3K_2':[('Nora','Loves'),('Synth','Loves')],'S3K_3':[('Nora','Hates'),('Synth','Hates')],'S3K_4':[('Nora','Hates'),('Synth','Hates')],
 'RV_1':[('Nora','Likes'),('Synth','Likes')],'RV_3':[('Nora','Hates')],'RVW_1':[('Nora','Likes'),('Synth','Likes')],'RVW_3':[('Nora','Hates')]}
def tif_script(out):
    sc=Script(TIF,'TopicInfo','Nora and Nora: Phase 2 dialogue fragments.')
    GV={k:sc.prop(k,'globalvariable') for k in ('CheckIn','Cruel','Stutter','T3Adjust','T4Adjust')}
    KW={(w,k):sc.prop(w+k,'keyword') for w in ('Synth','Nora') for k in ('Likes','Loves','Dislikes','Hates')}
    SMALL=sc.prop('SizeSmall','globalvariable')
    f=sc.func('React',[('akEvent','keyword'),('akSize','globalvariable')])
    so=f.cast('self','ScriptObject');f.callstatic('followersscript','SendAffinityEvent',so,'akEvent',None,'akSize',True,True,False,1.0)
    def q2(f): q=f.call('self','GetOwningQuest');return f.cast(q,QS)
    def frag(name,body=None,react=True):
        f=sc.func(name,[('akSpeakerRef','objectreference')])
        if body: body(f)                                  # stage flags first, so HurtUp sees them
        for r in (REACT.get(name,[]) if react else []):
            f.callself('React',KW[(r[0],r[1])],SMALL if len(r)>2 else None)
            if r[0]=='Synth' and r[1]=='Hates' and not name.startswith('RV'): f.call(q2(f),'HurtUp')
        return f
    setg=lambda k,v: (lambda f: f.call(GV[k],'SetValue',float(v)))
    modg=lambda k,v: (lambda f: f.call(GV[k],'Mod',float(v)))
    stage=lambda st: (lambda f: f.call(f.call('self','GetOwningQuest'),'SetStage',st))
    def seq(*fs):
        def run(f):
            for x in fs: x(f)
        return run
    call=lambda fn,*a: (lambda f: f.call(q2(f),fn,*a))
    for i in (1,2,3,4): frag('CK_%d'%i,seq(setg('CheckIn',i),call('CheckInDone')))
    frag('N1_End',call('N1Done'))
    frag('N2_Later',stage(45))
    for i,extra in [(1,[]),(2,[modg('T3Adjust',-1)]),(3,[modg('T3Adjust',1)]),(4,[modg('T3Adjust',2),setg('Cruel',1)])]:
        frag('N2_P%d'%i,seq(stage(50+i),*extra))
    frag('N2_End',call('N2Done'))
    frag('S3_Later',stage(65))
    frag('S3_Rude',setg('Stutter',1))
    frag('S3C_1',seq(stage(71),modg('T4Adjust',-1)));frag('S3C_2',seq(stage(72),modg('T4Adjust',-2),setg('Cruel',0)))
    frag('S3C_3',seq(stage(73),modg('T4Adjust',2)));frag('S3C_4',seq(stage(74),stage(66)))
    frag('S3K_1',stage(75));frag('S3K_2',seq(stage(76),modg('T4Adjust',-1)))
    frag('S3K_3',seq(stage(77),setg('Cruel',1)));frag('S3K_4',seq(stage(78),stage(66)))
    frag('S3_End',call('S3Done'))
    for i in (1,2,3,4):
        frag('RV_%d'%i,seq(*([modg('T4Adjust',1)] if i==1 else [])+[call('Outcome',80+i)]))
        frag('RVW_%d'%i,call('Outcome',90+i))
    frag('LV_End',call('LeaveDone'))
    pexw.write(sc.module(),out);return sc

def build_records(own,ns_idx,sl_idx,script_md,voice_csv,p1_script_md,p1_voice_csv,ns_path):
    O=lambda i:(own<<24)|i;SLF=lambda i:(sl_idx<<24)|i;NSF=lambda i:(ns_idx<<24)|i
    L,C=parse_script(script_md);V=voice_ids(voice_csv);L1,C1=parse_script(p1_script_md);V1=voice_ids(p1_voice_csv)
    Q=O(P2Q);D=Dialogue(Q)
    nxt={'topic':TOPIC_FIRST,'nate':NATE_FIRST,'scene':SCENE_FIRST,'greet':GREET_FIRST}
    def alloc(k): v=nxt[k];nxt[k]+=1;assert v<NEXT_FREE,k;return O(v)
    copies={}                                    # new INFO id -> voice file id it copies
    gv=lambda k:O(G[k])
    props=[(k,vm_obj(gv(k))) for k in ('CheckIn','Cruel','Stutter','T3Adjust','T4Adjust')]
    props+=[('Synth'+k,vm_obj(SLF(v))) for k,v in SL_KW.items()]+[('Nora'+k,vm_obj(NSF(v))) for k,v in NS_KW.items()]
    props+=[('SizeSmall',vm_obj(CA_SIZE_SMALL))]
    fr=lambda func: frag_vmad(TIF,func,props)
    def line_info(lid,frag=None,conds=b'',flags=0,src=None):
        L_,V_=(L1,V1) if lid.startswith('P1') else (L,V)
        ln=L_[lid];iid,emo=V_[lid]
        if src=='copy':
            fid=alloc('greet');copies[fid&0xFFFFFF]=iid&0xFFFFFF
        else: fid=O(iid&0xFFFF)
        return D.info(fid,ln['text'],emotion_for(ln['delivery'],emo),conds=conds,vmad=fr(frag) if frag else None,flags=flags)
    cache={}
    def npc(lid,frag=None):
        if (lid,frag) not in cache: cache[(lid,frag)]=D.topic(alloc('topic'),'SCEN',[line_info(lid,frag)])
        return cache[(lid,frag)]
    def player(cid,frag=None,src=C):
        c=src[cid];info=D.info(alloc('nate'),c['line'],EMO['neutral'],prompt=c['label'],vmad=fr(frag) if frag else None)
        return D.topic(alloc('topic'),'SCEN',[info])
    done=lambda st,val=1.0,OR=False: cond(GetStageDone,Q,st,'==',val,OR=OR)
    g=lambda k,op,val,OR=False: cond(GetGlobalValue,gv(k),0,op,float(val),OR=OR)
    scenes=[]
    def new_scene(edid,actors=(A_SYNTH,A_NORA),optional=()):
        s=Scene(alloc('scene'),edid,Q,list(actors),optional);scenes.append(s);return s
    def say(s,alias,lid,cnd=b'',frag=None,name=None):
        ph=s.phase(name or lid,cnd);s.line(alias,npc(lid,frag),ph);return ph
    SY,NO=A_SYNTH,A_NORA
    def hold(s):
        for a in s.actors: s.package(a,STAY_PACKAGE,0,len(s.phases)-1)
    # ---------- gifts ----------
    gift_infos=[line_info('P2-GF-%03d'%(i+1),conds=g('CheckIn','==',0)+g('GiftType','==',i+1)) for i in range(5)]
    gift_infos+=[line_info('P2-GF-010',conds=g('CheckIn','==',2)),
                 line_info('P2-GF-020',conds=g('CheckIn','==',3)+g('GiftType','==',6)),line_info('P2-GF-021',conds=g('CheckIn','==',3)+g('GiftType','==',7)),
                 line_info('P2-GF-030',conds=g('CheckIn','==',4),flags=0x0002),line_info('P2-GF-031',conds=g('CheckIn','==',4),flags=0x0002)]
    gift_topic=D.topic(alloc('topic'),'SCEN',gift_infos,edid='NN_P2_Gifts')
    sg=new_scene('NN_P2_Gift',actors=(SY,));ph=sg.phase('Start');sg.line(SY,gift_topic,ph)
    sng=new_scene('NN_P2_NoraGift',actors=(NO,));say(sng,NO,'P2-GF-040',name='Start')
    # ---------- check-in ----------
    sck=new_scene('NN_P2_CheckIn',optional=(NO,))
    say(sck,SY,'P2-CK-001',name='Start')
    ph=sck.phase('Choice');sck.choice(SY,ph,[player('P2-CK-010','CK_1'),player('P2-CK-013','CK_4'),player('P2-CK-012','CK_3'),player('P2-CK-011','CK_2')],
                                      [npc('P2-CK-020'),npc('P2-CK-023'),npc('P2-CK-022'),npc('P2-CK-021')])
    say(sck,NO,'P2-CK-030',g('CheckIn','==',1,OR=True)+g('CheckIn','==',3));say(sck,NO,'P2-CK-031',g('CheckIn','==',4))
    hold(sck)
    # ---------- NORA's first talk ----------
    sn1=new_scene('NN_P2_N1_NoraTalk',actors=(NO,))
    say(sn1,NO,'P2-N1-001',name='Start');say(sn1,NO,'P2-N1-002')
    for i in range(4): say(sn1,NO,'P2-N1-01%d'%i,g('CheckIn','==',i+1))
    ph=sn1.phase('Answer');sn1.choice(NO,ph,[player('P2-N1-020'),player('P2-N1-021'),0,player('P2-N1-022')])
    say(sn1,NO,'P2-N1-030',frag='N1_End');hold(sn1)
    # ---------- NORA's tier 2 talk ----------
    def n2_main(s,c0):
        say(s,NO,'P2-N2-020',c0,name='Main')
        ph=s.phase('Thoughts',c0)
        s.choice(NO,ph,[player('P2-N2-031','N2_P2'),player('P2-N2-033','N2_P4'),player('P2-N2-032','N2_P3'),player('P2-N2-030','N2_P1')],
                 [npc('P2-N2-041','N2_End'),npc('P2-N2-043','N2_End'),npc('P2-N2-042','N2_End'),npc('P2-N2-040','N2_End')])
        say(s,SY,'P2-N2-050',c0+done(52));say(s,SY,'P2-N2-051',c0+done(53))
        hold(s)
    sn2=new_scene('NN_P2_N2_NoraTalk',optional=(SY,))
    say(sn2,NO,'P2-N2-001',name='Start')
    ph=sn2.phase('Ask');sn2.choice(NO,ph,[player('P2-N2-010'),player('P2-N2-012','N2_Later'),player('P2-N2-013'),player('P2-N2-011')],[0,npc('P2-N2-015'),0,0])
    n2_main(sn2,done(45,0.0))
    sn2b=new_scene('NN_P2_N2_NoraTalkAgain',optional=(SY,));n2_main(sn2b,b'')
    # ---------- synth Nora's tier 3 talk ----------
    def s3_main(s,c0):
        cruel=g('CheckIn','==',4,OR=True)+g('Cruel','==',1)
        say(s,SY,'P2-S3-020',c0+cruel,name='Main');say(s,SY,'P2-S3-021',c0+cruel)
        ph=s.phase('CruelChoice',c0+cruel)
        s.choice(SY,ph,[player('P2-S3-030','S3C_1'),player('P2-S3-033','S3C_4'),player('P2-S3-032','S3C_3'),player('P2-S3-031','S3C_2')],
                 [npc('P2-S3-040','S3_End'),0,npc('P2-S3-042','S3_End'),npc('P2-S3-041','S3_End')])
        say(s,NO,'P2-S3-045',c0+done(73))
        kind=c0+g('CheckIn','!=',4)+g('Cruel','==',0)+done(71,0.0)+done(72,0.0)+done(73,0.0)+done(74,0.0)
        say(s,SY,'P2-S3-050',kind+g('Stutter','==',0),name='Kind');say(s,SY,'P2-S3-051',kind+g('Stutter','==',0))
        say(s,SY,'P2-S3-055',kind+g('Stutter','==',1));say(s,SY,'P2-S3-056',kind+g('Stutter','==',1))
        ph=s.phase('KindChoice',kind)
        s.choice(SY,ph,[player('P2-S3-061','S3K_2'),player('P2-S3-063','S3K_4'),player('P2-S3-062','S3K_3'),player('P2-S3-060','S3K_1')],
                 [npc('P2-S3-071','S3_End'),0,npc('P2-S3-072','S3_End'),npc('P2-S3-070','S3_End')])
        say(s,NO,'P2-S3-075',c0+done(77))
        reopen(s,c0+done(66),'RV')
        hold(s)
    def reopen(s,c,pre):
        if pre=='RV': say(s,SY,'P2-RV-001',c,name='Reopen')
        ph=s.phase(pre+'Choice',c)
        s.choice(SY,ph,[player('P1-S3-010',pre+'_1',C1),player('P1-S3-012',pre+'_3',C1),player('P1-S3-013',pre+'_4',C1),player('P1-S3-011',pre+'_2',C1)],
                 [npc('P2-RV-010'),npc('P1-S3-041') if False else abom_line(),npc('P2-RV-040'),npc('P2-RV-020')])
        base=80 if pre=='RV' else 90
        say(s,NO,'P2-RV-011',c+done(base+1));say(s,NO,'P2-RV-041',c+done(base+4))
    abom={}
    def abom_line():
        if 't' not in abom: abom['t']=D.topic(alloc('topic'),'SCEN',[line_info('P1-S3-041',src='copy')])
        return abom['t']
    ss3=new_scene('NN_P2_S3_SynthTalk',optional=(NO,))
    say(ss3,SY,'P2-S3-001',name='Start')
    ph=ss3.phase('Ask');ss3.choice(SY,ph,[player('P2-S3-010'),player('P2-S3-012','S3_Later'),player('P2-S3-013','S3_Rude'),player('P2-S3-011')],
                                   [0,npc('P2-S3-015'),npc('P2-S3-016'),0])
    s3_main(ss3,done(65,0.0))
    ss3b=new_scene('NN_P2_S3_SynthTalkAgain',optional=(NO,));s3_main(ss3b,b'')
    # at the vault, after "I need time": the four choices again
    srw=new_scene('NN_P2_VaultWait',optional=(NO,));reopen(srw,b'','RVW');hold(srw)
    # ---------- leaving / after the kill ----------
    slv=new_scene('NN_P2_Leave',optional=(NO,))
    say(slv,SY,'P2-LV-001',name='Start');say(slv,SY,'P2-LV-002',frag='LV_End');say(slv,NO,'P2-LV-003')
    sak=new_scene('NN_P2_AfterKill',actors=(NO,));say(sak,NO,'P2-RV-030',name='Start')
    # ---------- exchanges ----------
    exch=[]
    for i,seq_ in enumerate([[('P2-T1-030',SY),('P2-T1-031',NO)],[('P2-T1-050',SY),('P2-T1-051',NO)],
                             [('P2-T2-001',NO),('P2-T2-002',SY)],[('P2-T2-010',SY),('P2-T2-011',NO)],[('P2-T2-020',NO),('P2-T2-021',SY)],
                             [('P2-T3-001',SY),('P2-T3-002',NO)],[('P2-T3-010',NO),('P2-T3-011',SY),('P2-T3-012',NO)],[('P2-T3-020',SY),('P2-T3-021',NO)]]):
        sx=new_scene('NN_P2_Ex%d'%(i+1))
        for j,(lid,al) in enumerate(seq_): say(sx,al,lid,name='Start' if j==0 else None)
        exch.append(sx)
    # ---------- greetings ----------
    syn_is=cond(GetIsID,SLF(SL_NORA_NPC),0,'==',1.0);nora_is=cond(GetIsID,NSF(NS_NORA_NPC),0,'==',1.0)
    def greet(lid,conds,scene,phase='Start'):
        L_,V_=(L1,V1) if lid.startswith('P1') else (L,V);ln=L_[lid];iid,emo=V_[lid]
        fid=alloc('greet');copies[fid&0xFFFFFF]=iid&0xFFFFFF
        return D.info(fid,ln['text'],emotion_for(ln['delivery'],emo),conds=conds,start_scene=scene.fid,start_phase=phase)
    gre=[greet('P2-N2-001',nora_is+done(45)+done(50,0.0),sn2b,'Main'),
         greet('P2-S3-001',syn_is+done(65)+done(70,0.0),ss3b,'Main'),
         greet('P1-S3-001',syn_is+g('Waiting','>',0),srw,'RVWChoice')]
    D.topic(alloc('topic'),'GREE',gre,edid='NN_P2_Greetings',priority=100.0)
    # ---------- idles ----------
    T=O(TIER);tier=lambda n: cond(GetGlobalValue,T,0,'==',float(n))
    idles=[line_info(l,conds=syn_is+tier(1)+g('Waiting','==',0),flags=0x0002) for l in ('P2-T1-001','P2-T1-002','P2-T1-003','P2-T1-010','P2-T1-011','P2-T1-012')]
    idles+=[line_info(l,conds=nora_is+tier(1),flags=0x0002) for l in ('P2-T1-020','P2-T1-021')]
    idles+=[line_info('P2-T2-031',conds=syn_is+tier(2)+g('Waiting','==',0),flags=0x0002),line_info('P2-T2-030',conds=nora_is+tier(2),flags=0x0002)]
    D.topic(alloc('topic'),'IDLE',idles,edid='NN_P2_Idles')
    # ---------- combat aid barks (Say) ----------
    aid={}
    for k,lids,who in [('TopicAidSynth',('P2-CB-001','P2-CB-002'),syn_is),('TopicAidNora',('P2-CB-010','P2-CB-011'),nora_is),
                       ('TopicThanksSynth',('P2-CB-020',),syn_is),('TopicThanksNora',('P2-CB-021',),nora_is)]:
        aid[k]=D.topic(alloc('topic'),'SCEN',[line_info(l,conds=who,flags=0x0002) for l in lids],edid='NN_P2_'+k[5:])
    D.scenes=[s.build() for s in scenes]
    # ---------- quest NN_Phase2 ----------
    qprops=[('SynthNoraRef',vm_obj(SLF(SL_NORA_REF))),('NoraRef',vm_obj(NSF(NS_NORA_REF))),('Phase1',vm_obj(O(PH1))),('Followers',vm_obj(FOLLOWERS))]
    qprops+=[(k,vm_obj(gv(k))) for k in G]+[('Tier',vm_obj(O(TIER))),('Impatient',vm_obj(O(IMPATIENT)))]
    qprops+=[('AmmoList',vm_obj(O(FL_AMMO))),('JunkList',vm_obj(O(FL_JUNK))),('RareJunkList',vm_obj(O(FL_RARE))),
             ('Caps',vm_obj(CAPS)),('Stimpak',vm_obj(STIMPAK)),('RadAway',vm_obj(RADAWAY)),('Screws',vm_obj(SCREWS)),('Gears',vm_obj(GEARS)),
             ('Circuitry',vm_obj(CIRCUITRY)),('NuclearMaterial',vm_obj(NUCLEAR)),('Adhesive',vm_obj(ADHESIVE)),
             ('WalkQuest',vm_obj(O(WALKQ))),('VaultAnchor',vm_obj(VAULT_ANCHOR)),('NoteAnchor',vm_obj(SPOUSE_POD)),('LinkKeyword',vm_obj(LINK_CUSTOM02)),
             ('ReturnedMsg',vm_obj(O(MSG_RETURNED))),('NothingMsg',vm_obj(O(MSG_NOTHING))),('LeaveNote',vm_obj(O(LEAVE_NOTE))),('WaitNote',vm_obj(O(WAITNOTE))),
             ('HealthAV',vm_obj(HEALTH))]
    for k,s in [('Gift',sg),('NoraGift',sng),('CheckIn',sck),('N1',sn1),('N2',sn2),('S3',ss3),('Leave',slv),('AfterKill',sak)]: qprops.append(('Scene'+k,vm_obj(s.fid)))
    qprops+=[('SceneEx%d'%(i+1),vm_obj(s.fid)) for i,s in enumerate(exch)]+[(k,vm_obj(v)) for k,v in aid.items()]
    vm=struct.pack('<hhH',6,2,1)+ws(QS)+struct.pack('<BH',0,len(qprops))+b''.join(ws(n)+v for n,v in qprops)
    stg=[10,20,30,40,45,50,51,52,53,54,60,65,66,70,71,72,73,74,75,76,77,78,81,82,83,84,88,89,91,92,93,94]
    q=sub('EDID',zs('NN_Phase2'))+sub('VMAD',vm)+sub('FULL',zs('Synth Nora'))
    q+=sub('DNAM',struct.pack('<HBBII',0x0111,90,0,0,7))+sub('NEXT',b'')
    q+=b''.join(sub('INDX',struct.pack('<HBB',n,0,0))+sub('QSDT',b'\0') for n in stg)
    q+=sub('QOBJ',struct.pack('<H',20))+sub('FNAM',struct.pack('<I',0))+sub('NNAM',zs('Synth Nora has returned to Vault 111'))+sub('QSTA',struct.pack('<iII',A_SYNTH,0,0))
    q+=sub('ANAM',struct.pack('<I',2))
    for aid_,name,ref in [(A_SYNTH,'SynthNora',SLF(SL_NORA_REF)),(A_NORA,'Nora',NSF(NS_NORA_REF))]:
        q+=sub('ALST',struct.pack('<I',aid_))+sub('ALID',zs(name))+sub('FNAM',struct.pack('<I',0x282))+sub('ALFR',struct.pack('<I',ref))+sub('VTCK',struct.pack('<I',0))+sub('ALED',b'')
    quest=record('QUST',Q,0,q)
    child=D.records()
    group=b'GRUP'+struct.pack('<I',24+len(child))+struct.pack('<I',Q)+struct.pack('<IHHHH',10,0,0,0,0)+child
    walk=(sub('ALST',struct.pack('<I',0))+sub('ALID',zs('SynthNora'))+sub('FNAM',struct.pack('<I',0x282))+sub('ALFR',struct.pack('<I',SLF(SL_NORA_REF)))
          +sub('ALPC',struct.pack('<I',TRAVEL_LINK02))+sub('VTCK',struct.pack('<I',0))+sub('ALED',b''))
    walkq=record('QUST',O(WALKQ),0,sub('EDID',zs('NN_SynthNoraWalksBack'))+sub('DNAM',bytes(12))+sub('NEXT',b'')+sub('ANAM',struct.pack('<I',1))+walk)
    # ---------- other records ----------
    globs=[glob(gv(k),'NN_P2'+k,0.0) for k in G]
    def flst(fid,edid,items): return record('FLST',fid,0,sub('EDID',zs(edid))+b''.join(sub('LNAM',struct.pack('<I',x)) for x in items))
    flsts=[flst(O(FL_AMMO),'NN_P2GiftAmmo',AMMO),flst(O(FL_JUNK),'NN_P2GiftJunk',JUNK),flst(O(FL_RARE),'NN_P2GiftRareJunk',RARE)]
    def note_msg(fid,edid,text):
        return record('MESG',fid,0,sub('EDID',zs(edid))+sub('DESC',zs(text))+sub('FULL',zs(''))+sub('INAM',b'\0'*4)+sub('DNAM',b'\0'*4)+sub('TNAM',struct.pack('<I',4)))
    msgs=[note_msg(O(MSG_RETURNED),'NN_P2_ReturnedToVaultMsg',RETURNED_TEXT),note_msg(O(MSG_NOTHING),'NN_P2_NothingToAdvanceMsg',NOTHING_TEXT)]
    books=[book(O(LEAVE_NOTE),'NN_SynthNoraLeaveNote',"Synth Nora's Note",LEAVE_TEXT,ns_path)]
    n=1+len(D.topics)+sum(len(i) for _,_,i in D.topics)+len(D.scenes)
    info={'scenes':len(scenes),'topics':len(D.topics),'nate':nxt['nate']-NATE_FIRST,'greet':nxt['greet']-GREET_FIRST,'copies':copies,
          'voiced':sorted({i for _,_,infos in D.topics for i in []})}
    return {'quest':quest+group,'qcount':n,'walk':walkq,'globs':globs,'flsts':flsts,'msgs':msgs,'books':books,'info':info}

if __name__=='__main__':
    d=sys.argv[1];quest_script(os.path.join(d,QS+'.pex'));tif_script(os.path.join(d,TIF+'.pex'));print('phase 2 scripts ok')
