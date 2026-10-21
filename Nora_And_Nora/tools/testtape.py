"""Optional add-on "NoraAndNora - Test Tape.esp": a note that opens a test menu when read.
Menu: Status / Advance to next tier / Set tier 1-5 / Skip current wait / Bring both Noras to me / Reset relationship / Close.
It calls NN_Phase2Script's Debug* functions in NoraAndNora.esp. A note opening a button menu stands in for a holotape:
it needs no terminal record, which can't be built reliably without the Creation Kit.
Usage: python3 -I testtape.py <NoraSpouse.esm (note template)> <out dir>   (writes the plugin and Scripts/*.pex)"""
import sys,os,struct
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from build import sub,record,grup,zs,vm_obj,book,tes4
from scenes_lib import ws
from pexasm import Script
import pexw,phase2
MAIN=1                                            # NoraAndNora.esp master index
TAPE,MENU,TIERMENU,STATUS,GIVER=0x800,0x801,0x802,0x803,0x804
TAPE_TEXT=("NORA AND NORA - TEST TAPE\r\n\r\nFor testing the mod. Close the Pip-Boy after reading this and the menu opens.\r\n\r\n"
           "Status: current tier, gifts, answers and when the next event is due.\r\nAdvance to next tier: plays the next relationship talk now.\r\n"
           "Set tier: jumps to a tier, skipping the talks.\r\nSkip current wait: ends the current timer (patience, battle site, or the next tier).\r\n"
           "Bring both Noras to me: moves both of them to you.\r\nReset relationship: back to tier 1.")
STATUS_TEXT=("Tier: %.0f\nGifts given: %.0f of 5\nCheck-in answer: %.0f  (0 = not yet; 1-4 = choice)\n"
             "Cruel path: %.0f\nHurt: %.0f of 3\nNext event in: %.1f days")
def msgbox(fid,edid,title,body,buttons):
    d=sub('EDID',zs(edid))+sub('DESC',zs(body))+sub('FULL',zs(title))+sub('INAM',b'\0'*4)+sub('DNAM',struct.pack('<I',1))
    d+=b''.join(sub('ITXT',zs(b)) for b in buttons)
    return record('MESG',fid,0,d)
def scripts(outdir):
    phase2.quest_script(os.path.join(outdir,'_unused_p2.pex'));os.remove(os.path.join(outdir,'_unused_p2.pex'))   # registers its functions
    sc=Script('NN_TestTapeScript','ObjectReference','Nora and Nora: test tape menu.')
    P2=sc.prop('Phase2',phase2.QS)
    GV={k:sc.prop(k,'globalvariable') for k in ('Tier','GiftCount','CheckIn','Cruel','Hurt','NextEventDay')}
    M,TM,ST=sc.prop('MainMenu','message'),sc.prop('TierMenu','message'),sc.prop('StatusMsg','message')
    z=[0.0]*9
    f=sc.func('Menu')
    f.label('top')
    b=f.call(M,'Show',*z)
    for i,lab in enumerate(('status','adv','tier','skip','bring','reset')):
        c=f.cmp('cmp_eq',b,i);f.jmpt(c,lab)
    f.ret()
    f.label('status')
    v=[f.call(GV[k],'GetValue') for k in ('Tier','GiftCount','CheckIn','Cruel','Hurt')]
    nd=f.call(GV['NextEventDay'],'GetValue');now=f.callstatic('utility','GetCurrentGameTime');left=f.tmp('Float');f.op('fsub',left,nd,now)
    c=f.cmp('cmp_lt',left,0.0);f.jmpf(c,'show');f.op('assign',left,0.0)
    f.label('show');f.call(ST,'Show',*(v+[left,0.0,0.0,0.0]));f.jmp('top')
    f.label('adv');f.call(P2,'DebugAdvance');f.ret()
    f.label('tier');t=f.call(TM,'Show',*z);c=f.cmp('cmp_ge',t,5);f.jmpt(c,'top')
    n=f.tmp('Int');f.op('iadd',n,t,1);f.call(P2,'DebugSetTier',n);f.ret()
    f.label('skip');f.call(P2,'DebugSkipWait');f.ret()
    f.label('bring');f.call(P2,'DebugBringBoth');f.ret()
    f.label('reset');f.call(P2,'DebugReset')
    f=sc.func('OnRead');f.callself('Menu')
    pexw.write(sc.module(),os.path.join(outdir,'NN_TestTapeScript.pex'))
    g=Script('NN_TestTapeGiverScript','Quest','Nora and Nora: puts the test tape in your inventory once.')
    T=g.prop('Tape','book')
    f=g.func('OnQuestInit')
    pl=f.callstatic('game','GetPlayer');k=f.call(pl,'GetItemCount',T);c=f.cmp('cmp_gt',k,0);f.jmpt(c,'end')
    f.call(pl,'AddItem',T,1,False);f.label('end')
    pexw.write(g.module(),os.path.join(outdir,'NN_TestTapeGiverScript.pex'))
def build(ns_path,outdir):
    os.makedirs(os.path.join(outdir,'Scripts'),exist_ok=True);scripts(os.path.join(outdir,'Scripts'))
    O=lambda i:(2<<24)|i;M_=lambda i:(MAIN<<24)|i
    props=[('Phase2',vm_obj(M_(phase2.P2Q))),('Tier',vm_obj(M_(phase2.TIER)))]+[(k,vm_obj(M_(phase2.G[k]))) for k in ('GiftCount','CheckIn','Cruel','Hurt','NextEventDay')]
    props+=[('MainMenu',vm_obj(O(MENU))),('TierMenu',vm_obj(O(TIERMENU))),('StatusMsg',vm_obj(O(STATUS)))]
    vm=struct.pack('<hhH',6,2,1)+ws('NN_TestTapeScript')+struct.pack('<BH',0,len(props))+b''.join(ws(n)+v for n,v in props)
    tape=book(O(TAPE),'NN_TestTape','Nora and Nora: Test Tape',TAPE_TEXT,ns_path,vmad=vm)
    msgs=[msgbox(O(MENU),'NN_TestTapeMenu','Nora and Nora: Test Tape','What do you want to do?',
                 ['Status','Advance to next tier','Set tier...','Skip current wait','Bring both Noras to me','Reset relationship','Close']),
          msgbox(O(TIERMENU),'NN_TestTapeTierMenu','Set tier','Jump straight to a tier (the talks before it are skipped).',
                 ['Tier 1','Tier 2','Tier 3','Tier 4','Tier 5','Back']),
          msgbox(O(STATUS),'NN_TestTapeStatus','Two Noras: status',STATUS_TEXT,['OK'])]
    gvm=struct.pack('<hhH',6,2,1)+ws('NN_TestTapeGiverScript')+struct.pack('<BH',0,1)+ws('Tape')+vm_obj(O(TAPE))
    giver=record('QUST',O(GIVER),0,sub('EDID',zs('NN_TestTapeGiver'))+sub('VMAD',gvm)+sub('DNAM',bytes.fromhex('110100000000000000000000'))
                 +sub('NEXT',b'')+sub('ANAM',struct.pack('<I',0)))
    body=grup('MESG',b''.join(msgs))+grup('QUST',giver)+grup('BOOK',tape)
    p=os.path.join(outdir,'NoraAndNora - Test Tape.esp')
    open(p,'wb').write(tes4(['Fallout4.esm','NoraAndNora.esp'],5,'Nora & Nora option: test tape (testing menu)',next_id=0x805)+body)
    return p
if __name__=='__main__':
    print(build(sys.argv[1],sys.argv[2]))
