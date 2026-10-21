import sys,html,os
sys.path.insert(0,'.')
from scenes_lib import parse_script
O='/tmp/claude-0/-home-claude/be2bc821-49d7-5d69-a391-575a1c62ced3/scratchpad/out'
L,C=parse_script(O+'/phase1-script.md')
import csv
V={r['Line ID']:r['File name'] for r in csv.DictReader(open(O+'/Phase 1 voice sheet.csv',encoding='utf-8-sig'))}
e=html.escape
WHO={'SYNTH':('Synth Nora','syn'),'NORA':('Nora','nor'),'NATE':('Nate','nat')}
def line(lid,note=''):
    l=L[lid];who,cls=WHO[l['speaker']]
    f=V.get(lid,'');fid=f'<span class="fid">{f[:8]}</span>' if f else '<span class="fid">text only</span>'
    return f'<li class="ln {cls}"><span class="who">{who}</span><span class="txt">{e(l["text"])}</span><span class="meta">{e(l["delivery"])} · {fid}{(" · "+e(note)) if note else ""}</span></li>'
def choices(ids,outs=None,resp=None):
    outs=outs or {};resp=resp or {}
    rows=''
    for cid in ids:
        c=C[cid];o=outs.get(cid,'');r=resp.get(cid)
        rr=f'<div class="resp">→ {WHO[L[r]["speaker"]][0]}: “{e(L[r]["text"])}”</div>' if r else ''
        rows+=f'<li class="ch"><span class="btn b{c["button"]}">{c["button"]}</span><div><b>{e(c["label"])}</b><span class="full">“{e(c["line"])}”</span>{rr}{f"<span class=out>{e(o)}</span>" if o else ""}</div></li>'
    return f'<li class="choice"><div class="clabel">Nate chooses</div><ul>{rows}</ul></li>'
def branch(title,cond,items): return f'<li class="branch"><div class="blabel"><b>{e(title)}</b> <span>{e(cond)}</span></div><ol>{"".join(items)}</ol></li>'
seq=lambda ids:[line(i) for i in ids]

s1=(seq(['P1-S1-001','P1-S1-002','P1-S1-003'])+[
 branch('Real Nora is with you','scene path 1A',[choices(['P1-S1-010','P1-S1-011','P1-S1-012','P1-S1-013'],resp={'P1-S1-010':'P1-S1-020','P1-S1-011':'P1-S1-021','P1-S1-012':'P1-S1-022','P1-S1-013':'P1-S1-023'})]
   +seq(['P1-S1-030','P1-S1-031','P1-S1-032','P1-S1-033','P1-S1-034','P1-S1-035','P1-S1-036','P1-S1-037','P1-S1-038'])
   +[choices(['P1-S1-040','P1-S1-041','P1-S1-042','P1-S1-043'],resp={'P1-S1-040':'P1-S1-050','P1-S1-041':'P1-S1-051','P1-S1-042':'P1-S1-052','P1-S1-043':'P1-S1-053'})]
   +seq(['P1-S1-060','P1-S1-061','P1-S1-062'])
   +[choices(['P1-S1-070','P1-S1-071','P1-S1-072','P1-S1-073'],resp={'P1-S1-070':'P1-S1-075','P1-S1-071':'P1-S1-075','P1-S1-072':'P1-S1-075','P1-S1-073':'P1-S1-074'})]
   +[line('P1-S1-076','ends the meeting: Synthetic Love recruits her, objective "Travel with Nora to Vault 111"')]),
 branch('Real Nora is not with you','scene path 1B',seq(['P1-S1B-001','P1-S1B-002','P1-S1B-003'])+[line('P1-S1B-004','she joins; the confrontation waits for scene 1C')])])
