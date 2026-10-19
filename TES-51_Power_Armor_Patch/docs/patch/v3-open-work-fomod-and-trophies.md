# v4 — FOMOD + unique trophy legendaries + MPAM patch (BUILT)

**The packaged folder must be named exactly `TES-51 Patch FOMOD`.** Zip that folder, drag into
Vortex. Currently assembled at `C:\Nu-uh\Fallout_4_TES_Power_Armor\ES-51 Patch FOMOD\` — that folder
is missing its leading T and should be renamed.

```
fomod/info.xml, fomod/ModuleConfig.xml
textures/…                                             (208 MB, 72 files)
Plugin - Fixes Only/TES51_Patch.esp                    16,404 B  58 rec
Plugin - Fixes Only + Debug/TES51_Patch.esp            18,182 B  73 rec (15 new)
Plugin - Unique Legendaries/TES51_Patch.esp            20,816 B  65 rec (6 new)
Plugin - Unique Legendaries + Debug/TES51_Patch.esp    22,594 B  80 rec (21 new)
Patch - More Power Armour Mods/TES-51-MPAM.esp         25,761 B  88 rec
README.txt
```

Installer: Step 1 Components (Plugin Fixes · Textures · MPAM patch) → Step 2 Trophy Effects
(Unique · Original) → Step 3 Debug. Four conditional patterns on `trophies` × `debug` flags; the
MPAM patch installs additively and auto-recommends when `More Power Armour Mods.esp` is active.

## Unique legendaries — final spec

| Mod name | Slot | Actor values | Enchantments |
|---|---|---|---|
| Brahmin's Endurance | arms | END +2, LCK +1, CarryWeight +20 | `ResistancesInverseHealth_DR` + `_ER` |
| Hunter's Calling | arms | STR +2, CHA +1, LessDmg Ghouls/SuperMutants/Animals | `LegendaryAddCommonPerk`, `ReflectDamage` |
| Yao Guai's Gaze | helmet | STR +2, PER +1, LessDmgStandStill | `LegendaryAddCommonPerk`, `APRegen` |
| Deathclaw's Persistence | helmet | AGI +2, STR +1, LessDmgBlockSprint, `PA_OptimizedServos_AV` +20 | `LegendaryAddCommonPerk`, `EnchPA_OptimizedServos` |
| Forsworn's Rejection | helmet | PER +2, STR +1, CHA −1, LessDmg Humans/Robots | `LegendaryAddCommonPerk` |
| Briarheart's Denial | torso | AGI +2, END +1, CHA −1 | `Chameleon`, `LowHealthSlowTime` |

Every effect is stock vanilla. No new ENCH, MGEF or PERK records were authored.

## Key finding that shaped the build
**Vanilla legendary armour enchantments have no name** — empty FULL on `Chameleon`,
`ReflectDamage`, `LowHealthSlowTime`, `APRegen`, `ResistancesInverseHealth`. The effect line
players read comes from the **OMOD's own FULL and DESC**, the same way `mod_Legendary_Weapon_*`
works. So the six custom enchantments originally approved were dropped — they would have been
invisible. Named effect line = OMOD FULL/DESC; item-name suffix = INNR.

## INNR rewrite
`dn_PowerArmor_TES51_INNR` ruleset 3 held three suffixes keyed on three keywords each shared by two
trophies. Replaced with six entries keyed on six new keywords (`0x02000001`–`0x02000006`), giving
`TES-51 Left Arm of Brahmin's Endurance`. All rules before and after the trophy block verified
byte-identical to the original.

## Debug recipes — 15
`0x02000010`–`0x0200001E`, `BNAM = WorkbenchChemlab (00102158)`,
**`FNAM = RecipeUtility (0006980C)`**, 1× Steel each. Seven ARMO pieces + eight trophy MISC items.

**Category keyword is mandatory.** All 49 vanilla chem-lab recipes carry an `FNAM`; none ships
without one. The first build omitted it and the recipes would not have appeared under any tab.
Subrecord order matches vanilla exactly: `EDID, FVPA, DESC, CNAM, BNAM, FNAM, INTV`.

## MPAM patch — rebuilt for the ESL
The original `TES-51-MPAM.esp` mastered `SkyrimInspiredPowerArmor.esp`. 313 of the mod's 339 records
were renumbered during 4estGimp's ESL compaction, so it pointed at wrong records once the ESP was
disabled. Rebuilt against the ESL: FormIDs remapped by EditorID, then verified — all 49 structural
references resolve to the same records as before, zero mismatches.

62 byte replacements audited: 55 aligned in `KWDA`/`INRD`/`MNAM`, 7 unaligned inside `OBTS` where
FormIDs genuinely sit at odd offsets (offset 22 and 43). No false positives.
Masters: `Fallout4.esm`, `More Power Armour Mods.esp`, `SkyrimInspiredPowerArmor.esl`. ESL-flagged
(max new object id `0xE36`). Shares no records with the main patch; independent of the trophy choice.

Left alone deliberately: MPAM's slot-two copies keep their original names ("TES Core Assembly"),
which do not match the corrected slot-one names. The difference may be what distinguishes the two
slots in the workbench menu.

## Verified
- ESL flag set on all builds; every new record in `0x000`–`0xFFF`.
- Masters correct; own-record prefix `0x02`.
- WRLD `0000003C` and CELL `00018AA2` byte-identical passthrough.
- All XML parses; installer steps and 4 patterns confirmed.

## Still needs in-game testing
No vanilla item sets more than one creature-type damage reduction. Hunter's Calling sets three,
Forsworn's Rejection two. The shared perk should evaluate each independently but this cannot be
proven from the files. If one fails to apply, that is the cause.

## Process note
Twice now a commit went to a stale path after the folder was renamed. **Re-check the destination
path with `device_list_dir` before every commit batch.**
