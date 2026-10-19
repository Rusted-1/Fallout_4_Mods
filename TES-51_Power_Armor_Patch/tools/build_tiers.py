"""Add the eight new TES-51 armor tiers (Iron -> Daedric) to an existing TES51_Patch.esp.

usage: python3 -I build_tiers.py <base plugin> <existing patch> <out patch>

Every new record is cloned from the base mod's Lining F records for that piece
type, so filter keywords, attach point, loose-mod model and recipe layout are
the mod's own.  Stats are Lining F + the tier's bonus (the user's draft).
"""
import struct, sys
sys.path.insert(0, '/home/claude/tools')
from esp import subrecs, records

# ---------------------------------------------------------------- design data
PERK = dict(Science1=0x264D9, Science2=0x264DA, Armorer4=0x1797EA, Scrapper1=0x65E65, Scrapper2=0x1D2483,
            Medic1=0x4C926, Blacksmith1=0x4B253, Blacksmith2=0x4B26A, Blacksmith3=0x264D8,
            Chemist1=0xE36FF, NuclearPhysicist3=0x1D2471)
DT_ENERGY, DT_RAD = 0x60A81, 0x60A85
F_DR, F_ER, F_HP_LIMB, F_HP_TORSO = 100, 100, 75, 300   # Lining F (read from the base mod)
F_MULT = 0.25

# name, ruleset prefix, +DR, +ER, +Rad, +HP(limb; torso x4), perks, description
TIERS = [
 ("Iron Reinforcement", "Iron", 20, 5, 0, 15, ["Armorer4", "Scrapper1"],
  "Using some iron you have scrounged up, you're able to reinforce some of the thinner parts of the metal that have been bothering you."),
 ("Steel Reinforcement", "Steel", 40, 20, 5, 25, ["Armorer4", "Scrapper2"],
  "Using old bars of steel, you added further improvements to the weak parts of the armor."),
 ("Bonemold", "Bonemold", 50, 25, 10, 30, ["Armorer4", "Scrapper2", "Medic1"],
  "After experimenting with bones of the various mammals of the post-war, you find that it is actually better than the steel you have been using."),
 ("Dwarven", "Dwarven", 70, 40, 25, 45, ["Armorer4", "Scrapper2", "Blacksmith1"],
  "This odd metal washed up on the beach. After some experimentation, it is found to be super useful for your armor."),
 ("Orcish", "Orcish", 75, 50, 20, 55, ["Armorer4", "Scrapper2", "Blacksmith2"],
  "This odd metal was recovered from a Super Mutant camp. It is ugly, yet very, very sturdy."),
 ("Ebony", "Ebony", 85, 60, 35, 105, ["Armorer4", "Scrapper2", "Blacksmith3"],
  "This beautiful-looking material was discovered in the Glowing Sea by the original detonation site. Its sheer strength and durability are amazing."),
 ("Dragonplate", "Dragonplate", 90, 65, 45, 120, ["Science2", "Armorer4", "Scrapper2", "Blacksmith3", "Chemist1"],
  "An odd type of bone was found after a bunch of raiders blew up an old burial site to find some chems. It's old, very, very old. Yet somehow familiar, and strong."),
 ("Daedric", "Daedric", 105, 80, 75, 200, ["Science2", "Armorer4", "Blacksmith3", "NuclearPhysicist3"],
  "You found the bars in your room. You don't know how they got there. There is an ominous feeling about it, but its strength, oh, the strength."),
]
PIECES = ["Arm", "Helmet", "Leg", "Torso"]
PIECE_WORD = dict(Arm="Arm", Helmet="Helmet", Leg="Leg", Torso="Torso")
EXTRA_COMPONENTS = 5
FIRST_NEW_ID = 0x800

# ---------------------------------------------------------------- byte helpers
def sr(t, data):
    return t.encode() + struct.pack('<H', len(data)) + data
def z(s):
    return s.encode('cp1252') + b'\0'
def rec(t, fid, body, flags=0):
    return t.encode() + struct.pack('<IIIIHH', len(body), flags, fid, 0, 0x83, 0) + body
def grup(label, payload):
    return b'GRUP' + struct.pack('<I', 24 + len(payload)) + label.encode() + struct.pack('<IIHH', 0, 0, 0x83, 0) + payload

def raw_records(buf, off, end):
    """yield (type, fid, raw bytes) for the direct records of a top-level group."""
    while off < end:
        t = buf[off:off+4].decode('latin1'); sz = struct.unpack_from('<I', buf, off+4)[0]
        if t == 'GRUP':
            yield 'GRUP', None, buf[off:off+sz]; off += sz; continue
        fid = struct.unpack_from('<I', buf, off+12)[0]
        yield t, fid, buf[off:off+24+sz]; off += 24 + sz

