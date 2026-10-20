"""Build NN_Phase1Script.pex: Phase 1 outcome system (Vault 111 choice, waiting, leaving, battle-site eligibility).

Stages of quest NN_Phase1 (set by the Phase 1 dialogue, or by console for testing):
  100  Choice 1 - synth Nora stays a companion. Relationship tier -> 1.
  200  Choice 2 - she waits in Vault 111. With the "leaves after a while" option: 7-day timer.
  300  Choice 3 - she turns hostile (essential/protected flags cleared first).
  400  Choice 4 - dismissed; waits in Vault 111 for 3 days, then leaves.
  410  She has left the vault (disabled).
  420  Battle site eligible (Random Encounter add-on checks this stage).
Timers (game hours): 1 = patience (168), 2 = choice-4 wait (72), 3 = gear-up after a patience exit (72).

Equivalent Papyrus (abridged):
  Event OnStageSet(int auiStageID, int auiItemID)
    if auiStageID == 100  -> EndWait(); RelationTier.SetValue(1); if GetStageDone(200) -> nora.SetCompanion(true, true)
    if auiStageID == 200  -> Dismiss(); BeginWait(); if Impatient.GetValue() > 0 -> StartTimerGameTime(168, 1)
    if auiStageID == 300  -> EndWait(); Release(); base.SetEssential(false); base.SetProtected(false)
                             nora.RemoveFromAllFactions(); nora.StartCombat(Game.GetPlayer(), true)
    if auiStageID == 400  -> Release(); BeginWait(); StartTimerGameTime(72, 2)
    if auiStageID == 410  -> EndWait(); nora.Disable(false)
  Event OnTimerGameTime(int aiTimerID)
    1: if no choice made since (100/300/400 not done) -> PlaceAtMe(WaitNote) on her pod; Release(); SetStage(410); StartTimerGameTime(72, 3)
    2: SetStage(410); SetStage(420)
    3: SetStage(420)
"""
import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from pexasm import Script
import pexw
def build(out):
    sc=Script('NN_Phase1Script','Quest','Nora and Nora: Phase 1 outcomes for synth Nora.')
    NORA=sc.prop('SynthNoraRef','objectreference');FOL=sc.prop('Followers','followersscript')
    WAIT=sc.prop('WaitQuest','quest');ANCHOR=sc.prop('VaultAnchor','objectreference')
    TIER=sc.prop('RelationTier','globalvariable');IMP=sc.prop('Impatient','globalvariable')
    NOTE=sc.prop('WaitNote','book');POD=sc.prop('NoteAnchor','objectreference')

    # Function BeginWait(): move to the pod, start the sandbox-alias quest
    f=sc.func('BeginWait')
    f.call(NORA,'MoveTo',ANCHOR,0.0,0.0,0.0,True)
    f.call(WAIT,'Start')
    a=f.cast(NORA,'actor');f.call(a,'EvaluatePackage',False)
    # Function EndWait(): stop the sandbox quest and any pending timers
    f=sc.func('EndWait')
    f.call(WAIT,'Stop');f.call('self','CancelTimerGameTime',1);f.call('self','CancelTimerGameTime',2)
    a=f.cast(NORA,'actor');f.call(a,'EvaluatePackage',False)
    # Function Dismiss(): stop following, but can still be recruited (choice 2)
    f=sc.func('Dismiss')
    a=f.cast(NORA,'actor')
    f.call(FOL,'DismissCompanion',a,False,True)
    # Function Release(): no longer a companion at all (choices 3 and 4)
    f=sc.func('Release')
    f.callself('Dismiss')
    a=f.cast(NORA,'actor')
    f.call(a,'DisallowCompanion',True)

    f=sc.func('OnStageSet',[('auiStageID','Int'),('auiItemID','Int')])
    for st,lab in [(100,'s100'),(200,'s200'),(300,'s300'),(400,'s400'),(410,'s410')]:
        c=f.cmp('cmp_eq','auiStageID',st);f.jmpt(c,lab)
    f.ret()
    f.label('s100');f.callself('EndWait');f.call(TIER,'SetValue',1.0)
    d=f.call('self','GetStageDone',200);f.jmpf(d,'end')            # came back after waiting: re-recruit
    a=f.cast(NORA,'actor');f.call(a,'SetCompanion',True,True);f.ret()
    f.label('s200');f.callself('Dismiss');f.callself('BeginWait')
    v=f.call(IMP,'GetValue');c=f.cmp('cmp_gt',v,0.0);f.jmpf(c,'end')
    f.call('self','StartTimerGameTime',168.0,1);f.ret()
    f.label('s300');f.callself('EndWait');f.callself('Release')
    a=f.cast(NORA,'actor');b=f.call(a,'GetActorBase')
    f.call(b,'SetEssential',False);f.call(b,'SetProtected',False)
    f.call(a,'RemoveFromAllFactions');p=f.callstatic('game','GetPlayer');f.call(a,'StartCombat',p,True);f.ret()
    f.label('s400');f.callself('Release');f.callself('BeginWait');f.call('self','StartTimerGameTime',72.0,2);f.ret()
    f.label('s410');f.callself('EndWait');f.call(NORA,'Disable',False);f.ret()
    f.label('end')

    f=sc.func('OnTimerGameTime',[('aiTimerID','Int')])
    c=f.cmp('cmp_eq','aiTimerID',1);f.jmpt(c,'t1')
    c=f.cmp('cmp_eq','aiTimerID',2);f.jmpt(c,'t2')
    c=f.cmp('cmp_eq','aiTimerID',3);f.jmpt(c,'t3');f.ret()
    f.label('t1')
    for st in (100,300,400):
        d=f.call('self','GetStageDone',st);f.jmpt(d,'end')
    f.call(POD,'PlaceAtMe',NOTE,1,True,False,False)
    f.callself('Release');f.call('self','SetStage',410);f.call('self','StartTimerGameTime',72.0,3);f.ret()
    f.label('t2');f.call('self','SetStage',410);f.call('self','SetStage',420);f.ret()
    f.label('t3');f.call('self','SetStage',420)
    f.label('end')
    pexw.write(sc.module(),out);return sc
if __name__=='__main__':
    build(sys.argv[1]);print(sys.argv[1])
