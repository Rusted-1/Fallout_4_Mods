"""Tiny structured assembler for Fallout 4 Papyrus bytecode, checked against vanilla signatures (sigs.json)."""
import json,os
HERE=os.path.dirname(os.path.abspath(__file__))
SIGS=json.load(open(os.path.join(HERE,'sigs.json')))
I=lambda s:('id',s)
S=lambda s:('str',s)
def lookup(cls,method):
    c=cls.lower()
    while c:
        info=SIGS.get(c)
        if info is None: raise KeyError('no signatures for class %r'%c)
        f=info['fns'].get(method.lower())
        if f: return c,f
        c=info['parent']
    raise KeyError('%s.%s not found'%(cls,method))
class Func:
    def __init__(s,script,name,params=(),ret='None'):
        s.sc=script;s.name=name;s.params=list(params);s.rtype=ret;s.locals=[];s.code=[];s.labels={};s.n=0
        s.types={n:t for n,t in params}
    def tmp(s,t):
        n='::temp%d'%s.n;s.n+=1;s.locals.append((n,t));s.types[n]=t;return n
    def local(s,n,t): s.locals.append((n,t));s.types[n]=t;return n
    def none(s):
        if '::nonevar' not in s.types: s.local('::nonevar','None')
        return '::nonevar'
    def typeof(s,x):
        if x=='self': return s.sc.name
        if x in s.types: return s.types[x]
        if x in s.sc.vartypes: return s.sc.vartypes[x]
        raise KeyError('unknown variable '+x)
    def arg(s,a):
        if isinstance(a,str): return I(a)
        if isinstance(a,tuple): return a
        return a                               # int/float/bool/None literal
    def op(s,name,*args): s.code.append((name,[s.arg(a) for a in args]))
    def call(s,obj,method,*args):
        """obj.method(args) -> returns dest var name (or ::nonevar)."""
        cls,f=lookup(s.typeof(obj),method)
        assert len(args)==len(f['params']),'%s.%s takes %d args, got %d'%(cls,method,len(f['params']),len(args))
        dest=s.none() if f['ret'] in('None','') else s.tmp(f['ret'])
        s.code.append(('callmethod',[I(f['name']),I(obj),I(dest)]+[s.arg(a) for a in args]));return dest
    def callstatic(s,cls,method,*args):
        c,f=lookup(cls,method);assert f['global']
        assert len(args)==len(f['params'])
        dest=s.none() if f['ret'] in('None','') else s.tmp(f['ret'])
        s.code.append(('callstatic',[I(cls),I(f['name']),I(dest)]+[s.arg(a) for a in args]));return dest
    def callself(s,fname,*args):
        f=s.sc.funcs[fname];assert len(args)==len(f.params)
        dest=s.none() if f.rtype=='None' else s.tmp(f.rtype)
        s.code.append(('callmethod',[I(fname),I('self'),I(dest)]+[s.arg(a) for a in args]));return dest
    def cast(s,x,t): d=s.tmp(t);s.op('cast',d,x);return d
    def cmp(s,o,a,b): d=s.tmp('Bool');s.op(o,d,a,b);return d
    def label(s,n): s.labels[n]=len(s.code)
    def jmpf(s,cond,lab): s.code.append(('jmpf',[I(cond),('lab',lab)]))
    def jmpt(s,cond,lab): s.code.append(('jmpt',[I(cond),('lab',lab)]))
    def jmp(s,lab): s.code.append(('jmp',[('lab',lab)]))
    def ret(s,v=None): s.code.append(('return',[s.arg(v)]))
    def build(s):
        code=[]
        for i,(o,a) in enumerate(s.code):
            a=[(s.labels[x[1]]-i) if isinstance(x,tuple) and x[0]=='lab' else x for x in a];code.append((o,a))
        if any(l==len(s.code) for l in s.labels.values()): code.append(('nop',[]))
        return {'ret':s.rtype,'doc':'','uflags':0,'flags':0,'params':s.params,'locals':s.locals,'code':code}
class Script:
    def __init__(s,name,parent,doc=''):
        s.name=name;s.parent=parent;s.doc=doc;s.props=[];s.vartypes={};s.funcs={};s.order=[];s.vars=[]
        SIGS.setdefault(name.lower(),{'parent':parent.lower(),'fns':{},'props':{}})
    def prop(s,name,t):
        s.props.append((name,t));s.vartypes['::%s_var'%name]=t;return '::%s_var'%name
    def var(s,name,t,init=None): s.vars.append((name,t,init));s.vartypes[name]=t;return name
    def func(s,name,params=(),ret='None'):
        f=Func(s,name,params,ret);s.funcs[name]=f;s.order.append(name)
        SIGS[s.name.lower()]['fns'][name.lower()]={'name':name,'ret':ret,'params':list(params),'native':False,'global':False}
        return f
    def module(s):
        return {'src':s.name+'.psc','user':'Rusted-1','machine':'NoraAndNora','time':1792500000,
          'userflags':[('hidden',0),('conditional',1),('default',2),('collapsedonref',3),('collapsedonbase',4),('mandatory',5)],
          'objects':[{'name':s.name,'parent':s.parent,'doc':s.doc,'const':0,'uflags':0,'auto':'','structs':[],
            'vars':[('::%s_var'%n,t,0,None,1) for n,t in s.props]+[(n,t,0,v,0) for n,t,v in s.vars],
            'props':[{'name':n,'type':t,'doc':'','uflags':0,'flags':7,'auto':'::%s_var'%n} for n,t in s.props],
            'states':[('',[(n,s.funcs[n].build()) for n in s.order])]}]}
