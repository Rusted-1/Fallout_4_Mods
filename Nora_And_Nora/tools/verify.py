"""Check a built NoraAndNora.esp against the source plugins.
Usage: python3 -I verify.py <built UCF/NoraAndNora.esp> <EFF.esp> <p865_SyntheticLove.esp>"""
import sys,os,struct,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from esp import load,subs,z
from vmad import parse
built,eff,sl=sys.argv[1:4]
b=open(built,'rb').read()
def walk(s,e):
    i=s;n=0
    while i<e:
        t=b[i:i+4];sz=struct.unpack_from('<I',b,i+4)[0]
        if t==b'GRUP': n+=walk(i+24,i+sz);i+=sz
        else: i+=24+sz;n+=1
    assert i==e,'group sizes do not line up';return n
def norm(v):
    if isinstance(v,dict): return {k.lower():norm(x) for k,x in sorted(v.items(),key=lambda a:a[0].lower())}
    if isinstance(v,(list,tuple)): return [norm(x) for x in v]
    return v
print('records:',walk(0,len(b)))
P=load(built);masters=[z(d) for t,d in subs(P[0][3]) if t=='MAST'];print('masters:',masters,'ESL' if P[0][2]&0x200 else 'not ESL')
F=lambda recs:[x for x in recs if x[1]==0x289E4][0]
ps=subs(F(P)[3]);es=subs(F(load(eff))[3]);ss=subs(F(load(sl))[3])
assert [x for t,x in ps if t!='VMAD']==[x for t,x in es if t!='VMAD'],'non-script data differs from UCF'
pv,pr=parse(dict(ps)['VMAD']);ev,er=parse(dict(es)['VMAD']);sv,_=parse(dict(ss)['VMAD'])
assert dict(ps)['VMAD'][pr.i:]==dict(es)['VMAD'][er.i:],'fragments/aliases differ from UCF'
changed=[(s,k) for s in ev for k in ev[s] if norm(pv[s][k])!=norm(ev[s][k])]
assert sorted(changed)==[('followersscript','AffinityEvents'),('followersscript','ExtensionHooks')],changed
pa=norm(pv['followersscript']['AffinityEvents'])[1];ea=norm(ev['followersscript']['AffinityEvents'])[1];sa=norm(sv['followersscript']['AffinityEvents'])[1]
assert pa[:len(ea)]==ea
si=masters.index('p865_SyntheticLove.esp');own='%02X'%len([1 for t,d in subs(load(sl)[0][3]) if t=='MAST'])
fix=lambda e:json.loads(json.dumps(e).replace('"'+own+'0026','"%02X0026'%si))
assert pa[len(ea):]==[fix(x) for x in sa[len(ea):]]
ei=masters.index('EFF.esp');assert pv['followersscript']['ExtensionHooks'][1][1].startswith('%02X'%ei)
print('OK: UCF Followers record + %d Synthetic Love affinity events; UCF hook in slot %02X'%(len(pa)-len(ea),ei))
