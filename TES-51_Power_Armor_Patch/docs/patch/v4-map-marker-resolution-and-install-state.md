# v4 — Bethesda Comics marker: resolved (install-side, not plugin-side)

**Status: confirmed working in game on both the ESP and the ESL base (2026-09-01).**

## Symptom
After several build/test cycles, the Bethesda Comics map marker was still
visible and immediately fast-travelable on leaving Vault 111 — with both the
ESL-targeted and ESP-targeted patch builds.

## Root cause — two independent faults, both install-side
Every file-level check of the patch had passed. The plugin was never the
problem.

1. **The patch was never deployed.** A listing of
   `D:\SteamLibrary\steamapps\common\Fallout 4\Data` (1,069 plugins) showed
   neither `TES51_Patch.esp` nor `TES-51-MPAM.esp`. The mod existed in the
   Vortex staging folder but had never been hardlinked out. Every test ran
   with `SkyrimInspiredPowerArmor.esp` alone.
2. **The staged build was the wrong variant.** The file Vortex had installed
   was the ESL build:
   `MAST = Fallout4.esm, SkyrimInspiredPowerArmor.esl`. The ESL base mod had
   been disabled for ESP testing, so even once deployed the plugin would have
   been rejected for a missing master.

## The pairing rule
The patch variant must match the enabled base plugin, and only one base may
be enabled at a time — the ESP and the ESL each carry their own Bethesda
Comics marker, and a patch only silences the one it masters. A mismatched
pair produces no error in game; the patch simply does not load.

| Base plugin | Marker REFR | LCTN | Patch variant |
|---|---|---|---|
| `SkyrimInspiredPowerArmor.esp` (1.2 Update, 169,533 and Hot Fix, 169,646 — identical) | `0100A31B` | `01008470` | `Plugin (ESP) - …` |
| `SkyrimInspiredPowerArmor.esl` (4estGimp) | `01000A24` | `010009F3` | `Plugin - …` |

Both shipped `FNAM = 03` (Visible + CanTravelTo). 111 of 119 vanilla
Commonwealth map markers use `FNAM = 0x00`.

## Verified working configuration (ESL)
Vortex staging folder `TES-51 Patch FOMOD (2)`, installed from the FOMOD with
the ESL option and deployed (both plugins hardlinked into Data):

```
TES51_Patch.esp   22,594 bytes  (ESL / Unique Legendaries + Debug)
  MAST  Fallout4.esm, SkyrimInspiredPowerArmor.esl
  ONAM  01000A24
  REFR  01000A24  FNAM = 00   (undiscovered, no fast travel)

TES-51-MPAM.esp   25,761 bytes  (ESL-targeted MPAM patch)
```

Load order: both patch plugins after `SkyrimInspiredPowerArmor.esl` and
`More Power Armour Mods.esp`. Test on a save from before the marker was ever
discovered — discovered-state is baked into the save.

## Process note
When a verified-correct plugin fix does not take effect in game, check
deployment and master resolution **before** rebuilding the plugin again. The
decisive evidence was a directory listing of Data and a read of the master
list on the actually-installed file — neither had been done for several
iterations. A staging file that refuses to stage with
`file is hardlinked (nlink > 1)` is positive proof Vortex has deployed it.