def read_plugin(path):
    buf = open(path, 'rb').read()
    hsz = struct.unpack_from('<I', buf, 4)[0]
    header = buf[:24+hsz]
    groups = {}; order = []
    off = 24 + hsz
    while off < len(buf):
        sz = struct.unpack_from('<I', buf, off+4)[0]; lab = buf[off+8:off+12].decode()
        groups[lab] = buf[off+24:off+sz]; order.append(lab); off += sz
    return header, groups, order

def by_edid(path):
    out = {}
    for t, fid, fl, d in records(open(path, 'rb').read()):
        for a, x in subrecs(d):
            if a == 'EDID':
                out[x[:-1].decode('latin1')] = (t, fid, d); break
    return out

# ---------------------------------------------------------------- OMOD props
def prop(vtype, func, pid, v1, v2=b'\0\0\0\0'):
    return struct.pack('<B3xB3xH2x', vtype, func, pid) + v1 + v2 + b'\0\0\0\0'

def omod_data(template_data, tier_kw, dr, er, rad, hp, mult):
    head = bytearray(template_data[:28])
    props = [
        prop(1, 1, 4, struct.pack('<f', mult)),              # weight  MUL+ADD
        prop(1, 1, 5, struct.pack('<f', mult)),              # value   MUL+ADD
        prop(0, 2, 11, struct.pack('<i', hp)),               # health  ADD
        prop(0, 2, 6, struct.pack('<i', dr)),                # damage resistance ADD
        prop(4, 2, 3, struct.pack('<I', tier_kw), struct.pack('<I', 0x1FD)),  # keyword ADD
        prop(6, 2, 9, struct.pack('<I', DT_ENERGY), struct.pack('<f', er)),  # energy res ADD
    ]
    if rad:
        props.append(prop(6, 2, 9, struct.pack('<I', DT_RAD), struct.pack('<f', rad)))
    struct.pack_into('<I', head, 4, len(props))
    return bytes(head) + b''.join(props)

