"""Optional add-on "NoraAndNora - Subversion.esp": both Noras react to Subversion's choices (phase3-script.md section 5).
Masters: Fallout4.esm, NoraSpouse.esm, p865_SyntheticLove.esp, NoraAndNora.esp, InstituteReformation.esp.
Quest NN_Subversion (start game enabled) watches Subversion's quest stages (docs/analysis/09-subversion-hooks.md).
Each moment: Synth Nora's reaction pop-up, her line, then Organic Nora's reply if she is with you. Most of these
happen in Institute meetings where companions may not be present, so a moment waits (stage st+1 = pending) and plays
the next time synth Nora is a current companion near you and nobody is fighting.
After the synths are freed, at tier 2 or higher, the scene "They're free... am I?" plays (player choice; the
"not the same" answer counts toward Hurt in NoraAndNora.esp's Phase 2).
Usage: python3 -I subversion.py <NoraSpouse.esm (unused, kept for symmetry)> <out dir> <phase3-script.md> <phase3-subversion-voice-sheet.csv>"""
import sys,os,struct,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from build import sub,record,grup,zs,vm_obj,tes4
from scenes_lib import Dialogue,Scene,cond,GetIsID,GetStageDone,emotion_for,parse_script,voice_ids,frag_vmad,EMO,ws
from pexasm import Script,S
import pexw,phase2
HERE=os.path.dirname(os.path.abspath(__file__))
PLUGIN='NoraAndNora - Subversion.esp'
NS_IDX,SL_IDX,MAIN,SUBV,OWN=1,2,3,4,5
QUEST=0x81B; TOPIC_FIRST=0x820; NATE_FIRST=0x850; SCENE_ID=0x860; NEXT_ID=0x861
QS='NN_SubversionScript'; TIF='NN_SV_TIF'
SL_NORA_REF=0x000FB3; SL_NORA_NPC=0x000F99; NS_NORA_REF=0x001735; NS_NORA_NPC=0x000F9A
SL_KW={'Likes':0x26CD,'Loves':0x26CE,'Dislikes':0x26CB,'Hates':0x26CC}
CURRENT_COMPANION=0x00023C01; TIER=0x804; P2Q=0xB03
SQ={'ReformQuest':0x004C6A,'March':0x006B8B,'Director':0x00B896,'Piper':0x00C10C,'Hope':0x00D9DB,'NextLevel':0x00D6A7,
    'SAllGoodMan':0x00D06B,'InstantKarma':0x00D9C9}
# name: (own stage, reaction, line IDs); pending marker = stage+1
M={'SV001':(10,'Loves',['P3-SV-001']),'SV002':(20,'Likes',['P3-SV-002','P3-SV-003']),'SV010':(30,'Loves',['P3-SV-010','P3-SV-011']),
   'SV012':(40,'Dislikes',['P3-SV-012']),'SV013':(50,'Dislikes',['P3-SV-013','P3-SV-014']),'SV020':(60,'Hates',['P3-SV-020','P3-SV-021']),
   'SV030':(70,'Loves',['P3-SV-030','P3-SV-031']),'SV032':(80,'Likes',['P3-SV-032','P3-SV-033']),'SV040':(90,'Hates',['P3-SV-040','P3-SV-041']),
   'SV042':(100,'Hates',['P3-SV-042','P3-SV-043']),'SV050':(110,'Likes',['P3-SV-050','P3-SV-051'])}
AMI=150; CHOICE_STAGES={'Y':200,'B':201,'X':202,'A':203}
STAGES=[('ReformQuest',20,'SV001'),('March',10,'SV002'),('ReformQuest',75,'SV010'),('ReformQuest',57,'SV012'),('Director',13,'SV013'),
        ('ReformQuest',88,'SV020'),('Piper',100,'SV030'),('Hope',20,'SV032'),('NextLevel',100,'SV040'),('SAllGoodMan',100,'SV042'),
        ('InstantKarma',100,'SV050')]
