"""Regenerate sigs.json (vanilla function signatures used by pexasm.py) from the vanilla scripts.
Usage: python3 -I gen_sigs.py <folder of extracted vanilla .pex (from Fallout4 - Misc.ba2)>"""
import sys,os,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import pex
WANT={'actor','objectreference','quest','form','scriptobject','globalvariable','game','utility','debug','actorbase','referencealias',
      'alias','scene','topicinfo','faction','companionactorscript','followersscript','book','message','weapon','armor','potion','furniture','formlist','rescript','retriggerscript','cell','location','keyword'}
db={}
for r,_,fs in os.walk(sys.argv[1]):
    for f in fs:
        n=f[:-4].lower()
        if n not in WANT: continue
        o=pex.load(os.path.join(r,f))['objects'][0];fns={}
        for sn,fl in o['states']:
            if sn: continue
            for fn,fo in fl: fns[fn.lower()]={'name':fn,'ret':fo['ret'],'params':fo['params'],'native':bool(fo['flags']&2),'global':bool(fo['flags']&1)}
        db[n]={'parent':o['parent'].lower(),'fns':fns,'props':{p['name'].lower():p['type'] for p in o['props']}}
json.dump(db,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'sigs.json'),'w'),indent=0);print(len(db),'classes')
