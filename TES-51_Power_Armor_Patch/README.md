# TES-51 Power Armor -Skyrim Inspired- — Fix Patch

Backup of my patch for the old Fallout 4 mod *TES-51 Power Armor -Skyrim Inspired-*. The patch fixes
its bugs and adds new content: eight late-game armour tiers (Model G: Iron Reinforcement → Model N:
Daedric), unique trophy legendaries, FIS / FallUI support, and compatibility patches for More Power
Armour Mods and Kat's Power Armor Repair Kits.

**Needs the original mod.** This repo holds only my own work. It does not include the TES-51 Power
Armor mod or any other mod's files.

## What's here

| Folder | Contents |
|---|---|
| `FOMOD/TES-51 Patch FOMOD/` | The installer, **without its `textures` folder** (see below). Every plugin variant, `fomod/ModuleConfig.xml`, `README.txt` |
| `tools/` | The Python scripts that build the plugins, plus the v1.0 patch plugins they start from (`tools/v1.0-patch-inputs/`) |
| `docs/` | Project notes: analysis of the original mod, and a changelog / design doc for every patch version |
| `notes/` | My working notes: the first tier draft and the Enchantments plan (in progress) |

## Textures are not included
The FOMOD's `textures` component (72 DDS files, about 208 MB) is a re-encode of the original mod
author's textures: mipmaps added, six normal maps moved to BC5. Those are the original author's
assets, so they stay out of a public repo. How they were made is recorded in
`docs/patch/v2-texture-rework.md` and `docs/patch/v4-map-marker-resolution-and-install-state.md`.
The conversion script itself (`convert_textures.py`) was not available when this backup was made.

To rebuild a complete installer, copy the `textures` folder from the local FOMOD into
`FOMOD/TES-51 Patch FOMOD/` and zip that folder.

## Rebuilding the plugins
Run with Python 3, from inside `tools/`. Some scripts have absolute paths from my working session
written into them, so adjust those first. The pipeline is:

1. `build_tiers.py <base plugin> <v1.0 TES51_Patch.esp> <out> [<INNR source>]`: adds the eight tiers
2. `brahmin_regen.py <out>`: Brahmin's Endurance health regen (Unique Legendaries variants only)
3. `build_addons.py fis <base plugin> <built TES51_Patch.esp> <out>`: FIS tag add-on
4. `build_kat.py <Some_Assembly_Required_Repair_Kits.esp> <base plugin> <out>`: Kat's repair-kit patch
5. `verify.py`: checks masters, FormID ranges and references in every built plugin

The base plugin is either 4estGimp's `SkyrimInspiredPowerArmor.esl` or the 1.2 Hot Fix
`SkyrimInspiredPowerArmor.esp`. Always build from the v1.0 inputs; `brahmin_regen.py` refuses to run
twice on the same file.

## Status
Plugins are verified at the file level. The new tiers, the Brahmin regen, the FIS tags and the Kat's
patch have not been tested in game yet. The Enchantments slot is still being planned.
