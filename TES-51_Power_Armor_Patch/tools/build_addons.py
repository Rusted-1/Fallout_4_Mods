"""Optional add-on plugins for the TES-51 FOMOD.

  fis   <base> <built TES51_Patch.esp> <out>   FIS / FallUI: puts the "[PowerArmor]" tag at the
                                              front of every TES-51 piece name via its naming rule.
  liningc <base> <out>                         Torso Lining C health 60 -> 120 (original mod bug).
"""
import struct, sys
sys.path.insert(0, '/home/claude/tools')
from esp import subrecs, records
from build_tiers import sr, z, rec, grup, by_edid, serialize_innr

def plugin(masters, author_desc, groups, next_id=0x800):
    hedr = struct.pack('<fiI', 1.0, sum(len(r) for _, r in groups), next_id)
    body = sr('HEDR', hedr) + sr('CNAM', z('patch')) + sr('SNAM', z(author_desc))
    for m in masters:
        body += sr('MAST', z(m)) + sr('DATA', b'\0' * 8)
    body += sr('INTV', struct.pack('<I', 1))
    tes4 = b'TES4' + struct.pack('<IIIIHH', len(body), 0x200, 0, 0, 0x83, 0) + body   # ESL-flagged
    return tes4 + b''.join(grup(lab, b''.join(rs)) for lab, rs in groups)

def split_innr(body):
    head = []; rulesets = []; cur = None
    for a, x in subrecs(body):
        if a == 'VNAM': cur = []; rulesets.append(cur); continue
        if cur is None: head.append((a, x)); continue
        if a == 'WNAM': cur.append([(a, x)])
        else: cur[-1].append((a, x))
    return head, rulesets

def fis(base_path, patch_path, out_path):
    base_name = base_path.replace('\\', '/').split('/')[-1]
    innr = by_edid(patch_path)['dn_PowerArmor_TES51_INNR']
    head, rulesets = split_innr(innr[2])
    # FIS static-sorting convention (same as its dn_PowerArmor override): an unconditional
    # tag entry in a ruleset placed first, so the tag ends up at the very start of the name.
    tag = [[('WNAM', z('[PowerArmor]'))]]
    if rulesets and rulesets[-1] == []:
        rulesets = rulesets[:-1]          # keep the ruleset count unchanged (drop one empty slot)
    rulesets = [tag] + rulesets
    r = rec('INNR', innr[1], serialize_innr(head, rulesets))
    open(out_path, 'wb').write(plugin(['Fallout4.esm', base_name, 'TES51_Patch.esp'],
                                      'TES-51 FIS / FallUI power armor tags', [('INNR', [r])]))

def liningc(base_path, out_path):
    base_name = base_path.replace('\\', '/').split('/')[-1]
    t, fid, d = by_edid(base_path)['PA_TES51_Torso_Lining_C']
    out = b''
    for a, x in subrecs(d):
        if a == 'DATA':
            x = bytearray(x); pc = struct.unpack_from('<I', x, 4)[0]; o = 28; hit = 0
            for i in range(pc):
                if x[o] == 0 and x[o+4] == 2 and struct.unpack_from('<H', x, o+8)[0] == 11:
                    assert struct.unpack_from('<i', x, o+12)[0] == 60
                    struct.pack_into('<i', x, o+12, 120); hit += 1
                o += 24
            assert hit == 1; x = bytes(x)
        out += sr(a, x)
    r = rec('OMOD', fid, out)
    open(out_path, 'wb').write(plugin(['Fallout4.esm', base_name],
                                      'TES-51 Torso Lining C health fix (60 -> 120)', [('OMOD', [r])]))

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'fis': fis(*sys.argv[2:5])
    elif cmd == 'liningc': liningc(*sys.argv[2:4])
