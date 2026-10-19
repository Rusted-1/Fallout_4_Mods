# v6 (planned) — optional "Enchantments" slot

**Status: planning only. Nothing built yet.** Waiting on the user's list of enchantments.

## What the user wants (2026-10-17)
- A third mod slot on every TES-51 piece, called **Enchantments**, as an **optional FOMOD checkbox**.
- Each enchantment is a unique effect that becomes craftable **once a specific quest is completed**.
- **Helm Mk II** gets both the MPAM second slot and the new Enchantments slot, matching the regular helm.
- The effects are the user's own designs. Recharging Shields System (Nexus 66803) was shared **only as inspiration** for the kind of special effects wanted — the shield system itself is not wanted, and nothing is to be copied from it.

## Reference: the inspiration effects (Recharging Shields System's unique shields)
Nova (nuke on shield break), Reinforcements (summon allies), Stealth Field (15 s), Adrenaline Rush (2x melee, +15% move/reload), Bullet Absorb (80% chance). There, they fire on "shield break"; without a shield the proposed trigger is a health threshold (suggested 50%).

## Technical notes
- **Quest gating needs no scripts:** recipe (COBJ) conditions such as GetQuestCompleted / GetStageDone, the same mechanism as the perk-gated tiers.
- **No script needed:** stat/resistance/damage effects, health-threshold conditions, chance-based damage negation, stealth field while condition holds, and perk-based effects (MGEF "perk to apply", as vanilla's LegendaryAddCommonPerk does).
- **Needs Papyrus:** one-shot triggers with cooldown (explosion, summoning allies), timed effects (e.g. exactly 15 s). Scripts can be written here, but the user must compile them on their PC with the Creation Kit.
- The new slot overrides the same standard-lining OMODs as the MPAM patch, so it needs with-MPAM and without-MPAM builds.
- Slot layout today: slot 1 = TES-51 utilities + trophies (ap 0x17DAA7); slot 2 (MPAM) = 25 MPAM generic utilities ("TES Jet Pack", "TES Tesla Coils" …), Helm Mk II not covered yet.

## Needed from the user
Per enchantment: name, effect, which piece (or any), unlocking quest (and stage if specific), plus the trigger threshold choice.
