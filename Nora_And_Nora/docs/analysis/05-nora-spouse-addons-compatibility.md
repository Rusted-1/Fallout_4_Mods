# 05 — Nora Spouse add-ons: compatibility check

Three more Nora Spouse plugins are in my load order. Checked record by record against Nora Spouse,
Synthetic Love, UCF and each other.

| Plugin (Nexus) | Masters | What it is | Overrides |
|---|---|---|---|
| `NoraSpouseFarHarbor.esp` — Far Harbor Support 1.0 (House Variable, 24680) | Fallout4, DLCCoast, NoraSpouse | Nora interjections, idles, affinity and comments for Far Harbor | 217 Far Harbor DIAL/INFO/SCEN/QUST/PACK records, plus `COMNora` and `COMNoraIdles` |
| `Nora CTO.esp` — Nora Spouse Companion CTO Patch 0.1 (59834) | Fallout4, NoraSpouse (ESL) | Changes the `ENAM` flags on 10 of Nora's idle lines | `COMNora`, `COMNoraIdles`, 10 INFOs |
| `SS2 Nora Spouse Patch.esp` — Sim Settlements 2 patch 0.4 (57813) | Fallout4, SS2, NoraSpouse (ESL) | One SS2 dialogue line | 1 quest, 1 topic, 1 INFO in `SS2.esm` |

## Results
- **None of them touch** Synthetic Love, the vanilla `Followers` quest, or any record in `NoraAndNora.esp`.
  No conflict with this patch.
- **Far Harbor Support × CTO overlap** on `COMNora` and `COMNoraIdles` is harmless:
  - Both copies of `COMNora` equal Nora Spouse's original. Far Harbor's differs only by master-index renumbering
    (01 → 02 because of `DLCCoast.esm`) and padding. Fragment script properties, all 36 fragments and the alias
    section were checked after renumbering.
  - `COMNoraIdles`: CTO's copy is identical to Nora Spouse's. Far Harbor's only changes `TIFC` (info count 154 → 165)
    for its 11 new idle lines. INFOs are separate records, so they load whichever DIAL copy wins.
  - CTO's 10 INFO edits aren't touched by Far Harbor Support.
- **SS2 patch** is independent of everything else here.

## Installer
Nothing to add yet. These stay as their own mods in Vortex. Bundling their plugins into this installer would make
two Vortex mods supply the same files, and they're other authors' work. If later content builds on them
(e.g. synth Nora lines for Far Harbor), the FOMOD will offer that piece only when the matching plugin is active.
