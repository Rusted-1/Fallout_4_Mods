"""Override of Synthetic Love's "Cold Comfort" quest (p865_COMNoraQuest01, 000F9B) so it stays in the Pip-Boy.
Cold Comfort has two objectives: 20 "Travel with Nora to Vault 111 and examine the corpse" and 30 "Talk with Nora".
Up to v0.6.2 we hid 20 (there is no corpse in a Nora Spouse game), which left the quest with nothing displayed,
and a quest with nothing displayed drops out of the quest list. Instead, this copy:
- rewords objective 20 to "Go to Vault 111 with both Noras";
- points its marker alias (NoraCorpseAlias, unique actor 00026F36, the vanilla spouse corpse) at the spouse cryo pod.
  No Synthetic Love script uses that alias (checked in QF_p865_COMNoraQuest01_01000F9B.pex).
Everything else is copied unchanged. The record is identical in all 8 Synthetic Love versions apart from master
indexes and an unused DNAM byte, so one copy (form IDs remapped to our master list) fits them all."""
import struct
from esp import load,subs,z
from build import sub,record,zs
SL_QUEST=0x000F9B; SPOUSE_POD=0x0004A012
OBJ20_TEXT='Go to Vault 111 with both Noras'
def own_index(recs): return len([1 for t,d in subs(recs[0][3]) if t=='MAST'])
def record_(sl_path,idx_sl):
    recs=load(sl_path);own=own_index(recs)
    src=[x for x in recs if x[0]=='QUST' and x[1]&0xFFFFFF==SL_QUEST][0]
    sl_ids={fid for t,fid,fl,d in recs if fid>>24==own}
    out=b'';obj=None;alias=None
    for t,x in subs(src[3]):
        if t=='QOBJ': obj=struct.unpack_from('<H',x)[0]
        if t=='ALST': alias=struct.unpack_from('<I',x)[0]
        if t=='NNAM' and obj==20: x=zs(OBJ20_TEXT)
        if t=='ALUA' and alias==1:                       # corpse -> cryo pod (forced reference)
            out+=sub('ALFR',struct.pack('<I',SPOUSE_POD));continue
        x=bytearray(x)
        if t in('VMAD','ALUA','XNAM'):
            for i in range(len(x)-3):
                v=struct.unpack_from('<I',x,i)[0]
                if v in sl_ids: struct.pack_into('<I',x,i,(idx_sl<<24)|(v&0xFFFFFF))
        out+=sub(t,bytes(x))
    return record('QUST',(idx_sl<<24)|SL_QUEST,src[2]&~0x40000,out)
