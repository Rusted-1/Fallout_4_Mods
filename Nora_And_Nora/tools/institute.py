"""Synth Nora comes along to the Institute, like Nora Spouse's Nora does.
The Institute is reached by teleport, so companions are left behind unless something moves them. Vanilla only moves
the one companion the game tracks; Nora Spouse adds its own quest (COMNoraInstituteTeleportEffects) for its Nora.
This does the same for synth Nora:
- Quest NN_SynthNoraInstitute (0xE01, start game enabled) with NN_InstituteTeleportScript.
- OnInit: register for the player's OnLocationChange.
- When the player goes from outside the Institute to inside it, MQ207 stage 200 is done (allowed back in, the same
  condition Nora Spouse uses) and synth Nora is a current companion: move her to MQ302FollowerInstituteTeleportRef
  and give her TeleportPlayerInSpell (the teleport-in effect). Same refs and spell as Nora Spouse's quest.
The inside/outside test copies vanilla InstituteTeleportQuestAliasScript (loc == InstituteLocation or InstituteLocation.IsChild(loc))."""
import os,struct
from build import sub,record,zs,vm_obj,ws
from pexasm import Script,S
import pexw
INST_QUEST=0xE01
SL_NORA_REF=0x000FB3
INSTITUTE_LOC=0x000681AC; FOLLOWER_TP_REF=0x001D3323; TELEPORT_IN_SPELL=0x001E5601
CURRENT_COMPANION=0x00023C01; MQ207=0x000229EC
def script(outdir):
    sc=Script('NN_InstituteTeleportScript','Quest','Nora and Nora: brings synth Nora along when you teleport into the Institute.')
    SYN=sc.prop('SynthNoraRef','objectreference');LOC=sc.prop('InstituteLocation','location');TP=sc.prop('TeleportRef','objectreference')
    SP=sc.prop('TeleportSpell','spell');FAC=sc.prop('CompanionFaction','faction');MQ=sc.prop('MQ207','quest')
    f=sc.func('InInstitute',[('akLoc','location')],'Bool')
    c=f.cmp('cmp_eq','akLoc',LOC);f.jmpt(c,'yes')
    k=f.call(LOC,'IsChild','akLoc');f.jmpt(k,'yes');f.ret(False)
    f.label('yes');f.ret(True)
    f=sc.func('OnInit')
    pl=f.callstatic('game','GetPlayer');so=f.cast(pl,'ScriptObject');f.call('self','RegisterForRemoteEvent',so,S('OnLocationChange'))
    f=sc.func('::remote_Actor_OnLocationChange',[('akSender','actor'),('akOldLoc','location'),('akNewLoc','location')])
    n=f.callself('InInstitute','akNewLoc');f.jmpf(n,'end')
    o=f.callself('InInstitute','akOldLoc');f.jmpt(o,'end')
    d=f.call(MQ,'GetStageDone',200);f.jmpf(d,'end')
    a=f.cast(SYN,'actor');x=f.call(a,'IsInFaction',FAC);f.jmpf(x,'end')
    f.call(SYN,'MoveTo',TP,0.0,0.0,0.0,True);f.call(a,'AddSpell',SP,True)
    f.label('end')
    pexw.write(sc.module(),os.path.join(outdir,'NN_InstituteTeleportScript.pex'))
def record_(own,sl_idx):
    props=[('SynthNoraRef',vm_obj((sl_idx<<24)|SL_NORA_REF)),('InstituteLocation',vm_obj(INSTITUTE_LOC)),('TeleportRef',vm_obj(FOLLOWER_TP_REF)),
           ('TeleportSpell',vm_obj(TELEPORT_IN_SPELL)),('CompanionFaction',vm_obj(CURRENT_COMPANION)),('MQ207',vm_obj(MQ207))]
    vm=struct.pack('<hhH',6,2,1)+ws('NN_InstituteTeleportScript')+struct.pack('<BH',0,len(props))+b''.join(ws(n)+v for n,v in props)
    q=sub('EDID',zs('NN_SynthNoraInstitute'))+sub('VMAD',vm)+sub('FULL',zs(''))
    q+=sub('DNAM',struct.pack('<HBBII',0x0011,10,0,0,0))+sub('NEXT',b'')+sub('ANAM',struct.pack('<I',0))
    return record('QUST',(own<<24)|INST_QUEST,0,q)
