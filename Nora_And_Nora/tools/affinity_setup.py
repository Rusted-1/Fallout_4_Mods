"""Makes synth Nora's like/love/dislike/hate reactions work on an existing save.
Why: FollowersScript only reacts to keywords listed in its AffinityEvents array. That array is a script
property, so its value lives in the save game: edits to the Followers quest record (Synthetic Love's,
or our UCF merge) never reach a save where the Followers quest already ran. Nora Spouse avoids this by
appending her events at runtime (NoraFollowerDataScript). This does the same for Synthetic Love's four.
- Quest NN_AffinitySetup (0xE00, start game enabled) with NN_AffinitySetupScript.
- OnInit: for each event in its own AffinityEvents property, if FollowersScript.GetAffinityEventData(keyword)
  finds nothing, the event is appended to Followers.AffinityEvents. Safe to run on a save that already has them."""
import os,struct
from build import sub,record,zs,ws
from pexasm import Script
import pexw
SETUP_QUEST=0xE00
SL_EVENTS=(0x26CB,0x26CC,0x26CD,0x26CE)          # Synthetic Love: Dislikes, Hates, Likes, Loves
EVENT_SIZE=0x018CFF; COOLDOWN=0x0A1B7C           # same values Synthetic Love's own entries use
ST='followersscript#affinityeventdata'
def script(outdir):
    sc=Script('NN_AffinitySetupScript','Quest',"Nora and Nora: adds Synthetic Love's affinity events to the running Followers quest.")
    EV=sc.prop('AffinityEvents',ST+'[]')
    f=sc.func('OnInit')
    i=f.local('I','Int');f.op('assign',i,0)
    f.label('loop')
    n=f.tmp('Int');f.op('array_length',n,EV)
    c=f.cmp('cmp_lt',i,n);f.jmpf(c,'end')
    item=f.tmp(ST);f.op('array_getelement',item,EV,i)
    kw=f.tmp('keyword');f.op('struct_get',kw,item,'EventKeyword')
    have=f.callstatic('followersscript','GetAffinityEventData',kw)
    miss=f.tmp('Bool');f.op('not',miss,have);f.jmpf(miss,'next')
    fs=f.callstatic('followersscript','GetScript')
    arr=f.tmp(ST+'[]');f.op('propget','AffinityEvents',fs,arr)
    f.op('array_add',arr,item,1)
    f.label('next');f.op('iadd',i,i,1);f.jmp('loop')
    f.label('end')
    pexw.write(sc.module(),os.path.join(outdir,'NN_AffinitySetupScript.pex'))
def _obj(fid): return struct.pack('<BBHhI',1,1,0,-1,fid)[2:]   # value only (type/status written by caller)
def _member(name,t,val): return ws(name)+struct.pack('<BB',t,1)+val
def record_(own,sl_idx):
    structs=b''
    for k in SL_EVENTS:
        m=[_member('EventSize',1,_obj(EVENT_SIZE)),_member('CoolDownDays',1,_obj(COOLDOWN)),_member('EventKeyword',1,_obj((sl_idx<<24)|k))]
        structs+=struct.pack('<I',len(m))+b''.join(m)
    prop=ws('AffinityEvents')+struct.pack('<BBI',17,1,len(SL_EVENTS))+structs
    vm=struct.pack('<hhH',6,2,1)+ws('NN_AffinitySetupScript')+struct.pack('<BH',0,1)+prop
    q=sub('EDID',zs('NN_AffinitySetup'))+sub('VMAD',vm)+sub('FULL',zs(''))
    q+=sub('DNAM',struct.pack('<HBBII',0x0111,10,0,0,0))+sub('NEXT',b'')+sub('ANAM',struct.pack('<I',0))
    return record('QUST',(own<<24)|SETUP_QUEST,0,q)