s1c=seq(['P1-S1C-001','P1-S1C-002'])+[f'<li class="note">Then the confrontation from “Get away from him.” to “It walks in front of me.”, exactly as in path 1A.</li>']
road=seq(['P1-AM-001','P1-AM-002','P1-AM-003','P1-AM-004','P1-AM-005','P1-AM-010','P1-AM-011','P1-AM-012','P1-AM-013','P1-AM-014','P1-AM-020','P1-AM-021','P1-AM-022','P1-AM-023','P1-AM-024'])
ex=[branch('Exchange 1','',seq(['P1-AM-030','P1-AM-031','P1-AM-032'])),branch('Exchange 2','',seq(['P1-AM-040','P1-AM-041'])),branch('Exchange 3','',seq(['P1-AM-050','P1-AM-051','P1-AM-052','P1-AM-053']))]
s2=(seq(['P1-S2-001','P1-S2-002','P1-S2-003','P1-S2-004','P1-S2-005','P1-S2-006','P1-S2-007','P1-S2-008','P1-S2-009'])
 +[choices(['P1-S2-010','P1-S2-011','P1-S2-012','P1-S2-013'])]
 +seq(['P1-S2-020','P1-S2-021','P1-S2-022','P1-S2-030','P1-S2-031','P1-S2-032','P1-S2-033','P1-S2-034','P1-S3-001'])
 +[choices(['P1-S3-010','P1-S3-011','P1-S3-012','P1-S3-013'],outs={'P1-S3-010':'Choice 1','P1-S3-011':'Choice 2','P1-S3-012':'Choice 3','P1-S3-013':'Choice 4 → asks you to reconsider'})]
 +[branch('Choice 1 · Come with us','she stays a companion · NN_Phase1 100',seq(['P1-S3-020','P1-S3-021','P1-S3-022'])),
   branch('Choice 2 · I need time','she waits by her pod · NN_Phase1 200',seq(['P1-S3-030','P1-S3-031'])),
   branch('Choice 3 · Abomination','she turns hostile · NN_Phase1 300',seq(['P1-S3-040','P1-S3-041'])+[f'<li class="note">If you kill her and Nora is with you, scene SK plays:</li>']+seq(['P1-S3-045','P1-S3-046'])),
   branch('Choice 4 · Go your own way','pleads first',seq(['P1-S3-050','P1-S3-051'])+[f'<li class="note">The four choices come back. <b>Go your own way</b> becomes <b>“I’m sure.” / “I’m sorry. I’ve made up my mind.”</b> Any other pick switches to that choice.</li>']+seq(['P1-S3-060','P1-S3-061'])+[f'<li class="note">NN_Phase1 400: she waits 3 days in the vault, then leaves. The battle-site add-on can then place her last stand.</li>'])])
nt=seq(['P1-NT-001','P1-NT-002','P1-NT-003'])+[choices(['P1-NT-010','P1-NT-011','P1-NT-012','P1-NT-013'])]+[branch('If you asked “You okay?”','',seq(['P1-NT-020']))]

def scene(sid,name,trigger,items,tag=''):
    return f'''<section class="scene" id="{sid}"><header><div class="sid">{sid}</div><h2>{e(name)}</h2>{f'<span class="tag">{e(tag)}</span>' if tag else ''}</header>
<p class="trig"><b>Starts when</b> {trigger}</p><ol class="script">{"".join(items)}</ol></section>'''
body=''.join([
 scene('S1','Diamond City','synth Nora greets you (“Oh my God… Nate?”) after you have found the real Nora. The greeting runs at quest priority 90, so it wins over Synthetic Love’s own (71).',s1,'22 phases'),
 scene('S1C','First time together','you met synth Nora alone, and she comes within about 14 m of the real Nora.',s1c,'19 phases'),
 scene('Road','On the way to Vault 111','after the meeting, until you reach the cryo hall. Idle lines play at random. One exchange plays about once a game day while both Noras are with you.',road+ex,'15 idles · 3 exchanges'),
 scene('S2','Vault 111','synth Nora greets you in the cryo hall (Cold Comfort stage 30) and the real Nora is with you.',s2,'31 phases'),
 scene('NT','Reading “Nora’s Final Wish”','you read the note at the battle site and the real Nora is with you.',nt,'5 phases'),
])
mer='''flowchart LR
  A["Found the real Nora at Abernathy Farm"] --> B{"Synth Nora greets you: in Diamond City"}
  B -- "Nora with you" --> S1A["S1 · 1A: confrontation"]
  B -- "Nora not with you" --> S1B["S1 · 1B: she joins happily"]
  S1B --> S1C["S1C · first time together: panic, then confrontation"]
  S1A --> R["Road to Vault 111: idles + exchanges"]
  S1C --> R
  R --> S2["S2 · Vault 111: empty pod, breakdown"]
  S2 --> C{"The choice"}
  C --> O1["1 · Come with us: companion, tier 1"]
  C --> O2["2 · I need time: waits by her pod"]
  C --> O3["3 · Abomination: hostile"]
  C --> O4["4 · Go your own way: leaves after 3 days"]
  O2 -. "patience option: 7 days" .-> O4
  O3 --> SK["SK · That's that."]
  O4 --> BS["Battle site: (add-on)"]
  BS --> NT["NT · the note"]'''
