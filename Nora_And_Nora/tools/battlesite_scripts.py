"""Build the battle-site scripts.

NN_FinalWishScript (on BOOK NN_SynthNoraFinalWish, main plugin):
  Event OnRead() -> Phase1.SetStage(430)

NN_BattleSiteScript (on quest NN_BattleSite, Battle Site add-on, next to vanilla REScript):
  Event OnStageSet(int auiStageID, int auiItemID)
    if auiStageID == 10:                       ; start-up stage (set by the RE system)
      (self as REScript).Startup()
      center = CenterMarker.GetReference(); nora = SynthNora.GetActorReference()
      nora.Enable(false); nora.MoveTo(center, 0, 0, 0, true)
      base = nora.GetActorBase(); base.SetEssential(false); base.SetProtected(false)
      for i in NoraItems: nora.AddItem(i, 1, true)              ; light combat arms, medium chest/legs, automatic laser rifle
      nora.AddItem(PlasmaGrenade, 3, true); nora.AddItem(Stimpak, 4, true); nora.AddItem(FinalNote, 1, true)
      frame = center.PlaceAtMe(FrameBase, 1, true, false, false); frame.MoveTo(center, 70, 0, 0, true)
      for i in FrameItems: frame.AddItem(i, 1, true)            ; T-51c pieces
      if UsePowerArmor.GetValue() > 0: Utility.Wait(1.0); nora.SwitchToPowerArmor(frame); Utility.Wait(5.0)
      nora.Kill(None)
      2 coursers + 8 synths: a = center.PlaceActorAtMe(base, 1, None); a.MoveTo(center, dx, dy, 0, false); a.Kill(None)
      SetObjectiveDisplayed(10, true, false); RegisterForRemoteEvent(Phase1, "OnStageSet")
    if auiStageID == 1000:                     ; shut-down stage
      (Trigger.GetReference() as RETriggerScript).ReArmTrigger(); Stop()
  Event Quest.OnStageSet(Quest akSender, int auiStageID, int auiItemID)
    if auiStageID == 430: SetObjectiveCompleted(10, true); UnregisterForRemoteEvent(Phase1, "OnStageSet"); SetStage(1000)
"""
import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from pexasm import Script,S
import pexw
COURSERS=[(-160,130),(190,-100)]
SYNTHS=[(260,60),(-240,-80),(80,300),(-60,-280),(330,-220),(-310,210),(150,-340),(-200,330)]
def final_wish(out):
    sc=Script('NN_FinalWishScript','ObjectReference','Nora and Nora: reading the note completes the battle site.')
    P=sc.prop('Phase1','quest')
    f=sc.func('OnRead');f.call(P,'SetStage',430)
    pexw.write(sc.module(),out)
def battle_site(out):
    sc=Script('NN_BattleSiteScript','Quest','Nora and Nora: synth Nora\'s last stand.')
    PH1=sc.prop('Phase1','quest');NORA=sc.prop('SynthNora','referencealias');CEN=sc.prop('CenterMarker','referencealias')
    TRIG=sc.prop('Trigger','referencealias');COUR=sc.prop('CourserBase','actorbase');SYN=sc.prop('SynthBase','actorbase')
    FRAME=sc.prop('FrameBase','form');FITEMS=sc.prop('FrameItems','formlist');NITEMS=sc.prop('NoraItems','formlist')
    GREN=sc.prop('PlasmaGrenade','form');STIM=sc.prop('Stimpak','form');NOTE=sc.prop('FinalNote','form');USEPA=sc.prop('UsePowerArmor','globalvariable')

    def additems(f,lst,target,tag):
        n=f.call(lst,'GetSize');i=f.local('i_'+tag,'Int');f.op('assign',i,0)
        f.label('loop_'+tag);c=f.cmp('cmp_lt',i,n);f.jmpf(c,'done_'+tag)
        it=f.call(lst,'GetAt',i);f.call(target,'AddItem',it,1,True);f.op('iadd',i,i,1);f.jmp('loop_'+tag)
        f.label('done_'+tag)
    f=sc.func('SetUpSite')
    rs=f.cast('self','rescript');f.call(rs,'Startup')
    center=f.call(CEN,'GetReference');nora=f.call(NORA,'GetActorReference')
    f.call(nora,'Enable',False);f.call(nora,'MoveTo',center,0.0,0.0,0.0,True)
    b=f.call(nora,'GetActorBase');f.call(b,'SetEssential',False);f.call(b,'SetProtected',False)   # she is essential in Synthetic Love
    additems(f,NITEMS,nora,'n')
    f.call(nora,'AddItem',GREN,3,True);f.call(nora,'AddItem',STIM,4,True);f.call(nora,'AddItem',NOTE,1,True)
    frame=f.call(center,'PlaceAtMe',FRAME,1,True,False,False);f.call(frame,'MoveTo',center,70.0,0.0,0.0,True)
    additems(f,FITEMS,frame,'f')
    v=f.call(USEPA,'GetValue');c=f.cmp('cmp_gt',v,0.0);f.jmpf(c,'nopa')
    f.callstatic('utility','Wait',1.0)                                   # let her 3D load after the move
    f.call(nora,'SwitchToPowerArmor',frame);f.callstatic('utility','Wait',5.0)
    f.label('nopa')
    f.call(nora,'Kill',None)
    for base,offs in ((COUR,COURSERS),(SYN,SYNTHS)):
        for dx,dy in offs:
            a=f.call(center,'PlaceActorAtMe',base,1,None);f.call(a,'MoveTo',center,float(dx),float(dy),0.0,False);f.call(a,'Kill',None)
    f.call('self','SetObjectiveDisplayed',10,True,False)
    so=f.cast(PH1,'ScriptObject');f.call('self','RegisterForRemoteEvent',so,S('OnStageSet'))

    f=sc.func('OnStageSet',[('auiStageID','Int'),('auiItemID','Int')])
    c=f.cmp('cmp_eq','auiStageID',10);f.jmpf(c,'not10');f.callself('SetUpSite');f.ret()
    f.label('not10');c=f.cmp('cmp_eq','auiStageID',1000);f.jmpf(c,'end')
    t=f.call(TRIG,'GetReference');rt=f.cast(t,'retriggerscript')
    isnone=f.cmp('cmp_eq',rt,None);f.jmpt(isnone,'stop');f.call(rt,'ReArmTrigger')
    f.label('stop');f.call('self','Stop')
    f.label('end')

    f=sc.func('::remote_Quest_OnStageSet',[('akSender','quest'),('auiStageID','Int'),('auiItemID','Int')])
    c=f.cmp('cmp_eq','auiStageID',430);f.jmpf(c,'end')
    f.call('self','SetObjectiveCompleted',10,True)
    so=f.cast(PH1,'ScriptObject');f.call('self','UnregisterForRemoteEvent',so,S('OnStageSet'))
    f.call('self','SetStage',1000)
    f.label('end')
    pexw.write(sc.module(),out)
if __name__=='__main__':
    d=sys.argv[1];final_wish(os.path.join(d,'NN_FinalWishScript.pex'));battle_site(os.path.join(d,'NN_BattleSiteScript.pex'));print('ok')
