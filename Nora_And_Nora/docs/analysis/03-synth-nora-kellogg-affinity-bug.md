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

Confirmed from vanilla files and implemented in v0.2.0: see `docs/patch/v0.2-kellogg-fix.md` (MQ106 stage 902; a locked threshold caps affinity one point below it).

## "Random" progression
Mostly vanilla design: `CompanionActorScript.GetWithPlayerAffinityGain` gives every companion passive affinity for
travelling with the player. Combined with the unconditioned Kellogg scene, that looked like a bug. Separately, if UCF loads
after Synthetic Love, her four custom affinity events are dropped (doc 02), which removes affinity changes rather than adding them.