CHOICES=[('P3-SV-110','Y','Loves'),('P3-SV-111','B','Likes'),('P3-SV-112','X',None),('P3-SV-113','A','Dislikes')]
NPC_REPLY={'Y':'P3-SV-120','B':'P3-SV-121','X':'P3-SV-122','A':'P3-SV-123'}
A_SYNTH,A_NORA=0,1
T_POLL=1
def quest_script(out,L):
    dur=json.load(open(os.path.join(HERE,'phase3_durations.json')))
    sc=Script(QS,'Quest','Nora and Nora: both Noras react to Subversion.')
    SYN=sc.prop('SynthNoraRef','objectreference');NOR=sc.prop('NoraRef','objectreference');FAC=sc.prop('CompanionFaction','faction')
    TIERG=sc.prop('Tier','globalvariable');AMIS=sc.prop('SceneAmI','scene')
    KW={k:sc.prop('Synth'+k,'keyword') for k in SL_KW};QP={k:sc.prop('Q_'+k,'quest') for k in SQ}
    TP={lid:sc.prop('T_'+lid.replace('-','_'),'topic') for m in M.values() for lid in m[2]}
    f=sc.func('Ready',[('akRef','objectreference')],'Bool')
    a=f.cast('akRef','actor');d=f.call(a,'IsDead');f.jmpt(d,'no')
    x=f.call(a,'IsInFaction',FAC);f.jmpf(x,'no')
    pl=f.callstatic('game','GetPlayer');po=f.cast(pl,'objectreference');dist=f.call('akRef','GetDistance',po);c=f.cmp('cmp_lt',dist,3000.0);f.ret(c)
    f.label('no');f.ret(False)
    f=sc.func('CanPlay',[],'Bool')
    r=f.callself('Ready',SYN);f.jmpf(r,'no')
    pl=f.callstatic('game','GetPlayer');cb=f.call(pl,'IsInCombat');f.jmpt(cb,'no')
    a=f.cast(SYN,'actor');s_=f.call(a,'IsInScene');f.jmpt(s_,'no');f.ret(True)
    f.label('no');f.ret(False)
    f=sc.func('React',[('akEvent','keyword')])
    so=f.cast('self','ScriptObject');f.callstatic('followersscript','SendAffinityEvent',so,'akEvent',None,None,True,True,False,0.0)
    f=sc.func('Speak',[('akRef','objectreference'),('akTopic','topic'),('afSeconds','Float')])
    f.call('akRef','Say','akTopic',None,False,None);f.callstatic('utility','Wait','afSeconds')
    f=sc.func('Defer',[('aiPendingStage','Int')])
    f.call('self','SetStage','aiPendingStage');f.call('self','StartTimerGameTime',0.1,T_POLL)
    f=sc.func('M_AMI')
    d=f.call('self','GetStageDone',AMI);f.jmpt(d,'end')
    ok=f.callself('CanPlay');f.jmpt(ok,'go');f.callself('Defer',AMI+1);f.ret()
    f.label('go');f.call('self','SetStage',AMI);f.call(AMIS,'Start')
    f.label('end')
    for name,(st,react,lids) in M.items():
        f=sc.func('M_'+name)
        d=f.call('self','GetStageDone',st);f.jmpt(d,'end')
        ok=f.callself('CanPlay');f.jmpt(ok,'go');f.callself('Defer',st+1);f.ret()
        f.label('go');f.call('self','SetStage',st)
        f.callself('React',KW[react]);f.callstatic('utility','Wait',1.5)
        for i,lid in enumerate(lids):
            who=SYN if L[lid]['speaker']=='SYNTH' else NOR
            if who is NOR: nr=f.callself('Ready',NOR);f.jmpf(nr,'s%d'%i)
            f.callself('Speak',who,TP[lid],float(dur[lid])+0.4);f.label('s%d'%i)
        if name=='SV010':                                    # then "They're free... am I?" at tier 2+
            t=f.call(TIERG,'GetValue');c=f.cmp('cmp_ge',t,2.0);f.jmpf(c,'end')
            f.callstatic('utility','Wait',2.0);f.callself('M_AMI')
        f.label('end')
    f=sc.func('OnInit')
    for k in SQ:
        so=f.cast(QP[k],'ScriptObject');f.call('self','RegisterForRemoteEvent',so,S('OnStageSet'))
    f=sc.func('::remote_Quest_OnStageSet',[('akSender','quest'),('auiStageID','Int'),('auiItemID','Int')])
    for i,(qk,stg,name) in enumerate(STAGES):
        c=f.cmp('cmp_eq','akSender',QP[qk]);f.jmpf(c,'s%d'%i);c2=f.cmp('cmp_eq','auiStageID',stg);f.jmpf(c2,'s%d'%i);f.callself('M_'+name);f.ret();f.label('s%d'%i)
    f=sc.func('OnTimerGameTime',[('aiTimerID','Int')])
    any_=f.local('AnyLeft','Bool');f.op('assign',any_,False)
    for name,(st,_,_) in list(M.items())+[('AMI',(AMI,None,None))]:
        p=f.call('self','GetStageDone',st+1);f.jmpf(p,'n_'+name);d=f.call('self','GetStageDone',st);f.jmpt(d,'n_'+name)
        ok=f.callself('CanPlay');f.jmpf(ok,'w_'+name);f.callself('M_'+name);f.jmp('n_'+name)
        f.label('w_'+name);f.op('assign',any_,True);f.label('n_'+name)
    f.jmpf(any_,'end');f.call('self','StartTimerGameTime',0.1,T_POLL)
    f.label('end')
    pexw.write(sc.module(),out)
