# Texture rework

Written to `C:\Nu-uh\Fallout_4_TES_Power_Armor\TES-51 Textures Fixed\textures\...` (72 files + README).
Zip that folder and install through Vortex; it must win the file conflict against the TES-51 mod.

Tooling: `libnvtt-bin` / `nvcompress` 2.0.8 in the session container. ImageMagick for the one resize.

## Survey of the originals
72 textures, 151 MB. **Every one shipped with `mips=1`** — no mip chain anywhere. Verified by reading
11 DDS headers directly and classifying the remaining 61 by exact byte size (size = 128-byte header +
exact base level, which pins dimensions and format when no mips are present).

| Class | Count |
|---|---|
| 2048×2048 DXT1 | 51 |
| 1024×1024 DXT1 | 6 |
| 512×512 DXT5 | 5 |
| 2048×2048 BC5U | 3 |
| 4096×4096 DXT1 | 3 |
| 1024×1024 DXT5 | 2 |
| 256×256 DXT5 | 1 |
| 128×128 DXT1 (gradient) | 1 |

## Changes
1. **Mipmaps generated on all 72.** 151 MB → 208 MB on disk; lower runtime VRAM and bandwidth.
2. **Six normal maps DXT1 → BC5**: `TES51_Arm_n`, `TES51_Body_n`, `TES51_Helmet_n`, `TES51_Leg_n`,
   `TES51_Helmet2_n`, `TES51_SoulGems_n`. Three others (`TES51_Backpack_n`, `SteelSword_n`,
   `SteelWarhammer_n`) were already BC5 — the author knew the format and missed six files.
3. **`TES51_Helmet2_n` resized 4096 → 2048.** At 4096 BC5 with mips it was 22.4 MB, over the 20 MB
   per-file device-bridge limit. Source was DXT1, so the extra resolution held degraded data anyway.
   `TES51_Helmet2_Alt_s` and `TES51_Helmet2_Skyforge_d` kept at 4096.
4. **`TES51_TeslaGrad.dds` copied through untouched** — a 128×128 shader lookup ramp, not a surface
   texture. Mipmapping a LUT changes what the shader samples.

Nothing was upscaled or repainted. Every source pixel came from the mod's own files.

## Notes
- `nvcompress` 2.0.8 cannot read the `BC5U` fourcc, only `ATI2`. The three already-correct normals were
  fed through a temp copy with the fourcc patched to `ATI2`.
- All BC5 output was written back with the `BC5U` fourcc to match what the mod's own working normal maps
  already use in this install — both map to `BC5_UNORM`, but matching removes any doubt.
- Verified post-conversion: 0 files without mipmaps (except the deliberately skipped gradient),
  every `_n` file `BC5U` with a full chain, all dimensions preserved except the one intentional resize.
