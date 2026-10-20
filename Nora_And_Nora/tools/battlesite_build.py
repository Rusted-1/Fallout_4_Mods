"""Build 'NoraAndNora - Battle Site.esp' (needs all three DLCs + Random Encounter Framework).
Usage: python3 -I battlesite_build.py <REFramework Example Plugin.esp> <out dir>"""
import sys,os,struct
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from esp import load,subs,z
from build import sub,record,grup,tes4,vm_obj,ws,zs,glob,SL_NORA_REF,PH1_ID,FINALNOTE_ID
PLUGIN='NoraAndNora - Battle Site.esp'
MASTERS=['Fallout4.esm','DLCRobot.esm','DLCCoast.esm','DLCNukaWorld.esm','REFramework.esm','p865_SyntheticLove.esp','NoraAndNora.esp']
SL,NN,OWN=5,6,7
QID,FLST_FRAME,FLST_NORA,GLOB_PA,SMQN_ID=0x800,0x801,0x802,0x803,0x804
REPARENT=0x0002DFEE
RESCENE_PARENT=(4<<24)|0x20          # REFramework RESceneQuestsParent
COURSER=0x001EB9A7                    # LvlSynthCourserNoTeleport
SYNTH=0x0009317E                      # LvlSynthAmbush
FRAME=0x0002079E                      # PowerArmorFrameFurnitureNoCore
PLASMA_GRENADE=0x0010A33D;STIMPAK=0x00023736
T51C=[0x0022BEED,0x0022BEFC,0x0022BEE3,0x0022BEE8,0x0022BEF2,0x0022BEF7]   # LL_Armor_Power_T51_{Helmet,Torso,ArmLeft,ArmRight,LegLeft,LegRight}_C
NORA_ITEMS=[0x00184BD0,0x00184BCD,0x00184BC3,0x00184BC9,0x00184BC6,0x001879EA]  # combat arms Light L/R, torso Medium, legs Medium L/R, LL_LaserGun_Rifle_Auto
A_TRIGGER,A_CENTER,A_NORA=1,10,40
def own(i): return (OWN<<24)|i
def vm_alias(quest,alias): return struct.pack('<BBHhI',1,1,0,alias,quest)
def alias_block(s,alias_id):
    """Return the raw subrecords of one alias from the example quest."""
    out=[];on=False
    for k,x in s:
        if k=='ALST': on=struct.unpack('<I',x)[0]==alias_id
        if on: out.append((k,x))
        if on and k=='ALED': break
    return b''.join(sub(k,x) for k,x in out)
