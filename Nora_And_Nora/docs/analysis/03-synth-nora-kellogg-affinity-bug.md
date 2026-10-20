# 03 — Synth Nora's affinity bug ("Kellogg is dead" before he is)

## What I reported
Synth Nora's affinity seems to progress on its own, and she says things like "Kellogg is dead" when he isn't.

## Confirmed cause of the Kellogg lines
Synthetic Love's first-time **Admiration** scene, `p865_COMNora_02_FriendshipToAdmiration`, is a conversation about Kellogg's death:
- "Kellogg's dead" / "He was a monster. The things he did..."
- player options "How can I argue with that?", "I just wanted to stop a killer", "He was complex", "Take it easy. Kellogg's dead."

**None of those INFOs carry conditions.** The scene plays as soon as her affinity crosses the Admiration threshold (`CompanionActorScript` ThresholdData → `p865_COMNora` stage 400), whether or not Kellogg is dead.

## Planned fix
`CompanionActorScript` ThresholdData supports a **`ConditionalGlobal`** per threshold (Synthetic Love already uses one for Hatred: `p865_Nora_AffinityCondition_HatredAllowed`). Plan:
1. Add a new global to the patch and set it as the Admiration threshold's `ConditionalGlobal` on `p865_CompanionNora`.
2. A small quest script sets it to 1 once Kellogg is dead (MQ106 stage, to be confirmed from `Fallout4.esm`).
3. Later phase: a new, Kellogg-free admiration talk for when he is still alive.

Still to confirm from vanilla files: how the vanilla script treats a threshold whose global is 0 (cap vs skip), and the MQ106 stage number.

## Probable cause of "random" progression
Unconfirmed. Most likely contributor: the Followers conflict (doc 02) when UCF loads after Synthetic Love. To re-check in game after installing the patch.
