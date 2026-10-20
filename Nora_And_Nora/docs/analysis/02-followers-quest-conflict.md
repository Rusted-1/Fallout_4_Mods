# 02 — The Followers quest conflict

All three companion mods override the vanilla **`Followers`** quest (`000289E4`, "Follower &
Companion System Control Quest"). Only the last-loaded override takes effect.

Compared field by field (script properties compared as data, ignoring member order and
uninitialised padding bytes in `DNAM` / `CTDA`):

| Mod | Real change to Followers |
|---|---|
| Nora Spouse | None. Its copy matches the shared baseline. |
| Synthetic Love | Adds **4 entries to `FollowersScript.AffinityEvents`**: `p865_CustomEventNoraLoves`, `…Likes`, `…Dislikes`, `…Hates` (keywords `26CB`–`26CE`). These are synth Nora's custom affinity reactions. |
| UCF (`EFF.esp`) | Adds alias 17 `DismissMessageTarget` (ANAM 17 → 18) and two script properties: `ExtensionHooks` → `EFF.esp:000FFF`, `DismissMessageTarget` → alias 17. |

## Consequences
- **Nora Spouse vs Synthetic Love:** harmless. `NoraSpouse.esm` is an ESM, so it always loads before `p865_SyntheticLove.esp`, and it changes nothing anyway.
- **UCF vs Synthetic Love:** real conflict. If `EFF.esp` loads after Synthetic Love, synth Nora's four custom affinity events disappear and her scripted reactions can't change her affinity. If Synthetic Love loads after UCF, UCF loses its hook and dismiss alias. Nora Spouse's readme reports UCF incompatibility, which is consistent with this.

## Fix (v0.1.0)
The UCF variant of `NoraAndNora.esp` carries UCF's record byte-for-byte, with Synthetic Love's four
events appended (renumbered to the patch's Synthetic Love master slot) and UCF's hook renumbered to the
patch's UCF slot. `tools/verify.py` checks that nothing else differs.