def tif_script(out):
    phase2.quest_script(out+'.tmp');os.remove(out+'.tmp')                 # registers NN_Phase2Script's functions (HurtUp)
    sc=Script(TIF,'TopicInfo','Nora and Nora: Subversion scene fragments.')
    KW={k:sc.prop('Synth'+k,'keyword') for k in SL_KW};P2=sc.prop('Phase2',phase2.QS)
    f=sc.func('React',[('akEvent','keyword')])
    so=f.cast('self','ScriptObject');f.callstatic('followersscript','SendAffinityEvent',so,'akEvent',None,None,True,True,False,1.0)
    for lid,btn,react in CHOICES:
        f=sc.func('SV_'+btn,[('akSpeakerRef','objectreference')])
        q=f.call('self','GetOwningQuest');f.call(q,'SetStage',CHOICE_STAGES[btn])
        if react: f.callself('React',KW[react])
        if btn=='A': f.call(P2,'HurtUp')
    pexw.write(sc.module(),out)
def build(outdir,script_md,voice_csv):
    os.makedirs(os.path.join(outdir,'Scripts'),exist_ok=True)
    L,C=parse_script(script_md);V=voice_ids(voice_csv)
    quest_script(os.path.join(outdir,'Scripts',QS+'.pex'),L);tif_script(os.path.join(outdir,'Scripts',TIF+'.pex'))
    O=lambda i:(OWN<<24)|i;SLF=lambda i:(SL_IDX<<24)|i;NSF=lambda i:(NS_IDX<<24)|i
    Q=O(QUEST);D=Dialogue(Q);nxt={'topic':TOPIC_FIRST,'nate':NATE_FIRST}
    def alloc(k): v=nxt[k];nxt[k]+=1;assert v<{'topic':NATE_FIRST,'nate':SCENE_ID}[k];return O(v)
    who={'SYNTH':cond(GetIsID,SLF(SL_NORA_NPC),0,'==',1.0),'NORA':cond(GetIsID,NSF(NS_NORA_NPC),0,'==',1.0)}
    fprops=[('Synth'+k,vm_obj(SLF(v))) for k,v in SL_KW.items()]+[('Phase2',vm_obj((MAIN<<24)|P2Q))]
    def npc(lid,conds=b''):
        ln=L[lid];iid,emo=V[lid]
        info=D.info(O(iid&0xFFFF),ln['text'],emotion_for(ln['delivery'],emo),conds=who[ln['speaker']]+conds)
        return D.topic(alloc('topic'),'SCEN',[info],edid='NN_SV_'+lid.replace('-','_'))
    topics={lid:npc(lid) for m in M.values() for lid in m[2]}
    # scene "They're free... am I?"
    s=Scene(O(SCENE_ID),'NN_SV_AmI',Q,[A_SYNTH,A_NORA],optional=(A_NORA,))
    def say(alias,lid,c=b'',name=None):
        ph=s.phase(name or lid,c);s.line(alias,npc(lid),ph)
    say(A_SYNTH,'P3-SV-100',name='Start');say(A_NORA,'P3-SV-101')
    ph=s.phase('Choice')
    player=[]
    for lid,btn,_ in CHOICES:
        c=C[lid];info=D.info(alloc('nate'),c['line'],EMO['neutral'],prompt=c['label'],vmad=frag_vmad(TIF,'SV_'+btn,fprops))
        player.append(D.topic(alloc('topic'),'SCEN',[info]))
    s.choice(A_SYNTH,ph,player,[npc(NPC_REPLY[b]) for _,b,_ in CHOICES])
    yb=cond(GetStageDone,Q,CHOICE_STAGES['Y'],'==',1.0,OR=True)+cond(GetStageDone,Q,CHOICE_STAGES['B'],'==',1.0)
    say(A_NORA,'P3-SV-124',yb,name='Earned')
    for a in (A_SYNTH,A_NORA): s.package(a,0x00019AA2,0,len(s.phases)-1)
    D.scenes=[s.build()]
    props=[('SynthNoraRef',vm_obj(SLF(SL_NORA_REF))),('NoraRef',vm_obj(NSF(NS_NORA_REF))),('CompanionFaction',vm_obj(CURRENT_COMPANION)),
           ('Tier',vm_obj((MAIN<<24)|TIER)),('SceneAmI',vm_obj(O(SCENE_ID)))]
    props+=[('Synth'+k,vm_obj(SLF(v))) for k,v in SL_KW.items()]+[('Q_'+k,vm_obj((SUBV<<24)|v)) for k,v in SQ.items()]
    props+=[('T_'+lid.replace('-','_'),vm_obj(t)) for lid,t in topics.items()]
    vm=struct.pack('<hhH',6,2,1)+ws(QS)+struct.pack('<BH',0,len(props))+b''.join(ws(n)+v for n,v in props)
    stg=sorted({st for st,_,_ in M.values()}|{st+1 for st,_,_ in M.values()}|{AMI,AMI+1}|set(CHOICE_STAGES.values()))
    q=sub('EDID',zs('NN_Subversion'))+sub('VMAD',vm)+sub('FULL',zs(''))
    q+=sub('DNAM',struct.pack('<HBBII',0x0011,60,0,0,0))+sub('NEXT',b'')
    q+=b''.join(sub('INDX',struct.pack('<HBB',n,0,0))+sub('QSDT',b'\0') for n in stg)
    q+=sub('ANAM',struct.pack('<I',2))
    for aid,name,ref in [(A_SYNTH,'SynthNora',SLF(SL_NORA_REF)),(A_NORA,'Nora',NSF(NS_NORA_REF))]:
        q+=sub('ALST',struct.pack('<I',aid))+sub('ALID',zs(name))+sub('FNAM',struct.pack('<I',0x282))+sub('ALFR',struct.pack('<I',ref))+sub('VTCK',struct.pack('<I',0))+sub('ALED',b'')
    quest=record('QUST',Q,0,q)
    child=D.records()
    group=b'GRUP'+struct.pack('<I',24+len(child))+struct.pack('<I',Q)+struct.pack('<IHHHH',10,0,0,0,0)+child
    n=1+len(D.topics)+sum(len(i) for _,_,i in D.topics)+len(D.scenes)
    body=grup('QUST',quest+group)
    masters=['Fallout4.esm','NoraSpouse.esm','p865_SyntheticLove.esp','NoraAndNora.esp','InstituteReformation.esp']
    p=os.path.join(outdir,PLUGIN)
    open(p,'wb').write(tes4(masters,n,'Nora & Nora option: both Noras react to Subversion',next_id=NEXT_ID)+body)
    os.makedirs(os.path.join(outdir,'SEQ'),exist_ok=True)
    open(os.path.join(outdir,'SEQ',PLUGIN[:-4]+'.seq'),'wb').write(struct.pack('<I',Q))
    return p,{'topics':len(D.topics),'player':nxt['nate']-NATE_FIRST}
if __name__=='__main__':
    print(build(sys.argv[2],sys.argv[3],sys.argv[4]))
