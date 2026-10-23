"""Phase 4: relationship tiers 4 and 5, the broken phase, the duo romance and Eternal Lovers (docs/script/phase4-script.md).

Quest NN_Phase4 (0xEB5, start game enabled) with NN_Phase4Script; dialogue fragments in NN_P4S_TIF.
Timeline:
  NN_Phase2 stage 70 (tier 3 talk done)  -> tier 4 in (4 + T4Adjust) game days (at least 1)        stage 10 / 20
  Organic Nora's tier 4 talk (nice, or mean if the cruel flag is still set)                         stages 30-44
  -> tier 5 in (4 + T5Adjust) days ("really enjoy" -1, "I just don't know" +1)                      stage 50
  Both Noras' tier 5 talk -> romance question                                                       stages 60-63
  "It's too much" / "I need to think": asked again 12 game days later (both come up to you)         ReAsk global
  "She's just a machine": broken phase (tier 5 locked, flat lines, no reactions)                    stage 43, Broken global
  "Take her out": she turns hostile (NN_Phase2's own hostile path, Outcome 83)                       stage 44 / 90
Eternal Lovers ("I love you both"): perk on the player (fire/cryo/poison resistance +50), +100 health ability on each
Nora, and 1 HP per second regeneration from this script while the player has the perk. All permanent.
Synthetic Love's own romance: p865_COMNora stage 525 (its fragment calls RomanceSuccess) -> her two lines and
Organic Nora's reaction for the current tier.
Line INFO IDs come from docs/script/phase4-voice-sheet.csv (0xE60-0xEB4); everything else is 0xEB5 upwards."""
import sys,os,struct
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from build import sub,record,zs,vm_obj,glob
from scenes_lib import Dialogue,Scene,cond,GetStageDone,GetGlobalValue,GetIsID,GetInFaction,frag_vmad,emotion_for,parse_script,voice_ids,EMO,ws,RUN_REF
from pexasm import Script,S
import pexw,phase2

P4Q=0xEB5
G={'T5Adjust':0xEB6,'Duo':0xEB7,'Broken':0xEB8,'Mean':0xEB9,'Answer':0xEBA,'ReAsk':0xEBB,'Asked':0xEBC}
PERK_ID,AB_PLAYER,AB_NORA,MSG_PERK=0xEBD,0xEBE,0xEBF,0xEC0
FIRST_DYN=0xEC1; LIMIT=0x1000
QS='NN_Phase4Script'; TIF='NN_P4S_TIF'
# other mods / vanilla
SL_NORA_REF=0x000FB3; SL_NORA_NPC=0x000F99; NS_NORA_REF=0x001735; NS_NORA_NPC=0x000F9A
SL_KW=phase2.SL_KW; NS_KW=phase2.NS_KW
SL_COMNORA=0x001760; SL_ROMANCE_STAGE=525        # Synthetic Love: Fragment_Stage_0525 calls RomanceSuccess
SL_TALK_SCENE=0x00175E                            # Synthetic Love: COMNoraTalk_TalkScene (companion menu), phase "Loop"
CURRENT_COMPANION=0x00023C01; HEALTH=0x000002D4; STAY_PACKAGE=phase2.STAY_PACKAGE
MQ207=0x000229EC; SHAUN_REF=0x0005C337            # Institutionalized; Father (ShaunRef)
AB_FORTIFY_HEALTH=0x0004A0D2; AB_RESIST={'Fire':0x0004D86E,'Cryo':0x0004D86D,'Poison':0x0004D86B}
EQUIP_EITHER=0x00013F44
GetDistance,GetDead=1,46
A_SYNTH,A_NORA=0,1
STAGES=[10,20,25,30,31,32,33,34,41,42,43,44,50,52,55,60,61,62,63,81,90,100,110,111,112]
# timers
T_T4,T_T5,T_REASK,T_POLL,T_EXCH,T_FUT,T_BR=1,2,3,4,5,6,7
RT_REGEN,RT_BROKEN,RT_HOSTILE,RT_RO=10,11,12,13
POLL_H=0.1
Q_T4,Q_T5,Q_RA=1,2,3
PERK_NAME='Eternal Lovers'
PERK_DESC=("You understand what love is, no matter what form, where they are from, or who they are. Thanks to your relationship "
           "with both Noras, they each gain 100 hit points, and you heal 1 HP per second and take 50% less fire, cryo and poison damage.")

