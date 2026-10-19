# v5 — eight new armour tiers + FIS / FallUI tags (2026-10-17, FOMOD 1.1)

**Status: built and verified against the files. Not yet tested in game.**

## New tiers
Lining slot (ap 0x17DAA9), so a tier replaces Model F rather than stacking on it. Every tier is cloned from the base mod's own Lining F OMOD/MISC/COBJ for that piece type (Arm, Helmet, Leg, Torso). Stats are Model F + the user's bonus. Torso health is 4x limb (same ratio as B–F).

| Workbench name | DR | ER | Rad | HP limb/torso | Perks |
|---|---|---|---|---|---|
| Model F (existing) | 100 | 100 | – | 75 / 300 | Science 1, Armorer 4 |
| Model G: Iron Reinforcement | 120 | 105 | – | 90 / 360 | Science 1, Armorer 4, Scrapper 1 |
| Model H: Steel Reinforcement | 140 | 120 | 5 | 100 / 400 | Science 1, Armorer 4, Scrapper 2 |
| Model I: Bonemold | 150 | 125 | 10 | 105 / 420 | Science 1, Armorer 4, Scrapper 2, Medic 1 |
| Model J: Dwarven | 170 | 140 | 25 | 120 / 480 | Science 1, Armorer 4, Scrapper 2, Blacksmith 1 |
| Model K: Orcish | 175 | 150 | 20 | 130 / 520 | Science 1, Armorer 4, Scrapper 2, Blacksmith 2 (lower rad than Dwarven is intentional) |
| Model L: Ebony | 185 | 160 | 35 | 180 / 720 | Science 1, Armorer 4, Scrapper 2, Blacksmith 3 |
| Model M: Dragonplate | 190 | 165 | 45 | 195 / 780 | **Science 2**, Armorer 4, Scrapper 2, Blacksmith 3, Chemist 1 |
| Model N: Daedric | 205 | 180 | 75 | 275 / 1100 | **Science 2**, Armorer 4, Blacksmith 3, Nuclear Physicist 3 |

User decisions (2026-10-17):
- Blacksmith 3 applies to Ebony, Dragonplate and Daedric only; Dwarven B1, Orcish B2 stay.
- Nuclear Physicist 3 (vanilla max; the user first asked for 4).
- Science 1 kept on all tiers; Dragonplate and Daedric need Science 2.
- Daedric health = Dragonplate's +120 plus an extra 80 → +200 bonus (275 limb / 1100 torso total).
- No checkbox for the Torso Lining C fix.
- Upgrades must be listed in protection order in the workbench.

Other details:
- **Workbench order:** the workbench lists mods alphabetically by name (the user saw Bonemold, Daedric, Dragonplate, Dwarven, Ebony, Iron, Model A–F, Orcish, Steel). The tier OMOD names now continue the base mod's lettering — "Model G: Iron Reinforcement" … "Model N: Daedric" — so alphabetical order = protection order, straight after Model F. The armour piece names (INNR, e.g. "Ebony TES-51 Torso") are unchanged.
- Recipes: Model F recipe + 5 of every component (flat, same for all tiers).
- Weight/value: +5% per tier continuing A–F (Daedric +65%).
- Naming: tier keyword `dn_PowerArmor_TES51_Tier_<Name>` → INNR entry "<Name> TES-51" (e.g. "Ebony TES-51 Torso").
- Descriptions: the user's lore text, lightly spell-checked.
- 104 new records per variant (8 KYWD, 32 OMOD, 32 MISC, 32 COBJ) at 0x800–0x867. HEDR set to 1.0 in all variants. INNR override now present in every variant (Fixes Only copies the base INNR); ruleset VNAM counts rewritten correctly (the old legendary suffix ruleset said 3 but held 6).
- Perk FormIDs (Fallout4.esm): Science01 264D9, Science02 264DA, Armorer04 1797EA, Scrapper01 65E65, Scrapper02 1D2483, Medic01 4C926, Blacksmith01 4B253, Blacksmith02 4B26A, Blacksmith03 264D8, Chemist01 E36FF, NuclearPhysicist03 1D2471.

## Brahmin's Endurance — carry weight replaced by health regen (Unique Legendaries only)
- Removed the +20 CarryWeight (AV 0x2DC) property from both arm trophies (PA_TES51_Arm_Misc_TrophyL/R). END +2, LCK +1 and the two Bolstering enchantments (ResistancesInverseHealth DR/ER) are unchanged.
- Added new ENCH `ench_TES51_Legendary_BrahminRegen` (0x868 in the patch): one effect, vanilla `abRestoreHealth` (0x1504F1, constant value-modifier on Health — the effect behind `MS09JackHealthRegen`) at 5/3 = 1.667 HP/s, i.e. 5 health every 3 seconds, applied smoothly rather than in pulses.
- Chosen over HealRate (Life Giver 3's mechanism) because `fCombatHealthRegenRateMult` = 0 in Fallout4.esm: HealRate regen stops in combat. abRestoreHealth doesn't.
- Not yet checked in game: whether wearing Brahmin's on both arms doubles the regen (two enchanted items, likely stacks to 10 HP / 3 s).
- Vanilla has no health-regen armour legendary; the user picked it from the list of available effects.

## Build pipeline (in the working container)
`build_tiers.py` (base + v1.0 patch → patch with tiers) → `brahmin_regen.py` (Unique Legendaries variants only) → `build_addons.py fis` (FIS add-ons from the built patch). Always rebuild from the v1.0 originals; `brahmin_regen.py` refuses to run twice on the same file.

## FIS / FallUI
Pieces already carry ArmorTypePower, but FIS tags power armour via the vanilla dn_PowerArmor INNR; TES-51 uses dn_PowerArmor_TES51_INNR. `TES51_FIS.esp` (ESL-flagged, masters Fallout4 + base + TES51_Patch.esp) overrides the TES-51 INNR with an unconditional "[PowerArmor]" ruleset first — same convention as FIS's own static-sorting plugin. 4 variants (ESL/ESP × Fixes/Legendaries), chosen by the FOMOD. Optional; without FIS the tag shows as text.

## Torso Lining C
Already fixed (60 → 120) by the core patch since v1 — the base mod still has the bug. No separate option (user confirmed).

## Backup
Previous v1.0 plugins / fomod / README: `C:\Nu-uh\Fallout_4_TES_Power_Armor\TES-51 Patch FOMOD v1.0 backup\`.

## Compatibility checked
MPAM patch's standard-lining overrides keep slot 0x17DAA9, so the new tiers attach with MPAM installed.