## FOMOD source — complete as of 2026-09-01
`C:\Nu-uh\Fallout_4_TES_Power_Armor\TES-51 Patch FOMOD\`

```
fomod\                                  info.xml + ModuleConfig.xml (4 steps, 10 patterns)
Plugin - Fixes Only                     ESL, 16,404
Plugin - Fixes Only + Debug             ESL, 18,182
Plugin - Unique Legendaries             ESL, 20,816
Plugin - Unique Legendaries + Debug     ESL, 22,594
Plugin (ESP) - Fixes Only               ESP, 16,404
Plugin (ESP) - Fixes Only + Debug       ESP, 18,182
Plugin (ESP) - Unique Legendaries       ESP, 20,816
Plugin (ESP) - Unique Legendaries + Debug   ESP, 22,594
Patch - More Power Armour Mods          ESL-targeted, 25,761
Patch (ESP) - More Power Armour Mods    ESP-targeted, 25,684
textures\                               72 files, 208,073,536 bytes
README.txt
```

Note the ESL and ESP builds are byte-for-byte the same *sizes* — the only
difference is the MAST entry. Size alone cannot tell them apart; read the
master list.

All 11 `source="…"` folder names in `ModuleConfig.xml` were verified against
the folder names actually on disk. A mismatch there installs nothing and
reports no error.

### Textures component
72 DDS re-encoded with full mipmap chains; six normal maps moved DXT1 → BC5;
one 4096 map halved to 2048; `TES51_TeslaGrad.dds` skipped deliberately
(128×128 shader lookup ramp — mipmapping a gradient LUT changes what the
shader reads). Nothing upscaled or repainted. The component must be sorted to
overwrite the TES-51 Power Armor mod's own textures.

Final format census of the shipped set: **55 DXT1, 8 DXT5, 9 ATI2 (BC5)**.

#### Normal-map fourcc: ATI2, not BC5U (changed 2026-09-06)
All nine `_n` normal maps carry the **ATI2** fourcc. An earlier revision of
`convert_textures.py` rewrote nvcompress's native ATI2 output to `BC5U` to
match three of the mod's own originals; that was reverted at the user's
request and the header comment in the script now says not to re-add it.

The two tags name the same thing — DirectXTex maps both `ATI2` and `BC5U` to
`DXGI_FORMAT_BC5_UNORM`, and the change touched **only bytes 84–87** of each
file (verified: pixel data byte-identical before and after, no re-encode, no
generation loss). ATI2 is the more widely recognised tag and what most FO4
tooling emits.

Caveat worth recording: this could not be verified against vanilla directly,
because vanilla ships all textures inside BA2 archives, which store a DXGI
format enum per texture and carry no fourcc at all. So there is no vanilla
*loose-file* fourcc to compare to; the convention comes from tooling, not
from a Bethesda-shipped loose DDS. The original mod's own three BC5 normals
were `BC5U` and worked in game, so both tags are known-good on this engine.
If lighting on the armour ever looks wrong, this is a 4-byte revert.

Original-vs-rebuild normal maps:

| File | Original | Rebuild |
|---|---|---|
| `TES51_Arm_n` | DXT1 2048, 1 mip | ATI2 2048, 12 mips |
| `TES51_Backpack_n` | BC5U 2048, 1 mip | ATI2 2048, 12 mips |
| `TES51_Body_n` | DXT1 2048, 1 mip | ATI2 2048, 12 mips |
| `TES51_Helmet_n` | DXT1 2048, 1 mip | ATI2 2048, 12 mips |
| `TES51_Leg_n` | DXT1 2048, 1 mip | ATI2 2048, 12 mips |
| `TES51_SoulGems_n` | DXT1 1024, 1 mip | ATI2 1024, 11 mips |
| `TES51_Helmet2_n` | DXT1 4096, 1 mip | ATI2 2048, 12 mips |
| `SteelSword_n` | BC5U 2048, 1 mip | ATI2 2048, 12 mips |
| `SteelWarhammer_n` | BC5U 2048, 1 mip | ATI2 2048, 12 mips |

Note none of the originals had mipmaps at all — every one shipped with a
single surface. That, not the compression format, was the main defect.

## Still open
- In-game verification of Hunter's Calling (3 creature-type damage
  reductions) and Forsworn's Rejection (2) — no vanilla item sets more than
  one.
- Deployed base is the plain 1.2 Update (169,533), not the Hot Fix
  (169,646). Marker FormIDs are identical, so the patch fits either; the Hot
  Fix is the better base.
- Optional: align MPAM slot-two mod names with the corrected slot-one names.
