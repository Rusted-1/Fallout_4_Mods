# Vulpine Race — Human Nate Patch

Backup of my patch that keeps the **player character human** while the rest of
*Vulpine Race V5.1* carries on working normally.

Vulpine Race is all-or-nothing: it has no option to apply the fox race to only one of the
two pre-war spouses. Playing as Nate, this patch gives you a **human Sole Survivor** and
leaves **Nora in the pre-war intro as a Vulpine**, untouched.

**Needs the original mod.** This repo holds only my own work. It does not include Vulpine
Race's plugins, BA2 archives, meshes or textures, or any file from Eli's Robo Leg Outfits.

## What's here

| Folder | Contents |
|---|---|
| `FOMOD/Vulpine_Human_Nate/` | The installer: `fomod/` config and `Main/VulpineNateHuman.esp` (always installed), plus the user-facing `README.txt` |
| `tools/` | `esp.py` (plugin reader), `build_patch.py` (builds the plugin), `verify.py` (checks it) |
| `docs/analysis/` | How Vulpine Race actually applies the race, and why the old Xbox load-order trick was a red herring |
| `docs/patch/` | v1.0 design: the one-field change, plugin properties, known limits |

## What it changes

One record. `Player` (`00000007`) has its RNAM race field redirected from `VulpineRace`
(`01000F99`) back to vanilla `HumanRace` (`00013746`). Everything else on that record —
perks, keywords, hair colour, default outfit, voice type — is copied across byte for byte
from Vulpine's own version.

`MQ101PlayerSpouseMale` and `MQ101PlayerSpouseFemale` are **not touched**, which is what
keeps Nora Vulpine.

## Installing

Zip the `FOMOD/Vulpine_Human_Nate/` folder (zip its contents so `fomod/` sits at the top of
the zip) and drag the zip into Vortex. There are no options to pick.

Load order sorts itself: the patch masters `VulpinePlayer.esp`, so the game and LOOT always
place it afterwards. The plugin is an ESL-flagged `.esp`, so it does not use one of the 255
regular plugin slots.

**There is no in-game race toggle.** Fallout 4 has no race selector in the character
creation mirror — race is locked by the Player record. The plugin itself is the switch:
enabled means human player, disabled means Vulpine player.

**Start a new game.** Changing the player's race on an existing save is a reliable way to
break the character's head mesh.

**Both sexes are affected.** Male and female share the single `Player` record, so this makes
the player human whichever one is picked at the mirror. A Vulpine *player* Nora would mean
disabling the patch for that save.

## Rebuilding the plugin

Run with Python 3 from the folder that holds `tools/`. The scripts take paths as arguments,
so there is nothing to edit. You need Vulpine Race's own `VulpinePlayer.esp`, which is not
in this repo — point at the copy in your Vortex staging folder or the downloaded archive.

```
python3 -I tools/build_patch.py "<path>/VulpinePlayer.esp" FOMOD/Vulpine_Human_Nate/Main/VulpineNateHuman.esp
python3 -I tools/verify.py FOMOD/Vulpine_Human_Nate/Main/VulpineNateHuman.esp "<path>/VulpinePlayer.esp"
```

`build_patch.py` is deterministic — rebuilding from the same source reproduces the shipped
plugin byte for byte.

`verify.py` checks that the plugin holds exactly one record, that its RNAM is vanilla
HumanRace, that the masters are right and in order, that the TES4 header is ESL-flagged,
that no spouse record came along, and — when given the source plugin as a second argument —
that RNAM is the *only* subrecord that differs from Vulpine's original.

`esp.py` can also dump any Fallout 4 plugin's structure on its own:

```
python3 -I tools/esp.py "<path>/VulpineRace.esm"
```

## Status

v1.0. Verified at the file level: all `verify.py` checks pass and the build reproduces
byte for byte. **Not yet confirmed in game.**

First run should check:

- Nate appears fully human at the mirror, with vanilla head parts and no missing-mesh markers
- Nora still renders as a Vulpine in the pre-war house and the vault sequence

Possible future work, not started: a true per-sex split (human male, Vulpine female on the
same plugin) would need a Papyrus script on a startup quest reading
`Game.GetPlayer().GetActorBase().GetSex()` and swapping the race — feasible, but it needs
the Creation Kit or a compiler. The same one-record override technique generalises to any
other NPC_ record whose race you want redirected.
