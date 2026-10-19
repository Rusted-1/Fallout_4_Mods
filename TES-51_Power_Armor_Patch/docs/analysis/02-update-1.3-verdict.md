# "Update 1.3" (Nexus file id 74489) — verdict

File: `Update 1.3-74489-1-3-1693867678\SkyrimInspiredPowerArmor.esp` — 169,533 bytes, ESP only, no assets.

## It is a byte-for-byte copy of the original 1.2 Update plugin

| File | Size | SHA-256 |
|---|---|---|
| 1.2 Update | 169,533 | `be7de7529130bfcb9e0864143b52f5b8b3ace39f522807d54f2c2a548face26c` |
| **"Update 1.3"** | **169,533** | **`be7de7529130bfcb9e0864143b52f5b8b3ace39f522807d54f2c2a548face26c`** |
| 1.2 Hot Fix | 169,646 | `c296c2d8e695d40c6f894540f597afb0f22fb962a10f76e3d3b39815563c3770` |

Identical hashes = zero changed bytes. Header confirms: 993 records, NextObjectID `0x3E0F` — the pre-hotfix
values.

## Consequences
- It fixes nothing. The commenters are correct.
- **It is actively harmful if it wins the overwrite** against the official 1.2 Hot Fix: it reverts the plugin
  to 993 records and removes `COBJ co_Armor_Power_TES51_Helm2`, so the TES-51 Helm Mk II becomes
  uncraftable again.
- Every defect listed in `analysis/01-base-vs-hotfix.md` is present unchanged (deleted vanilla REFR
  `0016BDE6`, probable ITMs, broken previsibines in Back Bay, wrong NextObjectID, no ESL).

## Action
Do not install. If already installed in Vortex, ensure it loses the file-conflict against the Hot Fix, or
remove it outright.
