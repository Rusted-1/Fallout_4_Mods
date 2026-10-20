"""Assemble NN_KelloggGateScript.pex (Fallout 4 Papyrus bytecode) without the Creation Kit.

Equivalent Papyrus source:

  Scriptname NN_KelloggGateScript extends Quest
  Quest Property MQ106 Auto Const
  Int Property KelloggDeadStage = 902 Auto Const
  GlobalVariable Property AdmirationAllowed Auto Const      ; patch global, starts at 0
  ObjectReference Property SynthNoraRef Auto Const          ; Synthetic Love's Nora (ACHR 000FB3)
  ActorValue Property CA_Affinity Auto Const
  GlobalVariable Property CA_T2_Admiration Auto Const       ; vanilla Admiration threshold (500)

  Event OnQuestInit()
      If MQ106.GetStageDone(KelloggDeadStage)               ; Kellogg already dead: nothing to lock
          Stop()
          Return
      EndIf
      If SynthNoraRef.GetValue(CA_Affinity) >= CA_T2_Admiration.GetValue()
          Stop()                                            ; already past Admiration: leave her alone
          Return
      EndIf
      CompanionActorScript cas = SynthNoraRef as CompanionActorScript
      If cas == None
          Stop()
          Return
      EndIf
      CompanionActorScript:ThresholdData[] arr = cas.ThresholdData_Array
      Int i = 0
      While i < arr.Length
          If arr[i].Threshold_Global == CA_T2_Admiration
              arr[i].ConditionalGlobal = AdmirationAllowed  ; vanilla script caps affinity below a locked threshold
          EndIf
          i += 1
      EndWhile
      RegisterForRemoteEvent(MQ106, "OnStageSet")
  EndEvent

  Event Quest.OnStageSet(Quest akSender, Int auiStageID, Int auiItemID)
      If auiStageID == KelloggDeadStage
          Unlock()
      EndIf
  EndEvent

  Function Unlock()
      AdmirationAllowed.SetValue(1.0)
      UnregisterForRemoteEvent(MQ106, "OnStageSet")
      Stop()
  EndFunction
"""
import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import pexw
I=lambda s:('id',s)
STR=lambda s:('str',s)
NAME='NN_KelloggGateScript'
PROPS=[('MQ106','quest'),('KelloggDeadStage','Int'),('AdmirationAllowed','globalvariable'),
       ('SynthNoraRef','objectreference'),('CA_Affinity','actorvalue'),('CA_T2_Admiration','globalvariable')]
def fn(params,locals_,code,ret='None'):
    return {'ret':ret,'doc':'','uflags':0,'flags':0,'params':params,'locals':locals_,'code':code}