def quest_script(out):
    phase2.quest_script(out+'.p2tmp');os.remove(out+'.p2tmp')            # registers NN_Phase2Script's functions
    sc=Script(QS,'Quest','Nora and Nora: Phase 4, relationship tiers 4 and 5.')
    P=lambda n,t: sc.prop(n,t)
    SYN,NOR=P('SynthNoraRef','objectreference'),P('NoraRef','objectreference');P2=P('Phase2',phase2.QS)
    TIERG=P('Tier','globalvariable')
    PG={k:P('P2'+k,'globalvariable') for k in ('CheckIn','Cruel','T4Adjust','NextEventDay','Waiting')}
    GV={k:P(k,'globalvariable') for k in G}
    SLQ=P('SLRomanceQuest','quest');PERK=P('EternalLovers','perk');ABN=P('NoraAbility','spell');PMSG=P('PerkMsg','message')
    NOTHING=P('NothingMsg','message');HP=P('HealthAV','actorvalue')
    SC={k:P('Scene'+k,'scene') for k in ('T4','T4b','T5','T5b','ReAsk','BR6','RO','ExT4a','ExT4b','ExT5a','ExT5b','ExT5c','ExT5d','FU1','FU2','FU3')}
    CB1,CB2=P('TopicDownedSynth','topic'),P('TopicDownedNora','topic')
    PEND=sc.var('Pending','Int',0);PRO=sc.var('PendingRO','Bool',False);PBR=sc.var('PendingBR','Bool',False)
    EXI=sc.var('NextEx','Int',0);FUI=sc.var('NextFuture','Int',0);LASTB=sc.var('LastDowned','Float',0.0)
    def player(f): return f.callstatic('game','GetPlayer')
    def actor(f,r): return f.cast(r,'actor')
    def gval(f,g): return f.call(g,'GetValue')
    # ---------- helpers ----------
    f=sc.func('Timer',[('afHours','Float'),('aiID','Int')])
    f.call('self','StartTimerGameTime','afHours','aiID')
    now=f.callstatic('utility','GetCurrentGameTime');d=f.tmp('Float');f.op('fdiv',d,'afHours',24.0);t=f.tmp('Float');f.op('fadd',t,now,d)
    f.call(PG['NextEventDay'],'SetValue',t)
    f=sc.func('Days',[('afBase','Float'),('akAdjust','globalvariable')],'Float')   # hours for (base + adjust) days, at least one day
    a=f.call('akAdjust','GetValue');s_=f.tmp('Float');f.op('fadd',s_,'afBase',a);h=f.tmp('Float');f.op('fmul',h,s_,24.0)
    c=f.cmp('cmp_lt',h,24.0);f.jmpf(c,'ok');f.op('assign',h,24.0);f.label('ok');f.ret(h)
    f=sc.func('Ended',[],'Bool')
    e=f.call(P2,'Ended');f.jmpt(e,'yes');d=f.call('self','GetStageDone',90);f.ret(d)
    f.label('yes');f.ret(True)
    f=sc.func('IsBroken',[],'Bool')
    v=gval(f,GV['Broken']);c=f.cmp('cmp_gt',v,0.0);f.ret(c)
    f=sc.func('Locked',[],'Bool')                                       # no tier 5: broken or hostile
    for st in (43,44,90):
        d=f.call('self','GetStageDone',st);f.jmpt(d,'yes')
    f.ret(False);f.label('yes');f.ret(True)
    f=sc.func('BothNear',[],'Bool')
    for r in (SYN,NOR):
        n=f.call(P2,'Near',r);f.jmpf(n,'no')
    f.ret(True);f.label('no');f.ret(False)
    # ---------- tiers ----------
    f=sc.func('StartTierFourTimer')
    d=f.call('self','GetStageDone',10);f.jmpt(d,'end');e=f.callself('Ended');f.jmpt(e,'end')
    f.call('self','SetStage',10);h=f.callself('Days',4.0,PG['T4Adjust']);f.callself('Timer',h,T_T4)
    f.call('self','StartTimerGameTime',20.0,T_EXCH)
    f.label('end')
    f=sc.func('TierFour')
    d=f.call('self','GetStageDone',20);f.jmpt(d,'end');e=f.callself('Ended');f.jmpt(e,'end')
    f.call(TIERG,'SetValue',4.0);f.call('self','SetStage',20)
    # mean version: cruel check-in ("If that's all you're good at") or "Dumb machine", not cleared by "I'm sorry" (Phase 2 stage 72)
    f.call(GV['Mean'],'SetValue',0.0)
    s72=f.call(P2,'GetStageDone',72);f.jmpt(s72,'q')
    ci=gval(f,PG['CheckIn']);c=f.cmp('cmp_eq',ci,4.0);f.jmpt(c,'mean')
    cr=gval(f,PG['Cruel']);c=f.cmp('cmp_gt',cr,0.0);f.jmpf(c,'q')
    f.label('mean');f.call(GV['Mean'],'SetValue',1.0)
    f.label('q');f.op('assign',PEND,Q_T4)
    f.label('end')
    f=sc.func('TierFive')
    d=f.call('self','GetStageDone',50);f.jmpt(d,'end');l=f.callself('Locked');f.jmpt(l,'end');e=f.callself('Ended');f.jmpt(e,'end')
    f.call(TIERG,'SetValue',5.0);f.call('self','SetStage',50);f.op('assign',PEND,Q_T5)
    f.label('end')
    # ---------- called by dialogue fragments ----------
    f=sc.func('T4Outcome',[('aiCode','Int')])
    f.call('self','SetStage','aiCode');f.call('self','SetStage',30)
    c=f.cmp('cmp_eq','aiCode',43);f.jmpf(c,'n43')
    f.call(GV['Broken'],'SetValue',1.0);f.call('self','StartTimer',3.0,RT_BROKEN);f.call('self','StartTimerGameTime',24.0,T_BR);f.ret()   # NORA's line a day later
    f.label('n43');c=f.cmp('cmp_eq','aiCode',44);f.jmpf(c,'n44')
    f.call('self','StartTimer',12.0,RT_HOSTILE);f.ret()                  # fallback if her line does not play
    f.label('n44');c=f.cmp('cmp_eq','aiCode',41);f.jmpf(c,'n41');f.call(PG['Cruel'],'SetValue',0.0);f.call(GV['Mean'],'SetValue',0.0)
    f.label('n41');c=f.cmp('cmp_eq','aiCode',32);f.jmpf(c,'n32');f.call(GV['T5Adjust'],'Mod',-1.0)
    f.label('n32');c=f.cmp('cmp_eq','aiCode',42);f.jmpf(c,'n42');f.call(GV['T5Adjust'],'Mod',1.0)
    f.label('n42');h=f.callself('Days',4.0,GV['T5Adjust']);f.callself('Timer',h,T_T5)
    f=sc.func('TurnHostile')
    d=f.call('self','GetStageDone',90);f.jmpt(d,'end')
    f.call('self','SetStage',90);f.op('assign',PEND,0);f.call(P2,'Outcome',83)
    f.label('end')
    f=sc.func('RomanceStart')
    f.call(GV['Answer'],'SetValue',0.0);f.call(GV['Asked'],'SetValue',0.0)
    f=sc.func('UnlockPerk')
    pl=player(f);h=f.call(pl,'HasPerk',PERK);f.jmpt(h,'spells')
    f.call(pl,'AddPerk',PERK,False);f.call(PMSG,'Show',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
    f.label('spells')
    for r in (SYN,NOR): a=actor(f,r);f.call(a,'AddSpell',ABN,False)
    f.call('self','CancelTimer',RT_REGEN);f.call('self','StartTimer',1.0,RT_REGEN)
    f=sc.func('RomanceYes')
    f.call('self','SetStage',60);f.call('self','SetStage',61);f.call(GV['Duo'],'SetValue',1.0);f.call(GV['ReAsk'],'SetValue',0.0)
    f.call('self','CancelTimerGameTime',T_REASK);f.callself('UnlockPerk');f.call('self','StartTimerGameTime',24.0,T_FUT)
    f=sc.func('RomanceLater',[('aiCode','Int')])
    f.call('self','SetStage',60);f.call('self','SetStage','aiCode');f.call(GV['ReAsk'],'SetValue',0.0);f.callself('Timer',288.0,T_REASK)
    # ---------- talk queue / poll ----------
    f=sc.func('TryTalk',[],'Bool')
    f.jmpf(PRO,'q');n=f.call(P2,'Near',SYN);f.jmpf(n,'q');f.op('assign',PRO,False);f.call(SC['RO'],'Start');f.ret(True)
    f.label('q')
    c=f.cmp('cmp_eq',PEND,Q_T4);f.jmpf(c,'n1');n=f.call(P2,'Near',NOR);f.jmpf(n,'br')
    f.op('assign',PEND,0);f.call(SC['T4'],'Start');f.ret(True)
    f.label('n1')
    for q,k in ((Q_T5,'T5'),(Q_RA,'ReAsk')):
        c=f.cmp('cmp_eq',PEND,q);f.jmpf(c,'n%d'%q);b=f.callself('BothNear');f.jmpf(b,'br')
        f.op('assign',PEND,0);f.call(SC[k],'Start');f.ret(True)
        f.label('n%d'%q)
    f.label('br')
    f.jmpf(PBR,'no');b=f.callself('BothNear');f.jmpf(b,'no');f.op('assign',PBR,False);f.call(SC['BR6'],'Start');f.ret(True)
    f.label('no');f.ret(False)
    f=sc.func('Poll')
    e=f.callself('Ended');f.jmpt(e,'end')
    f.call('self','StartTimerGameTime',POLL_H,T_POLL)
    ok=f.call(P2,'CanTalk');f.jmpf(ok,'end')
    c=f.cmp('cmp_eq',PEND,0);f.jmpf(c,'try')                          # a talk that was walked away from before the answer: queue it again
    for st,later,keys,q,lab in ((20,25,('T4','T4b'),Q_T4,'r4'),(50,55,('T5','T5b'),Q_T5,'r5')):
        d=f.call('self','GetStageDone',st);f.jmpf(d,lab);d=f.call('self','GetStageDone',st+10);f.jmpt(d,lab)
        d=f.call('self','GetStageDone',later);f.jmpt(d,lab)
        for k in keys: pl_=f.call(SC[k],'IsPlaying');f.jmpt(pl_,lab)
        f.op('assign',PEND,q);f.jmp('try');f.label(lab)
    v=gval(f,GV['ReAsk']);c=f.cmp('cmp_gt',v,0.0);f.jmpf(c,'try');pl_=f.call(SC['ReAsk'],'IsPlaying');f.jmpt(pl_,'try');f.op('assign',PEND,Q_RA)
    f.label('try');f.callself('TryTalk')
    f.label('end')
    f=sc.func('CanChat',[],'Bool')                                     # ambient talk between the two
    e=f.callself('Ended');f.jmpt(e,'no');b=f.callself('IsBroken');f.jmpt(b,'no')
    w=gval(f,PG['Waiting']);c=f.cmp('cmp_gt',w,0.0);f.jmpt(c,'no')
    c=f.cmp('cmp_gt',PEND,0);f.jmpt(c,'no')
    ok=f.call(P2,'CanTalk');f.jmpf(ok,'no');b=f.callself('BothNear');f.ret(b)
    f.label('no');f.ret(False)
    f=sc.func('Exchange')
    e=f.callself('Ended');f.jmpt(e,'end');f.call('self','StartTimerGameTime',20.0,T_EXCH)
    t=gval(f,TIERG);c=f.cmp('cmp_ge',t,4.0);f.jmpf(c,'end')
    ok=f.callself('CanChat');f.jmpf(ok,'end')
    n=f.local('n','Int');f.op('assign',n,2);c=f.cmp('cmp_ge',t,5.0);f.jmpf(c,'pick');f.op('assign',n,6)
    f.label('pick');c=f.cmp('cmp_ge',EXI,n);f.jmpf(c,'go');f.op('assign',EXI,0)
    f.label('go')
    for i,k in enumerate(('ExT4a','ExT4b','ExT5a','ExT5b','ExT5c','ExT5d')):
        c=f.cmp('cmp_eq',EXI,i);f.jmpf(c,'x%d'%i);f.call(SC[k],'Start');f.label('x%d'%i)
    f.op('iadd',EXI,EXI,1)
    f.label('end')
    f=sc.func('Future')                                                # after the duo romance: each talk once, at most one per game day
    e=f.callself('Ended');f.jmpt(e,'end')
    d=f.call('self','GetStageDone',112);f.jmpt(d,'end')
    f.call('self','StartTimerGameTime',24.0,T_FUT)
    ok=f.callself('CanChat');f.jmpf(ok,'end')
    for i,(st,k) in enumerate(((110,'FU1'),(111,'FU2'),(112,'FU3'))):
        d=f.call('self','GetStageDone',st);f.jmpt(d,'f%d'%i);f.call('self','SetStage',st);f.call(SC[k],'Start');f.ret()
        f.label('f%d'%i)
    f.label('end')
    # ---------- events ----------
    f=sc.func('OnQuestInit')
    so=f.cast(P2,'ScriptObject');f.call('self','RegisterForRemoteEvent',so,S('OnStageSet'))
    so=f.cast(SLQ,'ScriptObject');f.call('self','RegisterForRemoteEvent',so,S('OnStageSet'))
    for r in (SYN,NOR):
        a=actor(f,r);so=f.cast(a,'ScriptObject');f.call('self','RegisterForRemoteEvent',so,S('OnEnterBleedout'))
    pl=player(f);so=f.cast(pl,'ScriptObject');f.call('self','RegisterForRemoteEvent',so,S('OnPlayerLoadGame'))
    d=f.call(SLQ,'GetStageDone',SL_ROMANCE_STAGE);f.jmpf(d,'p2');f.call('self','SetStage',100)     # romanced before this was installed
    f.label('p2');d=f.call(P2,'GetStageDone',70);f.jmpf(d,'poll');f.callself('StartTierFourTimer')
    f.label('poll');f.call('self','StartTimerGameTime',POLL_H,T_POLL)
    pl=player(f);h=f.call(pl,'HasPerk',PERK);f.jmpf(h,'end');f.call('self','StartTimer',1.0,RT_REGEN)
    f.label('end')
    f=sc.func('::remote_Actor_OnPlayerLoadGame',[('akSender','actor')])
    pl=player(f);h=f.call(pl,'HasPerk',PERK);f.jmpf(h,'end');f.call('self','CancelTimer',RT_REGEN);f.call('self','StartTimer',1.0,RT_REGEN)
    f.label('end')
    f=sc.func('::remote_Quest_OnStageSet',[('akSender','quest'),('auiStageID','Int'),('auiItemID','Int')])
    q2=f.cast(P2,'quest');c=f.cmp('cmp_eq','akSender',q2);f.jmpf(c,'sl')
    c=f.cmp('cmp_eq','auiStageID',70);f.jmpf(c,'end');f.callself('StartTierFourTimer');f.ret()
    f.label('sl');c=f.cmp('cmp_eq','akSender',SLQ);f.jmpf(c,'end');c=f.cmp('cmp_eq','auiStageID',SL_ROMANCE_STAGE);f.jmpf(c,'end')
    d=f.call('self','GetStageDone',100);f.jmpt(d,'end');f.call('self','SetStage',100);f.call('self','StartTimer',5.0,RT_RO)
    f.label('end')
    f=sc.func('::remote_Actor_OnEnterBleedout',[('akSender','actor')])
    t=gval(f,TIERG);c=f.cmp('cmp_ge',t,4.0);f.jmpf(c,'end')
    b=f.callself('IsBroken');f.jmpt(b,'end');e=f.callself('Ended');f.jmpt(e,'end')
    now=f.callstatic('utility','GetCurrentGameTime');dt=f.tmp('Float');f.op('fsub',dt,now,LASTB);c=f.cmp('cmp_lt',dt,0.01);f.jmpt(c,'end')
    na=actor(f,NOR);c=f.cmp('cmp_eq','akSender',na);f.jmpf(c,'syn')
    n=f.call(P2,'Near',SYN);f.jmpf(n,'end');f.op('assign',LASTB,now);f.call(SYN,'Say',CB1,None,False,None);f.ret()
    f.label('syn');n=f.call(P2,'Near',NOR);f.jmpf(n,'end');f.op('assign',LASTB,now);f.call(NOR,'Say',CB2,None,False,None)
    f.label('end')
    f=sc.func('OnTimer',[('aiTimerID','Int')])
    c=f.cmp('cmp_eq','aiTimerID',RT_REGEN);f.jmpf(c,'n1')
    pl=player(f);h=f.call(pl,'HasPerk',PERK);f.jmpf(h,'end')
    pc=f.call(pl,'GetValuePercentage',HP);c=f.cmp('cmp_lt',pc,1.0);f.jmpf(c,'again')
    d=f.call(pl,'IsDead');f.jmpt(d,'again');f.call(pl,'RestoreValue',HP,1.0)
    f.label('again');f.call('self','StartTimer',1.0,RT_REGEN);f.ret()
    f.label('n1');c=f.cmp('cmp_eq','aiTimerID',RT_BROKEN);f.jmpf(c,'n2')
    ca=f.cast(SYN,'companionactorscript');f.call(ca,'SetHasLeftPlayerPermanently');f.ret()   # her own likes/dislikes and comments stop
    f.label('n2');c=f.cmp('cmp_eq','aiTimerID',RT_HOSTILE);f.jmpf(c,'n3');f.callself('TurnHostile');f.ret()
    f.label('n3');c=f.cmp('cmp_eq','aiTimerID',RT_RO);f.jmpf(c,'end');f.op('assign',PRO,True)
    f.label('end')
    f=sc.func('OnTimerGameTime',[('aiTimerID','Int')])
    for tid,lab in ((T_T4,'t4'),(T_T5,'t5'),(T_REASK,'ra'),(T_POLL,'poll'),(T_EXCH,'ex'),(T_FUT,'fu'),(T_BR,'br')):
        c=f.cmp('cmp_eq','aiTimerID',tid);f.jmpt(c,lab)
    f.ret()
    f.label('t4');f.callself('TierFour');f.ret()
    f.label('t5');f.callself('TierFive');f.ret()
    f.label('ra');e=f.callself('Ended');f.jmpt(e,'end');f.call(GV['ReAsk'],'SetValue',1.0);f.op('assign',PEND,Q_RA);f.ret()
    f.label('poll');f.callself('Poll');f.ret()
    f.label('ex');f.callself('Exchange');f.ret()
    f.label('fu');f.callself('Future');f.ret()
    f.label('br');f.op('assign',PBR,True)
    f.label('end')
    # ---------- test tape ----------
    f=sc.func('TalkNow')
    ok=f.call(P2,'CanTalk');f.jmpf(ok,'later');r=f.callself('TryTalk');f.jmpf(r,'later')
    f.callstatic('debug','Notification',S('Test tape: playing the next talk.'));f.ret()
    f.label('later');f.callstatic('debug','Notification',S('Test tape: next talk queued. It plays when the Noras are close and nobody is fighting or in a scene.'))
    f=sc.func('DebugAdvance',[],'Bool')
    d=f.call('self','GetStageDone',10);f.jmpt(d,'a1');f.callself('StartTierFourTimer')
    f.label('a1');d=f.call('self','GetStageDone',20);f.jmpt(d,'a2');f.call('self','CancelTimerGameTime',T_T4);f.callself('TierFour');f.jmp('talk')
    f.label('a2');d=f.call('self','GetStageDone',30);f.jmpt(d,'a3');f.op('assign',PEND,Q_T4);f.jmp('talk')
    f.label('a3');l=f.callself('Locked');f.jmpt(l,'none')
    d=f.call('self','GetStageDone',50);f.jmpt(d,'a4');f.call('self','CancelTimerGameTime',T_T5);f.callself('TierFive');f.jmp('talk')
    f.label('a4');d=f.call('self','GetStageDone',60);f.jmpt(d,'a5');f.op('assign',PEND,Q_T5);f.jmp('talk')
    f.label('a5');d=f.call('self','GetStageDone',61);f.jmpt(d,'none')
    f.call('self','CancelTimerGameTime',T_REASK);f.call(GV['ReAsk'],'SetValue',1.0);f.op('assign',PEND,Q_RA)
    f.label('talk');c=f.cmp('cmp_gt',PEND,0);f.jmpf(c,'none');f.callself('TalkNow');f.ret(True)
    f.label('none');f.call(NOTHING,'Show',0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);f.ret(False)
    f=sc.func('DebugSkipWait',[],'Bool')
    d=f.call('self','GetStageDone',10);f.jmpf(d,'no')
    d=f.call('self','GetStageDone',20);f.jmpt(d,'s5');f.call('self','CancelTimerGameTime',T_T4);f.callself('TierFour');f.callself('TalkNow');f.ret(True)
    f.label('s5');d=f.call('self','GetStageDone',30);f.jmpf(d,'no');l=f.callself('Locked');f.jmpt(l,'no')
    d=f.call('self','GetStageDone',50);f.jmpt(d,'sr');f.call('self','CancelTimerGameTime',T_T5);f.callself('TierFive');f.callself('TalkNow');f.ret(True)
    f.label('sr');d=f.call('self','GetStageDone',60);f.jmpf(d,'no');d=f.call('self','GetStageDone',61);f.jmpt(d,'no')
    v=gval(f,GV['ReAsk']);c=f.cmp('cmp_gt',v,0.0);f.jmpt(c,'no')
    f.call('self','CancelTimerGameTime',T_REASK);f.call(GV['ReAsk'],'SetValue',1.0);f.op('assign',PEND,Q_RA);f.callself('TalkNow');f.ret(True)
    f.label('no');f.ret(False)
    f=sc.func('DebugSetTier',[('aiTier','Int')])                       # after NN_Phase2's DebugSetTier: start of tier 4 or 5, its talk queued
    c=f.cmp('cmp_ge','aiTier',4);f.jmpf(c,'end')
    d=f.call('self','GetStageDone',10);f.jmpt(d,'s');f.call('self','SetStage',10);f.call('self','StartTimerGameTime',20.0,T_EXCH)
    f.label('s');f.call('self','CancelTimerGameTime',T_T4);f.callself('TierFour')
    c=f.cmp('cmp_ge','aiTier',5);f.jmpf(c,'end')
    l=f.callself('Locked');f.jmpt(l,'end')
    d=f.call('self','GetStageDone',30);f.jmpt(d,'s2');f.call('self','SetStage',31);f.call('self','SetStage',30)
    f.label('s2');f.call('self','CancelTimerGameTime',T_T5);f.callself('TierFive')
    f.label('end')
    f=sc.func('DebugReset')
    for k in G: f.call(GV[k],'SetValue',0.0)
    for tid in (T_T4,T_T5,T_REASK,T_POLL,T_EXCH,T_FUT,T_BR): f.call('self','CancelTimerGameTime',tid)
    for tid in (RT_REGEN,RT_BROKEN,RT_HOSTILE,RT_RO): f.call('self','CancelTimer',tid)
    pl=player(f);f.call(pl,'RemovePerk',PERK)
    for r in (SYN,NOR): a=actor(f,r);f.call(a,'RemoveSpell',ABN)
    ca=f.cast(SYN,'companionactorscript');f.call(ca,'UnsetHasLeftPlayerPermanently')
    f.op('assign',PEND,0);f.op('assign',PRO,False);f.op('assign',PBR,False)
    f.call('self','Stop');f.call('self','Reset');f.call('self','Start')
    pexw.write(sc.module(),out);return sc

REACT={'T4N_Y':[('Nora','Likes'),('Synth','Likes')],'T4N_X':[('Nora','Loves'),('Synth','Loves')],'T4N_A':[('Nora','Likes')],
       'T4M_Y':[('Nora','Likes'),('Synth','Likes')],'T4M_X':[('Synth','Hates')],'T4M_B':[('Nora','Dislikes'),('Synth','Hates')],
       'T5C_Y':[('Nora','Loves')],'T5C_X':[('Nora','Likes')],'RM_Y':[('Nora','Loves'),('Synth','Loves')],
       'RO_Hate':[('Nora','Hates')],'RO_Love':[('Nora','Loves')]}
def tif_script(out):
    if QS.lower() not in __import__('pexasm').SIGS: quest_script(out+'.p4tmp');os.remove(out+'.p4tmp')
    sc=Script(TIF,'TopicInfo','Nora and Nora: Phase 4 dialogue fragments.')
    KW={(w,k):sc.prop(w+k,'keyword') for w in ('Synth','Nora') for k in ('Likes','Loves','Dislikes','Hates')}
    ASKED=sc.prop('Asked','globalvariable')
    f=sc.func('React',[('akEvent','keyword')])
    so=f.cast('self','ScriptObject');f.callstatic('followersscript','SendAffinityEvent',so,'akEvent',None,None,True,True,False,1.0)
    def q4(f): q=f.call('self','GetOwningQuest');return f.cast(q,QS)
    def frag(name,body=None):
        f=sc.func(name,[('akSpeakerRef','objectreference')])
        for r in REACT.get(name,[]): f.callself('React',KW[r])
        if body: body(f)
    stage=lambda st: (lambda f: f.call(f.call('self','GetOwningQuest'),'SetStage',st))
    call=lambda fn,*a: (lambda f: f.call(q4(f),fn,*a))
    frag('T4_Later',stage(25))
    for k,code in (('T4N_Y',31),('T4N_X',32),('T4N_A',33),('T4N_B',34),('T4M_Y',41),('T4M_A',42),('T4M_X',43),('T4M_B',44)):
        frag(k,call('T4Outcome',code))
    frag('T4_Hostile',call('TurnHostile'))
    frag('T5_Later',stage(55));frag('T5_AskX',stage(52))
    frag('RM_Reset',call('RomanceStart'))
    frag('T5C_Y');frag('T5C_X')
    frag('RM_Y',call('RomanceYes'));frag('RM_B',call('RomanceLater',62));frag('RM_X',call('RomanceLater',63))
    frag('RM_A',lambda f: f.call(ASKED,'SetValue',1.0))
    frag('RO_Hate');frag('RO_Love')
    frag('BR6_End',stage(81))
    pexw.write(sc.module(),out);return sc

def build_records(own,ns_idx,sl_idx,script_md,voice_csv):
    O=lambda i:(own<<24)|i;SLF=lambda i:(sl_idx<<24)|i;NSF=lambda i:(ns_idx<<24)|i
    L,C=parse_script(script_md);V=voice_ids(voice_csv)
    Q=O(P4Q);D=Dialogue(Q);nxt=[FIRST_DYN]
    def alloc(): v=nxt[0];nxt[0]+=1;assert v<LIMIT,'out of ESL form IDs';return O(v)
    gv=lambda k:O(G[k])
    copies={}
    props=[('Synth'+k,vm_obj(SLF(v))) for k,v in SL_KW.items()]+[('Nora'+k,vm_obj(NSF(v))) for k,v in NS_KW.items()]+[('Asked',vm_obj(gv('Asked')))]
    fr=lambda func: frag_vmad(TIF,func,props)
    syn_is=cond(GetIsID,SLF(SL_NORA_NPC),0,'==',1.0);nora_is=cond(GetIsID,NSF(NS_NORA_NPC),0,'==',1.0)
    WHO={'SYNTH':syn_is,'NORA':nora_is}
    def line_info(lid,frag=None,conds=b'',flags=0,copy=False,start_scene=None,start_phase=''):
        ln=L[lid];iid,emo=V[lid]
        if copy: fid=alloc();copies[fid&0xFFFFFF]=iid&0xFFFFFF
        else: fid=O(iid&0xFFFF)
        return D.info(fid,ln['text'],emotion_for(ln['delivery'],emo),conds=conds,vmad=fr(frag) if frag else None,flags=flags,
                      start_scene=start_scene,start_phase=start_phase)
    cache={}
    def npc(lid,frag=None):
        if lid not in cache: cache[lid]=(D.topic(alloc(),'SCEN',[line_info(lid,frag)]),frag)
        assert cache[lid][1]==frag,lid
        return cache[lid][0]
    pcache={}
    def player(cid,frag=None):
        if cid not in pcache:
            c=C[cid];info=D.info(alloc(),c['line'],EMO['neutral'],prompt=c['label'],vmad=fr(frag) if frag else None)
            pcache[cid]=D.topic(alloc(),'SCEN',[info])
        return pcache[cid]
    done=lambda st,val=1.0: cond(GetStageDone,Q,st,'==',val)
    g=lambda k,op,val,OR=False: cond(GetGlobalValue,gv(k),0,op,float(val),OR=OR)
    tier=lambda op,n: cond(GetGlobalValue,O(phase2.TIER),0,op,float(n))
    scenes=[];SC={}
    def new_scene(key,edid,actors=(A_SYNTH,A_NORA),optional=()):
        s=Scene(alloc(),edid,Q,list(actors),optional);scenes.append(s);SC[key]=s;return s
    def say(s,alias,lid,cnd=b'',frag=None,name=None):
        ph=s.phase(name or lid,cnd);s.line(alias,npc(lid,frag),ph);return ph
    def hold(s):
        for a in s.actors: s.package(a,STAY_PACKAGE,0,len(s.phases)-1)
    SY,NO=A_SYNTH,A_NORA
    # ---------- tier 4 talk ----------
    def t4_main(s,c0):
        nice=c0+g('Mean','==',0)
        for i,lid in enumerate(('P4-T4-020','P4-T4-021','P4-T4-022','P4-T4-023')): say(s,NO,lid,nice,name='Main' if i==0 else None)
        ph=s.phase('NiceChoice',nice)
        s.choice(NO,ph,[player('P4-T4-030','T4N_Y'),player('P4-T4-033','T4N_B'),player('P4-T4-031','T4N_X'),player('P4-T4-032','T4N_A')],
                 [npc('P4-T4-034'),npc('P4-T4-035'),npc('P4-T4-034'),npc('P4-T4-035')])
        mean=c0+g('Mean','==',1)
        for i,lid in enumerate(('P4-T4-040','P4-T4-041','P4-T4-042','P4-T4-043','P4-T4-044')): say(s,NO,lid,mean,name='MeanMain' if i==0 else None)
        ph=s.phase('MeanChoice',mean)
        s.choice(NO,ph,[player('P4-T4-050','T4M_Y'),player('P4-T4-053','T4M_B'),player('P4-T4-052','T4M_X'),player('P4-T4-051','T4M_A')],
                 [npc('P4-T4-054'),0,npc('P4-T4-056'),npc('P4-T4-055')])
        say(s,SY,'P4-T4-057',c0+done(44),frag='T4_Hostile')
        hold(s)
    st4=new_scene('T4','NN_P4_T4_NoraTalk',optional=(SY,))
    say(st4,NO,'P4-T4-010',name='Start')
    ph=st4.phase('Ask');st4.choice(NO,ph,[player('P4-T4-011'),player('P4-T4-013','T4_Later'),player('P4-T4-012'),player('P4-T4-014')],[0,npc('P4-T4-015'),0,0])
    t4_main(st4,done(25,0.0))
    st4b=new_scene('T4b','NN_P4_T4_NoraTalkAgain',optional=(SY,));t4_main(st4b,b'')
    # ---------- tier 5 talk and the romance question ----------
    def romance(s,c0):
        ph=s.phase('Romance',c0)
        s.choice(NO,ph,[player('P4-T5-050','RM_Y'),player('P4-T5-051','RM_B'),player('P4-T5-052','RM_X'),player('P4-T5-053','RM_A')])
        asked=c0+g('Asked','==',1)+g('Answer','==',0)
        say(s,SY,'P4-T5-054',asked);say(s,NO,'P4-T5-055',asked)
        ph=s.phase('RomanceAgain',asked)
        s.choice(NO,ph,[player('P4-T5-050','RM_Y'),player('P4-T5-051','RM_B'),player('P4-T5-052','RM_X'),0])
        say(s,SY,'P4-T5-060',c0+g('Answer','==',1));say(s,NO,'P4-T5-061',c0+g('Answer','==',1))
        say(s,NO,'P4-T5-062',c0+g('Answer','==',2));say(s,SY,'P4-T5-063',c0+g('Answer','==',2))
        say(s,NO,'P4-T5-064',c0+g('Answer','==',3))
        hold(s)
    def t5_main(s,c0):
        say(s,SY,'P4-T5-018',c0+done(52));say(s,NO,'P4-T5-019',c0+done(52))
        for i,(al,lid) in enumerate(((NO,'P4-T5-020'),(SY,'P4-T5-021'),(NO,'P4-T5-022'),(SY,'P4-T5-023'),(NO,'P4-T5-024'),(NO,'P4-T5-025'))):
            say(s,al,lid,c0,frag='RM_Reset' if i==0 else None,name='Main' if i==0 else None)
        ph=s.phase('Feelings',c0)
        s.choice(NO,ph,[player('P4-T5-030','T5C_Y'),player('P4-T5-032'),player('P4-T5-031','T5C_X'),player('P4-T5-033')])
        for al,lid in ((NO,'P4-T5-040'),(SY,'P4-T5-041'),(SY,'P4-T5-042'),(NO,'P4-T5-043'),(NO,'P4-T5-044')): say(s,al,lid,c0)
        romance(s,c0)
    st5=new_scene('T5','NN_P4_T5_Talk')
    say(st5,NO,'P4-T5-010',name='Start');say(st5,SY,'P4-T5-011')
    ph=st5.phase('Ask');st5.choice(NO,ph,[player('P4-T5-012'),player('P4-T5-015','T5_Later'),player('P4-T5-014','T5_AskX'),player('P4-T5-013')],
                                   [npc('P4-T5-017'),npc('P4-T5-016'),0,npc('P4-T5-017')])
    t5_main(st5,done(55,0.0))
    st5b=new_scene('T5b','NN_P4_T5_TalkAgain');t5_main(st5b,b'')
    sra=new_scene('ReAsk','NN_P4_RomanceAgain')
    say(sra,NO,'P4-T5-070',name='Start');say(sra,SY,'P4-T5-071',frag='RM_Reset',name='S071');romance(sra,b'')
    # ---------- ambient exchanges ----------
    for key,edid,seq,actors in (('ExT4a','NN_P4_ExT4a',[(SY,'P4-T4-001'),(NO,'P4-T4-002')],(SY,NO)),
                                ('ExT4b','NN_P4_ExT4b',[(SY,'P4-T4-003'),(NO,'P4-T4-004')],(SY,NO)),
                                ('ExT5a','NN_P4_ExT5a',[(SY,'P4-T5-001'),(NO,'P4-T5-002'),(SY,'P4-T5-003')],(SY,NO)),
                                ('ExT5b','NN_P4_ExT5b',[(NO,'P4-T5-004'),(SY,'P4-T5-005')],(SY,NO)),
                                ('ExT5c','NN_P4_ExT5c',[(NO,'P4-T5-006')],(NO,)),
                                ('ExT5d','NN_P4_ExT5d',[(SY,'P4-T5-007')],(SY,)),
                                ('FU1','NN_P4_Future1',[(SY,'P4-FU-%03d'%i) if i%2 else (NO,'P4-FU-%03d'%i) for i in range(1,8)],(SY,NO)),
                                ('FU2','NN_P4_Future2',[(SY,'P4-FU-010'),(NO,'P4-FU-011'),(NO,'P4-FU-012'),(SY,'P4-FU-013'),(NO,'P4-FU-014')],(SY,NO))):
        s=new_scene(key,edid,actors=actors)
        for j,(al,lid) in enumerate(seq): say(s,al,lid,name='Start' if j==0 else None)
    # kids talk, depending on Shaun: still missing / found and alive (Father) / dead
    met=cond(GetStageDone,MQ207,150,'==',1.0,OR=True)+cond(GetStageDone,MQ207,180,'==',1.0)
    dead=cond(GetDead,0,0,'==',1.0,run=RUN_REF,ref=SHAUN_REF);alive=cond(GetDead,0,0,'==',0.0,run=RUN_REF,ref=SHAUN_REF)
    missing=cond(GetStageDone,MQ207,150,'==',0.0)+cond(GetStageDone,MQ207,180,'==',0.0)+alive
    sfu=new_scene('FU3','NN_P4_Future3')
    say(sfu,NO,'P4-FU-020',missing,name='Start');say(sfu,SY,'P4-FU-021',missing)
    say(sfu,NO,'P4-FU-030',met+alive);say(sfu,SY,'P4-FU-031',met+alive)
    say(sfu,NO,'P4-FU-040',dead);say(sfu,SY,'P4-FU-041',dead)
    # ---------- broken phase ----------
    sbr=new_scene('BR6','NN_P4_Broken',actors=(NO,));say(sbr,NO,'P4-BR-006',frag='BR6_End',name='Start')
    # ---------- Synthetic Love's romance ----------
    sro=new_scene('RO','NN_P4_SynthRomance',optional=(NO,))
    say(sro,SY,'P4-RO-001',name='Start');say(sro,SY,'P4-RO-002')
    say(sro,NO,'P4-RO-010',tier('<=',3),frag='RO_Hate');say(sro,NO,'P4-RO-011',tier('==',4));say(sro,NO,'P4-RO-012',tier('>=',5),frag='RO_Love')
    # ---------- greetings ----------
    broken=g('Broken','==',1);notbroken=g('Broken','==',0)
    synth_near=cond(GetDistance,SLF(SL_NORA_REF),0,'<',1500.0)
    gre=[line_info('P4-T4-010',conds=nora_is+done(25)+done(30,0.0),copy=True,start_scene=st4b.fid,start_phase='Main'),
         line_info('P4-T5-010',conds=nora_is+done(55)+done(60,0.0)+synth_near,copy=True,start_scene=st5b.fid,start_phase='Main'),
         line_info('P4-T5-070',conds=nora_is+g('ReAsk','==',1)+synth_near,copy=True,start_scene=sra.fid,start_phase='S071')]
    # broken: flat greeting, then Synthetic Love's own companion menu (her talk scene)
    in_party=cond(GetInFaction,CURRENT_COMPANION,0,'==',1.0)
    gre+=[line_info('P4-BR-%03d'%i,conds=syn_is+broken+in_party,flags=0x0002,start_scene=SLF(SL_TALK_SCENE),start_phase='Loop') for i in range(1,6)]
    D.topic(alloc(),'GREE',gre,edid='NN_P4_Greetings',priority=100.0)
    D.topic(alloc(),'IDLE',[line_info('P4-BR-%03d'%i,conds=syn_is+broken,flags=0x0002,copy=True) for i in range(1,6)],edid='NN_P4_BrokenIdles')
    # ---------- combat: the other one goes down (Say) ----------
    cb={'TopicDownedSynth':D.topic(alloc(),'SCEN',[line_info('P4-CB-001',conds=syn_is+notbroken)],edid='NN_P4_DownedSynth'),
        'TopicDownedNora':D.topic(alloc(),'SCEN',[line_info('P4-CB-002',conds=nora_is)],edid='NN_P4_DownedNora')}
    D.scenes=[s.build() for s in scenes]
    # ---------- quest ----------
    qprops=[('SynthNoraRef',vm_obj(SLF(SL_NORA_REF))),('NoraRef',vm_obj(NSF(NS_NORA_REF))),('Phase2',vm_obj(O(phase2.P2Q))),('Tier',vm_obj(O(phase2.TIER)))]
    qprops+=[('P2'+k,vm_obj(O(phase2.G[k]))) for k in ('CheckIn','Cruel','T4Adjust','NextEventDay','Waiting')]
    qprops+=[(k,vm_obj(gv(k))) for k in G]
    qprops+=[('SLRomanceQuest',vm_obj(SLF(SL_COMNORA))),('EternalLovers',vm_obj(O(PERK_ID))),('NoraAbility',vm_obj(O(AB_NORA))),
             ('PerkMsg',vm_obj(O(MSG_PERK))),('NothingMsg',vm_obj(O(phase2.MSG_NOTHING))),('HealthAV',vm_obj(HEALTH))]
    qprops+=[('Scene'+k,vm_obj(SC[k].fid)) for k in ('T4','T4b','T5','T5b','ReAsk','BR6','RO','ExT4a','ExT4b','ExT5a','ExT5b','ExT5c','ExT5d','FU1','FU2','FU3')]
    qprops+=[(k,vm_obj(v)) for k,v in cb.items()]
    vm=struct.pack('<hhH',6,2,1)+ws(QS)+struct.pack('<BH',0,len(qprops))+b''.join(ws(n)+v for n,v in qprops)
    q=sub('EDID',zs('NN_Phase4'))+sub('VMAD',vm)+sub('FULL',zs(''))
    q+=sub('DNAM',struct.pack('<HBBII',0x0011,90,0,0,0))+sub('NEXT',b'')
    q+=b''.join(sub('INDX',struct.pack('<HBB',n,0,0))+sub('QSDT',b'\0') for n in STAGES)
    q+=sub('ANAM',struct.pack('<I',2))
    for aid,name,ref in [(A_SYNTH,'SynthNora',SLF(SL_NORA_REF)),(A_NORA,'Nora',NSF(NS_NORA_REF))]:
        q+=sub('ALST',struct.pack('<I',aid))+sub('ALID',zs(name))+sub('FNAM',struct.pack('<I',0x282))+sub('ALFR',struct.pack('<I',ref))+sub('VTCK',struct.pack('<I',0))+sub('ALED',b'')
    quest=record('QUST',Q,0,q)
    child=D.records()
    group=b'GRUP'+struct.pack('<I',24+len(child))+struct.pack('<I',Q)+struct.pack('<IHHHH',10,0,0,0,0)+child
    n=1+len(D.topics)+sum(len(i) for _,_,i in D.topics)+len(D.scenes)
    # ---------- Eternal Lovers ----------
    def spel(fid,edid,name,effects):
        d=sub('EDID',zs(edid))+sub('OBND',bytes(12))+sub('FULL',zs(name))+sub('ETYP',struct.pack('<I',EQUIP_EITHER))+sub('DESC',b'\0')
        d+=sub('SPIT',struct.pack('<IIIfIIffI',0,0,4,0.0,0,0,0.0,0.0,0))
        d+=b''.join(sub('EFID',struct.pack('<I',m))+sub('EFIT',struct.pack('<fII',mag,0,0)) for m,mag in effects)
        return record('SPEL',fid,0,d)
    spells=[spel(O(AB_PLAYER),'NN_AbEternalLoversPlayer',PERK_NAME,[(AB_RESIST[k],50.0) for k in ('Fire','Cryo','Poison')]),
            spel(O(AB_NORA),'NN_AbEternalLoversNora',PERK_NAME,[(AB_FORTIFY_HEALTH,100.0)])]
    perk=record('PERK',O(PERK_ID),0,sub('EDID',zs('NN_EternalLovers'))+sub('FULL',zs(PERK_NAME))+sub('DESC',zs(PERK_DESC))
                +sub('DATA',bytes([0,0,1,0,0]))+sub('PRKE',bytes([1,0,0]))+sub('DATA',struct.pack('<I',O(AB_PLAYER)))+sub('PRKF',b''))
    msg=record('MESG',O(MSG_PERK),0,sub('EDID',zs('NN_EternalLoversMsg'))+sub('DESC',zs(PERK_DESC))+sub('FULL',zs('Perk unlocked: '+PERK_NAME))
               +sub('INAM',b'\0'*4)+sub('DNAM',struct.pack('<I',1))+sub('ITXT',zs('OK')))
    globs=[glob(gv(k),'NN_P4'+k,0.0) for k in G]
    info={'scenes':len(scenes),'topics':len(D.topics),'lines':sum(len(i) for _,_,i in D.topics),'copies':copies,'next_id':nxt[0]}
    return {'quest':quest+group,'qcount':n,'globs':globs,'spells':spells,'perks':[perk],'msgs':[msg],'info':info}

if __name__=='__main__':
    d=sys.argv[1];quest_script(os.path.join(d,QS+'.pex'));tif_script(os.path.join(d,TIF+'.pex'));print('phase 4 scripts ok')
