"""Minimal reader for Fallout 4 plugin files (.esm / .esp / .esl).

Enough of the format to walk records and subrecords without the Creation Kit
or xEdit: the 24-byte record header, nested GRUP structures, zlib-compressed
record payloads, and the subrecord stream inside each record.

Used by build_patch.py and verify.py. Import it, or run it directly to dump a
plugin's structure:

    python3 -I tools/esp.py <plugin.esp>
"""

import struct
import sys
import zlib

COMPRESSED = 0x00040000  # record flag: payload is zlib-compressed
HDR = 24                 # record and GRUP header length


def read_subrecords(data):
    """Split a record payload into [(type, bytes), ...]."""
    subs = []
    i = 0
    n = len(data)
    while i < n:
        if i + 6 > n:
            break
        stype = data[i:i + 4].decode('ascii', errors='replace')
        ssize = struct.unpack('<H', data[i + 4:i + 6])[0]
        subs.append((stype, data[i + 6:i + 6 + ssize]))
        i += 6 + ssize
    return subs


def parse_plugin(path):
    """Walk a plugin and return a flat list of entries.

    Records are ('TYPE', depth, formid, flags, payload) with the payload
    already decompressed. GRUPs are ('GRUP', depth, label, grouptype, size).
    """
    with open(path, 'rb') as f:
        content = f.read()

    records = []

    def parse_group(i, end, depth):
        while i < end:
            rtype = content[i:i + 4].decode('ascii', errors='replace')
            if rtype == 'GRUP':
                gsize = struct.unpack('<I', content[i + 4:i + 8])[0]
                label = content[i + 8:i + 12]
                gtype = struct.unpack('<i', content[i + 12:i + 16])[0]
                records.append(('GRUP', depth, label, gtype, gsize))
                parse_group(i + HDR, i + gsize, depth + 1)
                i += gsize
            else:
                dsize = struct.unpack('<I', content[i + 4:i + 8])[0]
                flags = struct.unpack('<I', content[i + 8:i + 12])[0]
                formid = struct.unpack('<I', content[i + 12:i + 16])[0]
                rdata = content[i + HDR:i + HDR + dsize]
                if flags & COMPRESSED:
                    rdata = zlib.decompress(rdata[4:])
                records.append((rtype, depth, formid, flags, rdata))
                i += HDR + dsize
        return i

    # The TES4 header record comes first, outside any GRUP.
    dsize = struct.unpack('<I', content[4:8])[0]
    flags = struct.unpack('<I', content[8:12])[0]
    formid = struct.unpack('<I', content[12:16])[0]
    records.append((content[0:4].decode('ascii'), 0, formid, flags,
                    content[HDR:HDR + dsize]))

    parse_group(HDR + dsize, len(content), 0)
    return records


def editor_id(payload):
    for stype, sdata in read_subrecords(payload):
        if stype == 'EDID':
            return sdata.split(b'\x00')[0].decode('utf-8', errors='replace')
    return ''


def main(path):
    records = parse_plugin(path)
    print(f'Total entries: {len(records)}')
    for rec in records:
        if rec[0] == 'GRUP':
            _, depth, label, gtype, gsize = rec
            print('  ' * depth + f'GRUP label={label} type={gtype} size={gsize}')
        else:
            rtype, depth, formid, flags, rdata = rec
            print('  ' * depth + f'{rtype} formid={formid:08X} flags={flags:08X} '
                                 f'size={len(rdata)} EDID={editor_id(rdata)}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('usage: esp.py <plugin.esp>')
    main(sys.argv[1])
