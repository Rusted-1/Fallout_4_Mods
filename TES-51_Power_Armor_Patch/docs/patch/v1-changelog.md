# TES51_Patch.esp — changelog

Delivered as `TES-51 Power Armor Patch (ESL).zip`.

**v3 targets 4estGimp's ESL conversion, not the original .esp.** Masters: `Fallout4.esm`,
`SkyrimInspiredPowerArmor.esl`. ESL-flagged, zero new records, 58 overrides
(38 MISC, 16 OMOD, 1 LCTN, plus WRLD `0000003C` / CELL `00018AA2` as byte-identical structural
passthrough). `ONAM` = `01000A24`.

---

## v3 — retargeted at the ESL

### The install was wrong: the mod was loaded twice
Data contained **both** `SkyrimInspiredPowerArmor.esp` (169,646 B — the official Hot Fix) and
`SkyrimInspiredPowerArmor.esl` (166,689 B — 4estGimp, Nexus 85030), both enabled. Different
filenames, so Vortex saw no conflict. Two full copies of the mod: duplicate armor, recipes,
interiors and map markers.

**Resolution: disable the .esp, keep the .esl.** No save existed, so no item loss.

### What 4estGimp's ESL already fixed (verified by record-level diff)
- Removed the deleted vanilla `REFR 0016BDE6` override entirely — cleaner than undelete-and-disable.
- Removed the ITM `FLST do_ModMenuSlotKeywordList`.
- FormIDs compacted to `0x800`–`0xFB5`; plugin light-flagged.
- Built from the Hot Fix, so the Helm Mk II recipe is present.

Records whose original object ID was already ≤ `0xFFF` kept their FormIDs; the rest were renumbered
(e.g. `PA_TES51_Arm_Misc_TrophyR` stayed `01000FAF`, `PA_TES51_Arm_Misc_Trophy02L` moved
`01003DD4` → `010008C9`). The patch is remapped by EditorID.

### What 4estGimp did NOT fix — this patch's whole job
Map marker flags, all six trophies, torso lining C, Hot Rod paint rate, the wrong `LCTN MNAM`,
the 38 loose-item names, six missing descriptions, one grammar error, one stray property.

### The PRP question, settled empirically
- **`prp.esp`'s own Commonwealth WRLD record also has no `RNAM`, `OFST` or `CLSZ`** — the same shape
  as the TES-51 mod's. So the "missing 7,111 large references" concern is not something even the
  authoritative previsibine mod addresses. Passing the record through unchanged is not a regression.
  The whole v2 judgment call was about a non-issue.
- **PRP does override `CELL 0000E116`** (Back Bay) with regenerated `VISI` / `PCMB` / `XCRI` / `XPRI`.
  **v2's restoring that cell to vanilla would have clobbered PRP's previs.** Removed in v3 — the cell
  is no longer touched at all, which is safe because 4estGimp already removed the deleted reference
  that made it necessary.
- PRP does not override `CELL 00018AA2`.

### Dropped from v2 (no longer needed)
UDR of `REFR 0016BDE6`, the `CELL 0000E116` restore, the `CELL 00018AA2` restore. All obsolete once
targeting the ESL.

---

## Fixes carried forward

| Area | Change |
|---|---|
| Map marker | `FNAM` `0x03` → `0x00`; `LCTN MNAM` `000A8C6D` → `01000A24` |
| Trophies ×6 | PA_*_AV (set, never read) → raw SPECIAL AVIFs, matching vanilla `PA_Raider_Torso_Misc_Str` |
| Hot Rod paint | `PA_Strength_AV` `+2` → `+1` |
| Torso Lining C | Health `+60` → `+120` |
| Naming | 38 MISC renames |
| Text | 6 descriptions added, 1 grammar fix |
| Cleanup | stray property removed from the null sword mod |

Trophy values: Brahmin/Yao Guai STR +1 CHA +1; Deathclaw/Great STR +2 CHA +2; both Forsworn
STR +2 END +1 CHA −1. AVIFs: STR `000002C2`, END `000002C4`, CHA `000002C5`.

---

## Open items
1. **Complex Item Sorter** runs at the end of the load order and may rename the loose mod items,
   overriding the names in this patch. Harmless; re-run CIS after installing if desired.
2. Textures: no mipmaps anywhere; normal maps are DXT1 instead of BC5; `TES51_Helmet2_n.dds` is
   4096×4096 DXT1, 8 MB. Asset job, separate from the plugin.
3. `plugins.txt` was never read, so exact load-order positions are unconfirmed — but with the Back Bay
   cell no longer touched, no ordering question remains for this patch.
