# Nora and Nora — Nora Spouse × Synthetic Love

My patch and interaction mod for running two Nora companions together: the **real, human Nora**
from *Nora Spouse Companion* (House Variable) and the **synth Nora** from *Synthetic Love*
(Thrillvilled). The long-term goal is for the two to recognise each other, with unique dialogue,
interactions and actions from their first meeting to the late game. The full design is in
[`notes/interaction-ideas.md`](notes/interaction-ideas.md).

**Needs the original mods.** This repo holds only my own work. It does not include Nora Spouse,
Synthetic Love, Unlimited Companion Framework, Random Encounter Framework or any of their files.

## Status: v0.4.0 — fixes + Phase 1 systems
- **Done:** Followers quest merge for UCF users (v0.1). Kellogg fix (v0.2). Phase 1 outcome system, console-driven until the scenes exist (v0.3). Battle-site add-on (v0.4). All verified at the file level, not yet tested in game.
- **Writing:** Phase 1 script, draft 3 (`docs/script/phase1-script.md`).
- **Planned:** first meeting, Vault 111 breakdown and choice, relationship tiers, Shaun/faction reactions, romance, death-site encounter.

## What's here

| Folder | Contents |
|---|---|
| `FOMOD/Nora and Nora/` | The installer: `fomod/` config, `UCF/NoraAndNora.esp`, `NoUCF/NoraAndNora.esp`, `Scripts/` (`NN_KelloggGateScript.pex`, `NN_Phase1Script.pex`, `NN_FinalWishScript.pex`, `NN_BattleSiteScript.pex`), `Impatient/NoraAndNora - Impatient.esp`, `BattleSite/NoraAndNora - Battle Site.esp` |
| `tools/` | `esp.py` (plugin reader), `vmad.py` (script-data parser), `ba2.py` (archive reader), `lines.py` (dialogue dump), `build.py` (builds the plugins), `verify.py` (checks them), `pex.py` / `pexw.py` (Papyrus bytecode reader and writer), `kellogg_gate.py` (builds the Kellogg script), `voice_sheet.py` (script → voice sheet CSV), `xva_batch.py` (voice sheet → xVASynth batch CSV), `pexasm.py` (structured Papyrus assembler), `phase1_scripts.py` (builds the Phase 1 script), `verify_refs.py` (checks plugins against masters and scripts), `esmscan.py` (Fallout4.esm scanner), `battlesite_scripts.py` / `battlesite_build.py` (battle-site scripts and add-on plugin), `gen_sigs.py` (regenerates `sigs.json`, the vanilla signature list; not committed) |
| `docs/analysis/` | Findings about the source mods: how each Nora works, the Followers conflict, the Kellogg bug, game-version checks |
| `docs/patch/` | Design and changelog per version |
| `docs/script/` | Dialogue scripts (also the AI voice sheet). `phase1-script.md`: first meeting through the Vault 111 choice. `phase1-voice-sheet.csv` + `voice-guide.md`: AI voice sheet (89 lines, reserved file names 0x900–0x958). `phase1-xvasynth-batch.csv`: the same lines as an xVASynth batch file |
| `notes/` | My design ideas for the interactions |

## Requirements and load order
- Nora Spouse Companion 1.2 (`NoraSpouse.esm`)
- Synthetic Love (`p865_SyntheticLove.esp`), **any of its 8 installer versions**: they share identical record IDs, so one patch plugin covers all of them
- Optional: Unlimited Companion Framework (`EFF.esp`)
- Optional, for the battle-site add-on: Random Encounter Framework 1.02 + Automatron, Far Harbor and Nuka-World. Rebuilding it needs the framework's example plugin as a template; that's the framework author's file, so it isn't in this repo
- Recommended: Extended Dialogue Interface (XDI) for full-text player lines
- Compatible as-is, no patch needed: Nora Spouse Far Harbor Support, Nora Spouse CTO Patch, SS2 Nora Spouse Patch (see `docs/analysis/05-…`)
- Old-runtime game (1.10.163) is fine. Synthetic Love's archive is BA2 v8, which the old game reads only with BASS (Backported Archive2 Support System); the patch itself has no archive.

The patch masters every mod it touches, so LOOT always sorts it after them. It is an ESL-flagged
`.esp`, so it does not use one of the 255 regular plugin slots.

## Installing
Zip the **contents** of `FOMOD/Nora and Nora/` (so `fomod/` sits at the top of the zip) and drag the
zip into Vortex. The installer asks:
1. Do you use UCF? Pre-selected from whether `EFF.esp` is active.
2. Synth Nora's patience: does she wait forever, or leave after 7 days if left in Vault 111?
3. Battle site add-on: offered only with Random Encounter Framework and all three DLCs.

## Rebuilding
From inside `tools/`, with Python 3:

```
python3 -I build.py <p865_SyntheticLove.esp> <NoraSpouse.esm> <EFF.esp> <out dir>
python3 -I verify.py <out dir>/UCF/NoraAndNora.esp <EFF.esp> <p865_SyntheticLove.esp>
python3 -I gen_sigs.py <extracted vanilla scripts folder>
python3 -I kellogg_gate.py <out dir>/Scripts/NN_KelloggGateScript.pex
python3 -I phase1_scripts.py <out dir>/Scripts/NN_Phase1Script.pex
python3 -I battlesite_scripts.py <out dir>/Scripts
python3 -I battlesite_build.py "<REFramework Example Plugin.esp>" <out dir>/BattleSite
python3 -I verify_refs.py <out dir>/UCF/NoraAndNora.esp <out dir>/Scripts Fallout4.esm=<path> NoraSpouse.esm=<path> p865_SyntheticLove.esp=<path> EFF.esp=<path>
```

Any Synthetic Love version works as the input. The scripts take every path as an argument; nothing is hard-coded.