page=f'''<title>Two Noras Phase 1</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
/* Layout: one reading column; each scene is a transcript with speaker colour bands, branches indented like a script binder. */
:root{{--bg:#eef0ec;--paper:#f8f9f6;--ink:#1d2621;--muted:#5d6a62;--rule:#cfd6cf;--syn:#1f6f74;--nor:#9a4a2b;--nat:#4b5560;--accent:#2f5d50;--chip:#e2e7e1;
--display:"Barlow Condensed","Arial Narrow",sans-serif;--body:"Source Serif 4",Georgia,serif;--mono:"JetBrains Mono",ui-monospace,Menlo,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#141a17;--paper:#1b221e;--ink:#e3e8e3;--muted:#9aa79f;--rule:#2f3a34;--syn:#5fb6bb;--nor:#e08a63;--nat:#a9b4bf;--accent:#7cc0a8;--chip:#26302b;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#141a17;--paper:#1b221e;--ink:#e3e8e3;--muted:#9aa79f;--rule:#2f3a34;--syn:#5fb6bb;--nor:#e08a63;--nat:#a9b4bf;--accent:#7cc0a8;--chip:#26302b;color-scheme:dark}}
body{{background:var(--bg);color:var(--ink);font:16px/1.55 var(--body)}}
.wrap{{max-width:900px;margin:0 auto;padding-block:32px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:28px}}
h1{{font:700 clamp(2.2rem,6vw,3.4rem)/1 var(--display);letter-spacing:.01em;margin:0;text-wrap:balance}}
.lede{{color:var(--muted);max-width:65ch;margin:.5rem 0 0}}
.kicker{{font:600 .8rem var(--display);letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}}
.legend{{display:flex;flex-wrap:wrap;gap:8px 16px;font:500 .85rem var(--mono);color:var(--muted)}}
.legend span::before{{content:"";display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:-1px;background:var(--c)}}
.flow{{background:var(--paper);border:1px solid var(--rule);border-radius:6px;padding:16px;overflow-x:auto}}
.flow pre{{margin:0;min-width:640px}}
nav{{display:flex;flex-wrap:wrap;gap:8px}}
nav a{{font:600 .95rem var(--display);letter-spacing:.06em;text-transform:uppercase;color:var(--ink);text-decoration:none;border:1px solid var(--rule);border-radius:3px;padding:4px 10px;background:var(--paper)}}
nav a:hover,nav a:focus-visible{{border-color:var(--accent);color:var(--accent);outline:none}}
.scene{{background:var(--paper);border:1px solid var(--rule);border-radius:6px;padding:20px 20px 12px}}
.scene header{{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 12px}}
.sid{{font:500 .8rem var(--mono);color:#fff;background:var(--accent);padding:2px 7px;border-radius:3px}}
:root:not([data-theme="light"]) .sid{{color:var(--bg)}}
h2{{font:600 1.7rem/1.1 var(--display);margin:0;letter-spacing:.01em}}
.tag{{font:400 .8rem var(--mono);color:var(--muted)}}
.trig{{margin:.6rem 0 1rem;color:var(--muted);max-width:70ch}} .trig b{{color:var(--ink)}}
ol,ul{{list-style:none;margin:0;padding:0}}
.script{{display:flex;flex-direction:column;gap:2px}}
.ln{{display:grid;grid-template-columns:7.5rem minmax(0,1fr);gap:2px 12px;padding:7px 0 7px 10px;border-left:3px solid var(--c)}}
.ln.syn{{--c:var(--syn)}} .ln.nor{{--c:var(--nor)}} .ln.nat{{--c:var(--nat)}}
.who{{font:600 .95rem var(--display);letter-spacing:.06em;text-transform:uppercase;color:var(--c);padding-top:2px}}
.txt{{min-width:0}}
.meta{{grid-column:2;font:400 .75rem/1.4 var(--mono);color:var(--muted)}}
.fid{{color:var(--ink);opacity:.75}}
.choice,.branch,.note{{margin:10px 0}}
.clabel,.blabel{{font:600 .85rem var(--display);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}}
.blabel b{{color:var(--ink);letter-spacing:.04em;font-size:1.05rem;text-transform:none}} .blabel span{{font-family:var(--mono);font-weight:400;letter-spacing:0;text-transform:none;font-size:.75rem}}
.choice ul{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,190px),1fr));gap:8px}}
.ch{{display:flex;gap:10px;background:var(--chip);border-radius:4px;padding:10px;min-width:0}}
.ch div{{min-width:0;display:flex;flex-direction:column;gap:3px}}
.ch .full{{font-size:.9rem;color:var(--muted)}} .resp{{font-size:.88rem}} .out{{font:500 .75rem var(--mono);color:var(--accent)}}
.btn{{flex:none;width:1.6rem;height:1.6rem;border-radius:50%;display:grid;place-items:center;font:600 .8rem var(--mono);color:#fff}}
.bY{{background:#b8901c}} .bB{{background:#a8352b}} .bX{{background:#2d5fa6}} .bA{{background:#3c8a4a}}
.branch{{border:1px dashed var(--rule);border-radius:4px;padding:10px 12px}}
.branch ol{{display:flex;flex-direction:column;gap:2px}}
.note{{font-size:.92rem;color:var(--muted);padding-left:13px;max-width:70ch}}
.foot{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:16px}}
.foot div{{background:var(--paper);border:1px solid var(--rule);border-radius:6px;padding:16px}}
.foot h3{{font:600 1.2rem var(--display);margin:0 0 6px;letter-spacing:.02em}}
.foot p,.foot li{{font-size:.93rem;margin:0}} .foot ul{{display:flex;flex-direction:column;gap:4px;list-style:disc;padding-left:1.1rem}}
code{{font:400 .85em var(--mono);background:var(--chip);padding:1px 4px;border-radius:3px}}
@media (max-width:560px){{.ln{{grid-template-columns:1fr}} .meta{{grid-column:1}}}}
</style>
<div class="wrap">
<div><div class="kicker">Nora and Nora · v0.5.0</div><h1>Two Noras, Phase 1</h1>
<p class="lede">How the first meeting, the road to Vault 111 and the choice at the empty pod now play in your game. Every line below is in the plugin, using the same file name you’re recording it under. Nate’s lines are text only.</p></div>
<div class="legend"><span style="--c:var(--syn)">Synth Nora</span><span style="--c:var(--nor)">Nora</span><span style="--c:var(--nat)">Nate</span><span style="--c:#b8901c">Y agree</span><span style="--c:#a8352b">B refuse</span><span style="--c:#2d5fa6">X sarcastic</span><span style="--c:#3c8a4a">A ask</span></div>
<div class="flow"><pre class="mermaid">{mer}</pre></div>
<nav><a href="#S1">Diamond City</a><a href="#S1C">First together</a><a href="#Road">Road</a><a href="#S2">Vault 111</a><a href="#NT">The note</a></nav>
{body}
<div class="foot">
<div><h3>Test it</h3><ul><li>Install <code>Nora and Nora 0.5.0.zip</code> over 0.4.0.</li><li>Use a save where you’ve found the real Nora but haven’t met synth Nora in Diamond City.</li><li>Lines are silent until your voice files are in. The subtitles still play.</li></ul></div>
<div><h3>Not in yet</h3><ul><li>Affinity reactions (likes and dislikes) on the choices.</li><li>Nate’s “How are you holding up?” questions in the companion menu.</li><li>Lip-sync, which comes with your recordings.</li></ul></div>
<div><h3>Known risk</h3><p>All of this was assembled without the Creation Kit and checked at the file level only: 8 scenes, 89 of 89 voiced lines placed, 0 reference problems. It hasn’t run in game yet.</p></div>
</div></div>'''
open(sys.argv[1],'w').write(page);print(len(page))
