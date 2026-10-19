"""Brahmin's Endurance: replace +20 Carry Weight with health regeneration (5 HP every 3 s).

usage: python3 -I brahmin_regen.py <TES51_Patch.esp (Unique Legendaries build)>   (edits in place)

New ENCH  ench_TES51_Legendary_BrahminRegen, cloned from vanilla
ench_mod_LegendaryArmor_APRegen's layout, single effect = vanilla abRestoreHealth
(0x1504F1, constant value-modifier on Health, the effect vanilla uses for
MS09JackHealthRegen) at 5/3 HP per second.  Works in combat, unlike HealRate.
"""
import struct, sys
sys.path.insert(0, '/home/claude/tools')
from esp import subrecs, records
from build_tiers import sr, z, rec, grup, read_plugin, raw_records

RESTORE_HEALTH_MGEF = 0x001504F1
CARRY_WEIGHT_AV = 0x2DC
RATE = 5.0 / 3.0
NEW_DESC = ("Slowly regenerates health, 5 every 3 seconds. "
            "Damage and Energy Resistance increase as your health drops.")
TROPHIES = ("PA_TES51_Arm_Misc_TrophyL", "PA_TES51_Arm_Misc_TrophyR")

def edit_omod(raw, ench_fid):
    t = raw[:4]; flags, fid = struct.unpack_from('<II', raw, 8)
    body = raw[24:]
    assert not flags & 0x40000
    out = b''; edid = None
    for a, x in subrecs(body):
        if a == 'EDID': edid = x[:-1].decode()
        if a == 'DESC': x = z(NEW_DESC)
        if a == 'DATA':
            x = bytearray(x); pc = struct.unpack_from('<I', x, 4)[0]
            head, props = bytes(x[:28]), [bytes(x[28+24*i:52+24*i]) for i in range(pc)]
            assert len(x) == 28 + 24 * pc
            keep = []; removed = 0
            for p in props:
                vt, fn, pid = p[0], p[4], struct.unpack_from('<H', p, 8)[0]
                if pid == 10 and struct.unpack_from('<I', p, 12)[0] == CARRY_WEIGHT_AV:
                    removed += 1; continue
                keep.append(p)
            assert removed == 1, edid
            # Ench ADD, same layout as the trophy's existing enchantment properties
            tmpl = next(p for p in keep if struct.unpack_from('<H', p, 8)[0] == 0)
            new = bytearray(tmpl); struct.pack_into('<I', new, 12, ench_fid)
            keep.append(bytes(new))
            hb = bytearray(head); struct.pack_into('<I', hb, 4, len(keep))
            x = bytes(hb) + b''.join(keep)
        out += sr(a, x)
    return edid, raw[:4] + struct.pack('<I', len(out)) + raw[8:24] + out

def run(path):
    header, groups, order = read_plugin(path)
    hd = bytearray(header); ver, cnt, nxt = struct.unpack_from('<fiI', hd, 30)
    ench_fid = 0x02000000 | nxt
    ench_body = (sr('EDID', z('ench_TES51_Legendary_BrahminRegen')) + sr('OBND', b'\0' * 12) +
                 sr('ENIT', bytes.fromhex('000000000000000000000000000000000000000006000000000000000000000000000000')) +
                 sr('EFID', struct.pack('<I', RESTORE_HEALTH_MGEF)) +
                 sr('EFIT', struct.pack('<fII', RATE, 0, 0)))
    ench = rec('ENCH', ench_fid, ench_body)
    om = groups['OMOD']; new_om = b''; hit = []
    for t, fid, raw in raw_records(om, 0, len(om)):
        e = dict(subrecs(raw[24:])).get('EDID', b'')[:-1].decode()
        if e in TROPHIES:
            e2, raw = edit_omod(raw, ench_fid); hit.append(e2)
        new_om += raw
    assert sorted(hit) == sorted(TROPHIES), hit
    groups['OMOD'] = new_om
    groups['ENCH'] = groups.get('ENCH', b'') + ench
    canon = ['KYWD', 'ENCH', 'COBJ', 'LCTN', 'MISC', 'OMOD', 'INNR', 'WRLD']
    body = b''.join(grup(l, groups[l]) for l in canon if groups.get(l))
    n = sum(1 for _ in records(body))
    struct.pack_into('<fiI', hd, 30, 1.0, n, nxt + 1)
    open(path, 'wb').write(bytes(hd) + body)
    print(path.split('/')[-2], 'ench', hex(ench_fid), 'records', n)

if __name__ == '__main__':
    for p in sys.argv[1:]: run(p)
