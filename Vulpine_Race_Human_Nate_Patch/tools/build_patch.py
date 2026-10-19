"""Build VulpineNateHuman.esp.

Reads the Vulpine Race mod's own VulpinePlayer.esp, lifts its override of the
Player record (00000007) out byte for byte, rewrites only the 4-byte RNAM
(race) field from VulpineRace to vanilla HumanRace, and wraps the result in a
fresh ESL-flagged plugin.

Nothing else is copied: the two MQ101PlayerSpouse records stay untouched in the
original plugin, so Nora keeps her Vulpine race.

    python3 -I tools/build_patch.py <path to VulpinePlayer.esp> <out.esp>
"""

import os
import struct
import sys
import zlib

HUMAN_RACE = 0x00013746     # Fallout4.esm  HumanRace
PLAYER_FORMID = 0x00000007  # Fallout4.esm  Player
COMPRESSED = 0x00040000
ESL_FLAG = 0x00000200
HDR = 24

MASTERS = [b'Fallout4.esm', b'VulpineRace.esm', b'VulpinePlayer.esp']

AUTHOR = b'Claude patch\x00'
DESC = (b'Reverts the player character to HumanRace so Nate stays human. '
        b'Nora and all Vulpine records are untouched.\x00')


def iter_records(buf):
    """Yield (offset, type, datasize, flags, formid, header_tail, payload)."""
    i = 0
    n = len(buf)
    while i < n:
        rtype = buf[i:i + 4]
        if rtype == b'GRUP':
            i += HDR  # descend into the group
            continue
        dsize = struct.unpack('<I', buf[i + 4:i + 8])[0]
        flags = struct.unpack('<I', buf[i + 8:i + 12])[0]
        formid = struct.unpack('<I', buf[i + 12:i + 16])[0]
        yield (i, rtype, dsize, flags, formid, buf[i + 16:i + HDR],
               buf[i + HDR:i + HDR + dsize])
        i += HDR + dsize


def patch_rnam(payload, new_race):
    """Rewrite the RNAM subrecord, leaving every other subrecord byte-identical."""
    out = bytearray()
    i = 0
    found = False
    while i < len(payload):
        stype = payload[i:i + 4]
        ssize = struct.unpack('<H', payload[i + 4:i + 6])[0]
        sdata = payload[i + 6:i + 6 + ssize]
        if stype == b'RNAM' and ssize == 4:
            old = struct.unpack('<I', sdata)[0]
            print(f'  RNAM {old:08X} -> {new_race:08X}')
            sdata = struct.pack('<I', new_race)
            found = True
        out += stype + struct.pack('<H', len(sdata)) + sdata
        i += 6 + ssize
    if not found:
        sys.exit('RNAM not found in the Player record')
    return bytes(out)


def sub(tag, payload):
    return tag + struct.pack('<H', len(payload)) + payload


def build(src, out_path):
    data = open(src, 'rb').read()

    player = None
    for rec in iter_records(data):
        if rec[1] == b'NPC_' and rec[4] == PLAYER_FORMID:
            player = rec
            break
    if player is None:
        sys.exit(f'No Player record (00000007) in {src}')

    _, _, dsize, flags, _, hdr_tail, payload = player
    print(f'Found Player record: size={dsize} flags={flags:08X}')

    if flags & COMPRESSED:
        expected = struct.unpack('<I', payload[0:4])[0]
        payload = zlib.decompress(payload[4:])
        print(f'Decompressed: {len(payload)} bytes (expected {expected})')

    new_payload = patch_rnam(payload, HUMAN_RACE)

    # Rebuild the record uncompressed - functionally identical, easier to inspect.
    record = (b'NPC_' + struct.pack('<I', len(new_payload))
              + struct.pack('<I', flags & ~COMPRESSED)
              + struct.pack('<I', PLAYER_FORMID) + hdr_tail + new_payload)

    grup = (b'GRUP' + struct.pack('<I', HDR + len(record)) + b'NPC_'
            + struct.pack('<i', 0) + hdr_tail + record)

    tes4_payload = sub(b'HEDR', struct.pack('<fII', 1.0, 1, 0x00000800))
    tes4_payload += sub(b'CNAM', AUTHOR)
    tes4_payload += sub(b'SNAM', DESC)
    for m in MASTERS:
        tes4_payload += sub(b'MAST', m + b'\x00')
        tes4_payload += sub(b'DATA', struct.pack('<Q', 0))

    tes4 = (b'TES4' + struct.pack('<I', len(tes4_payload))
            + struct.pack('<I', ESL_FLAG) + struct.pack('<I', 0)
            + hdr_tail + tes4_payload)

    with open(out_path, 'wb') as f:
        f.write(tes4)
        f.write(grup)

    print(f'\nWrote {out_path} ({os.path.getsize(out_path)} bytes)')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('usage: build_patch.py <VulpinePlayer.esp> <out.esp>')
    build(sys.argv[1], sys.argv[2])
