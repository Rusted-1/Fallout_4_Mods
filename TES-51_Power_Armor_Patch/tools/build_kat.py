"""TES-51 patch for Kat's Power Armor Repair Kits (Nexus 53558).

usage: python3 -I build_kat.py <Some_Assembly_Required_Repair_Kits.esp> <TES-51 base plugin> <out .esp>

Same pattern as Kat's own per-armour add-ons (e.g. SAR_Repair_Kits_T65.esp):
  * new MISC  "TES-51 Repair Kit"      - clone of Kat's T-60 kit
  * new COBJ  kit recipe, chem station  - clone of Kat's T-60 kit recipe
  * the 7 TES-51 piece repair recipes  (co_Armor_Power_TES51_*) -> 1 kit, torso 2 kits
"""
import struct, sys
sys.path.insert(0, '/home/claude/tools')
from esp import subrecs
from build_tiers import sr, z, rec, by_edid
from build_addons import plugin

KAT_IDX, BASE_IDX, OWN = 0x01000000, 0x02000000, 0x03000000

def remap_kat(fid):  # Kat main has 1 master: its own records are 0x01 -> index 01 here too
    return fid

def main(kat_path, base_path, out_path):
    kat = by_edid(kat_path); base = by_edid(base_path)
    base_name = base_path.replace('\\', '/').split('/')[-1]
    kit_fid, cobj_fid = OWN | 0x800, OWN | 0x801

    misc = b''
    for a, x in subrecs(kat['kat_misc_t60repairkit'][2]):
        if a == 'EDID': x = z('kat_misc_tes51repairkit')
        elif a == 'FULL': x = z('TES-51 Repair Kit')
        misc += sr(a, x)

    cobj = b''
    for a, x in subrecs(kat['kat_co_misc_t60repairkit'][2]):
        if a == 'EDID': x = z('kat_co_misc_tes51repairkit')
        elif a == 'DESC': x = z('Repairs damaged TES-51 Power Armor.')
        elif a == 'CNAM': x = struct.pack('<I', kit_fid)
        cobj += sr(a, x)

    repairs = []
    for piece in ('ArmLeft', 'ArmRight', 'Helm', 'Helm2', 'LegLeft', 'LegRight', 'Torso'):
        t, fid, d = base[f'co_Armor_Power_TES51_{piece}']
        s = dict(subrecs(d)); assert 'BNAM' not in s   # repair recipe, not a crafting recipe
        body = b''
        for a, x in subrecs(d):
            if a == 'FVPA': x = struct.pack('<II', kit_fid, 2 if piece == 'Torso' else 1)
            elif a == 'CNAM':   # base's own record (index 01 in the base) -> index 02 here
                c = struct.unpack('<I', x)[0]; assert c >> 24 == 1
                x = struct.pack('<I', (c & 0xFFFFFF) | BASE_IDX)
            elif a not in ('EDID', 'DESC', 'INTV'):
                raise SystemExit(f'unhandled subrecord {a} in {piece}')
            body += sr(a, x)
        repairs.append(rec('COBJ', (fid & 0xFFFFFF) | BASE_IDX, body))

    data = plugin(['Fallout4.esm', 'Some_Assembly_Required_Repair_Kits.esp', base_name],
                  "TES-51 patch for Kat's Power Armor Repair Kits",
                  [('MISC', [rec('MISC', kit_fid, misc)]),
                   ('COBJ', [rec('COBJ', cobj_fid, cobj)] + repairs)], next_id=0x802)
    open(out_path, 'wb').write(data)

if __name__ == '__main__':
    main(*sys.argv[1:4])
