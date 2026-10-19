import sys, struct; sys.path.insert(0,'tools')
from build import *
PARTS=['Helm','Torso','ArmLeft','ArmRight','LegLeft','LegRight']
SETS=[('rr','Armor_Power_Scrapper_'),('cw','00RaidT45Armor_Power_RaidT45_'),('rk','Armor_Power_RaiderBrute_')]
WB_CHEM, CAT_UTIL = 0x102158, 0x6980C
recs=[]; nid=0x800
for k,pre in SETS:
    f=remapper(k)
    for p in PARTS:
        a=SRC[k]['byedid'][pre+p]
        subs=[('EDID',zstr('RPA_Debug_co_'+pre+p)),('DESC',b'\0'),('CNAM',p32(f(a['fid']))),
              ('BNAM',p32(WB_CHEM)),('FNAM',p32(CAT_UTIL)),('INTV',p32(1))]
        recs.append(rec('COBJ',0,(SELF<<24)|nid,subs)); nid+=1
hsubs=[('HEDR',struct.pack('<fII',1.0,len(recs),nid)),('CNAM',zstr('RPA_Fixes')),
       ('SNAM',zstr('DEBUG: free Chem Station (Utility) recipes for every Scrapper, Raider T-45 and Raider Brute power armor piece.'))]
for m in OUTMAST: hsubs+=[('MAST',zstr(m)),('DATA',b'\0'*8)]
open(sys.argv[1],'wb').write(rec('TES4',0x200,0,hsubs)+grup('COBJ',recs))
print(len(recs),'recipes')
