# Nora and Nora — Nora Spouse × Synthetic Love

My patch and interaction mod for running two Nora companions together: the **real, human Nora**
from *Nora Spouse Companion* (House Variable) and the **synth Nora** from *Synthetic Love*
(Thrillvilled). The long-term goal is for the two to recognise each other, with unique dialogue,
interactions and actions from their first meeting to the late game. The full design is in
[`notes/interaction-ideas.md`](notes/interaction-ideas.md).

**Needs the original mods.** This repo holds only my own work. It does not include Nora Spouse,
Synthetic Love, Unlimited Companion Framework, Random Encounter Framework or any of their files.

## Status: v0.2.0 — compatibility fixes
- **Done:** Followers quest merge for UCF users (v0.1). Kellogg fix for synth Nora's Admiration scene (v0.2). Both verified at the file level, not yet tested in game.
- **Planned:** first meeting, Vault 111 breakdown and choice, relationship tiers, Shaun/faction reactions, romance, death-site encounter.

## What's here

| Folder | Contents |
|---|---|
| `FOMOD/Nora and Nora/` | The installer: `fomod/` config, `UCF/NoraAndNora.esp`, `NoUCF/NoraAndNora.esp`, `Scripts/NN_KelloggGateScript.pex` |
| `tools/` | `esp.py` (plugin reader), `vmad.py` (script-data parser), `ba2.py` (archive reader), `lines.py` (dialogue dump), `build.py` (builds the plugins), `verify.py` (checks them), `pex.py` / `pexw.py` (Papyrus bytecode reader and writer), `kellogg_gate.py` (builds the Kellogg script) |
| `docs/analysis/` | Findings about the source mods: how each Nora works, the Followers conflict, the Kellogg bug, game-version checks |
| `docs/patch/` | Design and changelog per version |
| `notes/` | My design ideas for the interactions |

## Requirements and load order
- Nora Spouse Companion 1.2 (`NoraSpouse.esm`)
- Synthetic Love (`p865_SyntheticLove.esp`), **any of its 8 installer versions**: they share identical record IDs, so one patch plugin covers all of them
- Optional: Unlimited Companion Framework (`EFF.esp`)
- Compatible as-is, no patch needed: Nora Spouse Far Harbor Support, Nora Spouse CTO Patch, SS2 Nora Spouse Patch (see `docs/analysis/05-…`)
- Old-runtime game (1.10.163) is fine. Synthetic Love's archive is BA2 v8, which the old game reads only with BASS (Backported Archive2 Support System); the patch itself has no archive.

The patch masters every mod it touches, so LOOT always sorts it after them. It is an ESL-flagged
`.esp`, so it does not use one of the 255 regular plugin slots.

## Installing
Zip the **contents** of `FOMOD/Nora and Nora/` (so `fomod/` sits at the top of the zip) and drag the
zip into Vortex. The installer asks one question: do you use UCF? It pre-selects the answer from
whether `EFF.esp` is active.

## Rebuilding
From inside `tools/`, with Python 3:

```
python3 -I build.py <p865_SyntheticLove.esp> <NoraSpouse.esm> <EFF.esp> <out dir>
python3 -I verify.py <out dir>/UCF/NoraAndNora.esp <EFF.esp> <p865_SyntheticLove.esp>
python3 -I kellogg_gate.py <out dir>/Scripts/NN_KelloggGateScript.pex
```

Any Synthetic Love version works as the input. The scripts take every path as an argument; nothing is hard-coded.