# ---------------------------------------------------------------- build
def build(base_path, patch_path, out_path, innr_source_path):
    base = by_edid(base_path)
    header, groups, order = read_plugin(patch_path)
    base_idx = 0x01000000; own = 0x02000000
    def bfid(edid):  # base record formid as seen from the patch (master index 01)
        return (base[edid][1] & 0x00FFFFFF) | base_idx

    next_id = FIRST_NEW_ID
    def alloc():
        nonlocal next_id
        fid = own | next_id; next_id += 1; return fid

    new = {k: [] for k in ('KYWD', 'MISC', 'COBJ', 'OMOD')}
    innr_entries = []
    summary = []
    for name, short, dDR, dER, dRad, dHP, perks, desc in TIERS:
        ti = TIERS.index(next(t for t in TIERS if t[0] == name))
        mult = round(F_MULT + 0.05 * (ti + 1), 2)
        kw = alloc(); kw_edid = f"dn_PowerArmor_TES51_Tier_{short}"
        new['KYWD'].append(rec('KYWD', kw, sr('EDID', z(kw_edid)) + sr('CNAM', b'\0\0\0\0')))
        innr_entries.append((f"{short} TES-51", [kw, bfid('dn_PowerArmor_TES51')]))
        for piece in PIECES:
            t_omod = dict(subrecs(base[f"PA_TES51_{piece}_Lining_F"][2]))
            t_misc_fid = struct.unpack('<I', t_omod['LNAM'])[0]
            t_misc = next(v for v in base.values() if v[1] == t_misc_fid)
            t_cobj = list(subrecs(base[f"co_PA_TES51_{piece}_Lining_F"][2]))
            omod_fid, misc_fid, cobj_fid = alloc(), alloc(), alloc()
            hp = dHP * 4 if piece == 'Torso' else dHP
            hp_total = (F_HP_TORSO if piece == 'Torso' else F_HP_LIMB) + hp
            ed = f"PA_TES51_{piece}_Tier_{short}"
            # OMOD
            label = f"Model {'GHIJKLMN'[ti]}: {name}"   # workbench sorts by name; continue A-F
            body = sr('EDID', z(ed)) + sr('FULL', z(label)) + sr('DESC', z(desc))
            body += sr('DATA', omod_data(t_omod['DATA'], kw, F_DR + dDR, F_ER + dER, dRad, hp_total, mult))
            body += sr('MNAM', t_omod['MNAM'])          # same filter keywords as Lining F
            body += sr('LNAM', struct.pack('<I', misc_fid))
            new['OMOD'].append(rec('OMOD', omod_fid, body))
            # loose mod
            mb = b''
            for a, x in subrecs(t_misc[2]):
                if a == 'EDID': x = z(f"pa_comp_TES51_{piece}_Tier_{short}")
                elif a == 'FULL': x = z(f"TES-51 {short} {PIECE_WORD[piece]} Lining")
                mb += sr(a, x)
            new['MISC'].append(rec('MISC', misc_fid, mb))
            # recipe
            cb = b''
            for a, x in t_cobj:
                if a == 'EDID': x = z(f"co_PA_TES51_{piece}_Tier_{short}")
                elif a == 'FVPA':
                    comps = [struct.unpack_from('<II', x, i) for i in range(0, len(x), 8)]
                    x = b''.join(struct.pack('<II', c, n + EXTRA_COMPONENTS) for c, n in comps)
                elif a == 'CTDA':
                    continue  # rebuilt below
                elif a == 'CNAM':
                    x = struct.pack('<I', omod_fid)
                if a == 'CNAM':
                    tmpl = next(x2 for a2, x2 in t_cobj if a2 == 'CTDA')
                    for p in ([] if any(x.startswith('Science') for x in perks) else ['Science1']) + perks:
                        c = bytearray(tmpl); struct.pack_into('<I', c, 12, PERK[p]); cb += sr('CTDA', bytes(c))
                cb += sr(a, x)
            new['COBJ'].append(rec('COBJ', cobj_fid, cb))
            summary.append((short, piece, F_DR + dDR, F_ER + dER, dRad, hp_total, perks))

    # ---- naming rule: original (or patched) TES-51 INNR + tier names before the plain "TES-51" fallback
    innr_rec = by_edid(innr_source_path)['dn_PowerArmor_TES51_INNR']
    innr_fid = (innr_rec[1] & 0x00FFFFFF) | base_idx
    innr_body = rebuild_innr(innr_rec[2], innr_entries)
    new['INNR'] = [rec('INNR', innr_fid, innr_body)]

    # ---- assemble
    canon = ['KYWD', 'COBJ', 'LCTN', 'MISC', 'OMOD', 'INNR', 'WRLD']
    out_groups = []
    added = 0
    for lab in canon:
        payload = groups.get(lab, b'')
        if lab == 'INNR':
            # replace any existing INNR override of the same record
            kept = b''.join(r for t, fid, r in raw_records(payload, 0, len(payload)) if fid != innr_fid)
            payload = kept + new['INNR'][0]
        elif lab in new:
            payload += b''.join(new[lab])
        if payload:
            out_groups.append(grup(lab, payload))
    for lab in order:
        assert lab in canon, lab

    h = bytearray(header)
    # HEDR: version 1.0, record count, next object id
    hdr_off = 24
    assert h[hdr_off:hdr_off+4] == b'HEDR'
    body_bytes = b''.join(out_groups)
    cnt = sum(1 for _ in records(body_bytes))
    struct.pack_into('<fiI', h, hdr_off+6, 1.0, cnt, next_id)
    out = bytes(h) + body_bytes
    open(out_path, 'wb').write(out)
    return summary


def rebuild_innr(body, tier_entries):
    """Insert tier names into the ruleset that holds 'TES-51b'..'TES-51', and write
    correct VNAM counts for every ruleset."""
    subs = list(subrecs(body))
    head = []; rulesets = []; cur = None
    for a, x in subs:
        if a == 'VNAM':
            cur = []; rulesets.append(cur); continue
        if cur is None: head.append((a, x)); continue
        if a == 'WNAM': cur.append([(a, x)])
        else: cur[-1].append((a, x))
    for rs in rulesets:
        names = [e[0][1][:-1].decode('cp1252') for e in rs]
        if 'TES-51f' in names:
            pos = names.index('TES-51')
            ynam = next(x for a, x in rs[pos] if a == 'YNAM')
            ins = []
            for label, kws in tier_entries:
                ins.append([('WNAM', z(label)), ('KSIZ', struct.pack('<I', len(kws))),
                            ('KWDA', b''.join(struct.pack('<I', k) for k in kws)), ('YNAM', ynam)])
            rs[pos:pos] = ins
            break
    else:
        raise SystemExit('TES-51 tier ruleset not found')
    return serialize_innr(head, rulesets)


def serialize_innr(head, rulesets):
    out = b''.join(sr(a, x) for a, x in head)
    for rs in rulesets:
        out += sr('VNAM', struct.pack('<I', len(rs)))
        for e in rs:
            out += b''.join(sr(a, x) for a, x in e)
    return out


if __name__ == '__main__':
    base, patch, out = sys.argv[1:4]
    innr_src = sys.argv[4] if len(sys.argv) > 4 else base
    s = build(base, patch, out, innr_src)
    for row in s: print(row)
