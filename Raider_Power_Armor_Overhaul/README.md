# Raider Power Armor Overhaul — RPA Fixes

Backup of my patch that rebalances three raider power armor mods into one clear ladder and gives
them the right FIS / FallUI icon:

**Vanilla Raider < Scrapper < Raider T-45 < Raider Brute**

| Set | Mod | Role in the ladder |
|---|---|---|
| Vanilla Raider | Fallout 4 | Floor, unchanged |
| Scrapper | *Rivets And Rage - A Scrappy Raider Armor Pack* | Junk-built step up from vanilla raider |
| Raider T-45 | *CWRaidPAT45* (CW Raider T-45 Power Armor) | Raider-patched T-45 frame, keeps the T-45 upgrade path |
| Raider Brute | *Rust King - Brute Power Armor* | Raider rebuild of a T-51 suit, top of the ladder, new T-51 style upgrade path |

**Needs the original mods.** This repo holds only my own work. It does not include any of the three
armor mods, FIS, or any other mod's files.

## What's here

| Folder | Contents |
|---|---|
| `FOMOD/RPA_Fixes/` | The installer: `fomod/` config, `Main/RPA_Fixes.esp` (always installed), `Debug/RPA_Fixes - Debug Chem Station.esp` (optional) |
| `tools/` | The Python scripts that read the plugins and build both patches |
| `docs/analysis/` | What the three mods looked like before the patch, and how FIS was tagging them |
| `docs/patch/` | v1.0 design: target stats, upgrade paths, FIS fix, debug plugin |

## Installing
Zip the `FOMOD/RPA_Fixes/` folder (zip its contents so `fomod/` sits at the top of the zip) and
drag the zip into Vortex. The installer has one option:

- **Debug: Craft all raider PA at the Chem Station.** Free recipes for all 18 pieces under the Chem
  Station's Utility tab. For testing only.

Load `RPA_Fixes.esp` after `CWRaidPAT45.esp`, `DesRustKing-RaiderBrutePowerArmor.esp`,
`DesRivetsAndRage-AScrappyRaiderArmorPack.esp` and `DesRivetsAndRage - Raider only patch.esp`.
Both plugins are ESL-flagged `.esp` files.

## Rebuilding the plugins
Run with Python 3 from the folder that holds `tools/`. The scripts expect this working layout,
which is not in the repo:

- `ex/cw/CWRaidPAT45.esp`
- `ex/rk/Rust King - Brute Power Armor - BA2/DesRustKing-RaiderBrutePowerArmor.esp`
- `ex/rr/Rivets And Rage - A Scrappy Raider Armor Pack - BA2/DesRivetsAndRage-AScrappyRaiderArmorPack.esp`
- `ex/fis/...` (the extracted FIS archive, only needed for `verify.py`'s FIS checks)

Steps:

1. `python3 -I tools/scan.py <Fallout4.esm> fo4.pkl ARMO,OMOD,INNR,KYWD,COBJ,MISC,AVIF,DMGT,ENCH,LVLI,FURN`
2. `python3 -I tools/scan.py <Fallout4.esm> fo4b.pkl TRNS,CMPO,PERK,MSWP,ARMA,FLST,EQUP,IMPF,SNDR,RACE`
3. Same two scans on `DLCNukaWorld.esm` into `nw.pkl` (`ARMO,OMOD,INNR,KYWD,COBJ,MISC,LVLI`) and
   `nwb.pkl` (`TRNS,CMPO,PERK,MSWP,ARMA,FLST`)
4. `python3 -I tools/make_patch.py out/RPA_Fixes.esp`: builds the main patch
5. `python3 -I tools/make_debug.py "out/RPA_Fixes - Debug Chem Station.esp"`: builds the debug plugin
6. `python3 -I tools/verify.py out/RPA_Fixes.esp`: checks that every FormID resolves and that
   overrides keep the original references. One expected difference is reported: the Raider T-45
   naming record, where the FIS tag ruleset is inserted.

Target stats live in the `TARGET` table at the top of `tools/make_patch.py`.

## Status
v1.0. Plugins are verified at the file level and tested in game, including the debug recipes.

Still to check: the ladder is anchored to vanilla `Fallout4.esm` values. These installed plugins may
change vanilla raider / T-45 / T-51 stats or touch these armors, and have not been compared yet:
`PowerArmorStatsPatch-AllDLC.esp`, `More Power Armour Mods.esp`,
`SimplePowerArmorReductionSystem.esp`, `DesRivetsAndRage - Raider only patch.esp`,
`unofficial fallout 4 patch.esp`.
