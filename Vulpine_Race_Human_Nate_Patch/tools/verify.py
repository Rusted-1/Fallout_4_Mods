"""Check a built VulpineNateHuman.esp.

Asserts the things that actually matter for this patch:

  * the plugin holds exactly one record, the Player override
  * its RNAM points at vanilla HumanRace, not VulpineRace
  * the TES4 header is ESL-flagged and masters Fallout4.esm, VulpineRace.esm
    and VulpinePlayer.esp, in that order
  * no MQ101PlayerSpouse record was dragged along

If the source plugin is given as a second argument, it also diffs the Player
record against it subrecord by subrecord and asserts that RNAM is the only
field that differs.

    python3 -I tools/verify.py <VulpineNateHuman.esp> [VulpinePlayer.esp]
"""

import os
import struct
import sys

# python3 -I drops the script's own directory from sys.path, so put it back.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from esp import parse_plugin, read_subrecords, editor_id

HUMAN_RACE = 0x00013746
VULPINE_RACE = 0x01000F99
PLAYER_FORMID = 0x00000007
ESL_FLAG = 0x00000200
EXPECTED_MASTERS = ['Fallout4.esm', 'VulpineRace.esm', 'VulpinePlayer.esp']

failures = []


def check(ok, label, detail=''):
    print(f'  [{"ok" if ok else "FAIL"}] {label}' + (f' - {detail}' if detail else ''))
    if not ok:
        failures.append(label)


def u32(data):
    return struct.unpack('<I', data)[0]


def find_player(records):
    for rec in records:
        if rec[0] == 'NPC_' and rec[2] == PLAYER_FORMID:
            return rec[4]
    return None


def main(patch_path, source_path=None):
    records = parse_plugin(patch_path)
    tes4 = next(r for r in records if r[0] == 'TES4')
    npcs = [r for r in records if r[0] == 'NPC_']

    print(f'{patch_path}')

    check(tes4[3] & ESL_FLAG == ESL_FLAG, 'TES4 is ESL-flagged',
          f'flags={tes4[3]:08X}')

    masters = [sd.split(b'\x00')[0].decode() for st, sd
               in read_subrecords(tes4[4]) if st == 'MAST']
    check(masters == EXPECTED_MASTERS, 'masters are correct and in order',
          ', '.join(masters))

    check(len(npcs) == 1, 'exactly one record in the plugin',
          f'{len(npcs)} NPC_ record(s)')

    spouses = [editor_id(r[4]) for r in npcs
               if editor_id(r[4]).startswith('MQ101PlayerSpouse')]
    check(not spouses, 'no spouse record included', ', '.join(spouses))

    payload = find_player(records)
    check(payload is not None, 'Player record (00000007) present')
    if payload is None:
        return finish()

    subs = dict(read_subrecords(payload))
    check('RNAM' in subs and u32(subs['RNAM']) == HUMAN_RACE,
          'RNAM is vanilla HumanRace',
          f'{u32(subs["RNAM"]):08X}' if 'RNAM' in subs else 'missing')
    check('RNAM' not in subs or u32(subs['RNAM']) != VULPINE_RACE,
          'RNAM is not VulpineRace')

    if source_path:
        print(f'\ndiff against {source_path}')
        src_payload = find_player(parse_plugin(source_path))
        if src_payload is None:
            check(False, 'Player record found in source plugin')
            return finish()

        src = read_subrecords(src_payload)
        new = read_subrecords(payload)
        check([s[0] for s in src] == [s[0] for s in new],
              'subrecord set and order unchanged')

        differing = [a[0] for a, b in zip(src, new) if a[1] != b[1]]
        check(differing == ['RNAM'], 'RNAM is the only field that differs',
              ', '.join(differing) if differing else 'nothing differs')

    finish()


def finish():
    print()
    if failures:
        print(f'{len(failures)} check(s) FAILED: ' + '; '.join(failures))
        sys.exit(1)
    print('All checks passed.')


if __name__ == '__main__':
    if len(sys.argv) not in (2, 3):
        sys.exit('usage: verify.py <VulpineNateHuman.esp> [VulpinePlayer.esp]')
    main(*sys.argv[1:])
