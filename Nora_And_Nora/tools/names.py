"""Who is who: synth Nora is shown as "Synth Nora", and her affinity messages say so.
- NN_Names (quest, always running): one alias forced to synth Nora's reference with a display name.
  An alias display name works for all 8 Synthetic Love versions, unlike editing her NPC record (which differs per version).
- Synthetic Love's four affinity messages (identical in all 8 versions) are reworded: "Synth Nora liked that." etc.
Nora Spouse's own messages ("Nora liked that.") are left alone."""
import struct
from build import sub,record,zs
NAMES_QUEST=0xB01; NAME_MSG=0xB02
SL_NORA_REF=0x000FB3
SL_MESSAGES={0x26C1:('p865_CA_Nora_likes','Synth Nora liked that.'),0x26C2:('p865_CA_Nora_Loves','Synth Nora loved that.'),
             0x26BF:('p865_CA_Nora_Dislikes','Synth Nora disliked that.'),0x26C0:('p865_CA_Nora_Hates','Synth Nora hated that.')}
def mesg(fid,edid,desc,full):
    d=sub('EDID',zs(edid))+sub('DESC',zs(desc))+sub('FULL',zs(full))+sub('INAM',b'\0'*4)+sub('DNAM',b'\0'*4)+sub('TNAM',struct.pack('<I',2))
    return record('MESG',fid,0,d)
def records(own,sl_idx):
    O=lambda i:(own<<24)|i
    msgs=[mesg(O(NAME_MSG),'NN_SynthNoraName','','Synth Nora')]
    msgs+=[mesg((sl_idx<<24)|i,e,t,t) for i,(e,t) in sorted(SL_MESSAGES.items())]
    q=sub('EDID',zs('NN_Names'))+sub('FULL',zs(''))
    q+=sub('DNAM',struct.pack('<HBBII',0x0111,10,0,0,0))+sub('NEXT',b'')
    q+=sub('ANAM',struct.pack('<I',1))
    q+=sub('ALST',struct.pack('<I',0))+sub('ALID',zs('SynthNora'))+sub('FNAM',struct.pack('<I',0x282))
    q+=sub('ALFR',struct.pack('<I',(sl_idx<<24)|SL_NORA_REF))+sub('ALDN',struct.pack('<I',O(NAME_MSG)))+sub('VTCK',struct.pack('<I',0))+sub('ALED',b'')
    return msgs,record('QUST',O(NAMES_QUEST),0,q)