def build(example,outdir):
    ex=load(example);exq=[r for r in ex if r[0]=='QUST'][0];exn=[r for r in ex if r[0]=='SMQN'][0]
    qs=subs(exq[3])
    re_props=[('REParent',vm_obj(REPARENT)),('RegisteredAliases',struct.pack('<BBI',11,1,0))]
    bs_props=[('Phase1',vm_obj((NN<<24)|PH1_ID)),('SynthNora',vm_alias(own(QID),A_NORA)),('CenterMarker',vm_alias(own(QID),A_CENTER)),
              ('Trigger',vm_alias(own(QID),A_TRIGGER)),('CourserBase',vm_obj(COURSER)),('SynthBase',vm_obj(SYNTH)),('FrameBase',vm_obj(FRAME)),
              ('FrameItems',vm_obj(own(FLST_FRAME))),('NoraItems',vm_obj(own(FLST_NORA))),('PlasmaGrenade',vm_obj(PLASMA_GRENADE)),
              ('Stimpak',vm_obj(STIMPAK)),('FinalNote',vm_obj((NN<<24)|FINALNOTE_ID)),('UsePowerArmor',vm_obj(own(GLOB_PA)))]
    def script(name,props): return ws(name)+struct.pack('<BH',0,len(props))+b''.join(ws(n)+b for n,b in props)
    vm=struct.pack('<hhH',6,2,2)+script('REScript',re_props)+script('NN_BattleSiteScript',bs_props)
    d=dict(qs);q=b''
    q+=sub('EDID',zs('NN_BattleSite'))+sub('VMAD',vm)+sub('FULL',zs('The Battle Site'))+sub('DNAM',d['DNAM'])+sub('ENAM',d['ENAM'])
    q+=sub('FLTR',zs('Nora and Nora\\'))+sub('NEXT',b'')
    q+=b''.join(sub('CTDA',x) for k,x in qs[qs.index(('NEXT',b''))+1:] if k=='CTDA' and qs.index((k,x))<[i for i,(kk,_) in enumerate(qs) if kk=='INDX'][0])
    q+=sub('INDX',struct.pack('<HBB',10,0x02,0))+sub('QSDT',b'\0')+sub('INDX',struct.pack('<HBB',1000,0x04,0))+sub('QSDT',b'\0')
    q+=sub('QOBJ',struct.pack('<H',10))+sub('FNAM',struct.pack('<I',0))+sub('NNAM',zs('Investigate the battle site'))+sub('QSTA',struct.pack('<iII',A_NORA,0,0))
    q+=sub('ANAM',struct.pack('<I',A_NORA+1))
    q+=alias_block(qs,A_TRIGGER)+alias_block(qs,A_CENTER)
    q+=(sub('ALST',struct.pack('<I',A_NORA))+sub('ALID',zs('SynthNora'))+sub('FNAM',struct.pack('<I',0x282))
        +sub('ALFR',struct.pack('<I',(SL<<24)|SL_NORA_REF))+sub('VTCK',struct.pack('<I',0))+sub('ALED',b''))
    quest=record('QUST',own(QID),0,q)
    flst=lambda fid,ed,items: record('FLST',fid,0,sub('EDID',zs(ed))+b''.join(sub('LNAM',struct.pack('<I',i)) for i in items))
    lists=[flst(own(FLST_FRAME),'NN_BattleSiteFrameItems',T51C),flst(own(FLST_NORA),'NN_BattleSiteNoraItems',NORA_ITEMS)]
    g=glob(own(GLOB_PA),'NN_BattleSitePowerArmor',1.0)
    # Story Manager node: under REFramework's RESceneQuestsParent (random parent), no previous sibling
    ns=subs(exn[3]);n=b''
    cond=lambda fn,p1,p2,val: struct.pack('<B3xfH2xIIIIi',0x00,val,fn,p1,p2,0,0,-1)
    for k,x in ns:
        if k=='EDID': x=zs('NN_BattleSiteNode')
        elif k=='PNAM': x=struct.pack('<I',RESCENE_PARENT)
        elif k=='SNAM': x=struct.pack('<I',0)
        elif k=='CITC': x=struct.pack('<I',3)
        elif k=='CTDA':
            x=bytes([0x00])+x[1:]                                    # AND with ours
            n+=sub(k,x)+sub('CTDA',cond(59,(NN<<24)|PH1_ID,420,1.0))+sub('CTDA',cond(59,(NN<<24)|PH1_ID,430,0.0));continue
        elif k=='NNAM': x=struct.pack('<I',own(QID))
        n+=sub(k,x)
    node=record('SMQN',own(SMQN_ID),0,n)
    body=grup('GLOB',g)+grup('FLST',b''.join(lists))+grup('QUST',quest)+grup('SMQN',node)
    os.makedirs(outdir,exist_ok=True);p=os.path.join(outdir,PLUGIN)
    h=tes4(MASTERS,5,"Nora & Nora add-on: synth Nora's battle site (needs all DLCs + Random Encounter Framework)")
    h=h[:24]+h[24:].replace(struct.pack('<fII',1.0,5,0x808),struct.pack('<fII',1.0,5,0x805))
    open(p,'wb').write(h+body);return p
if __name__=='__main__': print(build(sys.argv[1],sys.argv[2]))
