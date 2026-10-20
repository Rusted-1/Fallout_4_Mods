# 04 — Game version and framework checks

My game is the **old runtime (1.10.163)**.

| File | Format | OK on old runtime? |
|---|---|---|
| `NoraSpouse.esm` | HEDR 1.00, form version 131 | Yes |
| `p865_SyntheticLove.esp` (all 8) | HEDR 1.00, form version 131 | Yes |
| `p865_SyntheticLove - Main.ba2` | **BA2 v8 (Next-Gen)** | Only with **BASS**, which I have |
| `NoraSpouse - Main.ba2`, UCF BA2s | BA2 v1 | Yes |
| `EFF.esp` (UCF 1.1.0) | HEDR 0.95, form version 131 | Yes |
| `REFramework.esm` (Random Encounter Framework 1.02) | ESM+ESL, form version 131 | Yes. **Masters all three DLCs** (Automatron, Far Harbor, Nuka-World) |
| Encounter Zone Recalculation 1.0 | F4SE DLL (2020) | Yes, it's the old-runtime build. Not needed by this patch |

## Random Encounter Framework
Restructures the vanilla Story Manager random-encounter nodes (76 quest nodes, 37 branch nodes, no
scripts) so mods can add encounters without overwriting each other. Planned for synth Nora's
death-site encounter (design choice 4). Still needed: the example plugin from the mod's optional
files, to see the intended attach point.