def v(n): return I('::%s_var'%n)
CAS='companionactorscript';TD='companionactorscript#thresholddata'
oninit=fn([],[('::temp0','Bool'),('::temp1','Float'),('::temp2','Float'),('::temp3','Bool'),('::temp4',CAS),
              ('::temp5',TD+'[]'),('::temp6','Int'),('i','Int'),('::temp7',TD),('::temp8','globalvariable'),
              ('::temp9','Bool'),('::temp10','ScriptObject'),('::temp11','Bool'),('::nonevar','None')],[
 ('callmethod',[I('GetStageDone'),v('MQ106'),I('::temp0'),v('KelloggDeadStage')]),   # 0
 ('jmpf',[I('::temp0'),3]),                                                          # 1 -> 4
 ('callmethod',[I('Stop'),I('self'),I('::nonevar')]),                                # 2
 ('return',[None]),                                                                  # 3
 ('callmethod',[I('GetValue'),v('SynthNoraRef'),I('::temp1'),v('CA_Affinity')]),    # 4
 ('callmethod',[I('GetValue'),v('CA_T2_Admiration'),I('::temp2')]),                 # 5
 ('cmp_ge',[I('::temp3'),I('::temp1'),I('::temp2')]),                               # 6
 ('jmpf',[I('::temp3'),3]),                                                          # 7 -> 10
 ('callmethod',[I('Stop'),I('self'),I('::nonevar')]),                                # 8
 ('return',[None]),                                                                  # 9
 ('cast',[I('::temp4'),v('SynthNoraRef')]),                                          # 10
 ('cmp_eq',[I('::temp3'),I('::temp4'),None]),                                        # 11
 ('jmpf',[I('::temp3'),3]),                                                          # 12 -> 15
 ('callmethod',[I('Stop'),I('self'),I('::nonevar')]),                                # 13
 ('return',[None]),                                                                  # 14
 ('propget',[I('ThresholdData_Array'),I('::temp4'),I('::temp5')]),                  # 15
 ('array_length',[I('::temp6'),I('::temp5')]),                                       # 16
 ('assign',[I('i'),0]),                                                              # 17
 ('cmp_lt',[I('::temp3'),I('i'),I('::temp6')]),                                      # 18
 ('jmpf',[I('::temp3'),9]),                                                          # 19 -> 28
 ('array_getelement',[I('::temp7'),I('::temp5'),I('i')]),                            # 20
 ('struct_get',[I('::temp8'),I('::temp7'),I('Threshold_Global')]),                   # 21
 ('cmp_eq',[I('::temp9'),I('::temp8'),v('CA_T2_Admiration')]),                       # 22
 ('jmpf',[I('::temp9'),2]),                                                          # 23 -> 25
 ('struct_set',[I('::temp7'),I('ConditionalGlobal'),v('AdmirationAllowed')]),        # 24
 ('iadd',[I('i'),I('i'),1]),                                                         # 25
 ('jmp',[-8]),                                                                       # 26 -> 18
 ('nop',[]),                                                                         # 27
 ('cast',[I('::temp10'),v('MQ106')]),                                                # 28
 ('callmethod',[I('RegisterForRemoteEvent'),I('self'),I('::temp11'),I('::temp10'),STR('OnStageSet')]), # 29
])
onstage=fn([('akSender','quest'),('auiStageID','Int'),('auiItemID','Int')],[('::temp0','Bool'),('::nonevar','None')],[
 ('cmp_eq',[I('::temp0'),I('auiStageID'),v('KelloggDeadStage')]),
 ('jmpf',[I('::temp0'),2]),
 ('callmethod',[I('Unlock'),I('self'),I('::nonevar')]),
])
unlock=fn([],[('::temp0','ScriptObject'),('::nonevar','None')],[
 ('callmethod',[I('SetValue'),v('AdmirationAllowed'),I('::nonevar'),1.0]),
 ('cast',[I('::temp0'),v('MQ106')]),
 ('callmethod',[I('UnregisterForRemoteEvent'),I('self'),I('::nonevar'),I('::temp0'),STR('OnStageSet')]),
 ('callmethod',[I('Stop'),I('self'),I('::nonevar')]),
])
def module():
    return {'src':NAME+'.psc','user':'Rusted-1','machine':'NoraAndNora','time':1792460000,
     'userflags':[('hidden',0),('conditional',1),('default',2),('collapsedonref',3),('collapsedonbase',4),('mandatory',5)],
     'objects':[{'name':NAME,'parent':'Quest','doc':'Nora and Nora: holds synth Nora below Admiration until Kellogg is dead.',
       'const':0,'uflags':0,'auto':'','structs':[],
       'vars':[('::%s_var'%n,t,0,None,1) for n,t in PROPS],
       'props':[{'name':n,'type':t,'doc':'','uflags':0,'flags':7,'auto':'::%s_var'%n} for n,t in PROPS],
       'states':[('',[('OnQuestInit',oninit),('::remote_Quest_OnStageSet',onstage),('Unlock',unlock)])]}]}
if __name__=='__main__':
    out=sys.argv[1] if len(sys.argv)>1 else NAME+'.pex'
    pexw.write(module(),out);print(out)
