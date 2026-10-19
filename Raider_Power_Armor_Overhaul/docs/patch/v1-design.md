# v1.0 — Ladder design

Decisions: Raider < Scrapper < Raider T-45 < Brute. The Brute is built from a T-51 suit, so it sits
on top and gets a T-51 style upgrade path. No spawn gating. All three sets use the raider PA icon
in FIS.

## Per-piece stats (DR / ER / part HP)
| Set | Helm | Each limb | Torso | Set DR / ER / HP |
|---|---|---|---|---|
| Vanilla Raider (untouched) | 100 / 50 / 50 | 50 / 25 / 50 | 200 / 100 / 100 | 500 / 250 / 350 |
| Scrapper | 105 / 55 / 50 | 55 / 30 / 50 | 210 / 110 / 100 | 535 / 285 / 350 |
| Raider T-45 | 110 / 60 / 50 | 60 / 30 / 50 | 220 / 130 / 200 | 570 / 310 / 450 |
| Brute | 125 / 75 / 70 | 70 / 45 / 70 | 240 / 140 / 280 | 645 / 395 / 630 |

- Raider T-45 keeps its original DR and ER. Part HP was raised to match real T-45.
- Brute caps values: helm 80, limbs 120, torso 170. Weights unchanged on all sets.

## Set DR / ER at each upgrade step
| | base | b | c | d | e | f |
|---|---|---|---|---|---|---|
| Vanilla Raider | 500/250 | 620/250 | – | – | – | – |
| Scrapper | 535/285 | 655/285 | – | – | – | – |
| Raider T-45 | 570/310 | 690/430 | 810/550 | 930/670 | 1050/790 | 1170/910 |
| Brute | 645/395 | 765/515 | 885/635 | 1005/755 | 1125/875 | 1245/995 |
| Vanilla T-51 (ceiling) | 740/490 | 860/610 | 980/730 | 1100/850 | 1220/970 | 1340/1090 |

Each set beats the one below it at every step. The Brute stays under real T-51.

## Brute upgrade path
Lining OMODs copy the vanilla T-51 lining values for each part (Weight / Value multipliers, Health,
Rating, `dn_PowerArmor_Lining_X` keyword, dtEnergy). Recipes copy the vanilla T-51 lining
components and perk conditions.

| Lining | Name | Record |
|---|---|---|
| B | Welded Plate | Override of the Brute's own `PA_RaiderBrute_*_Lining_B`. Was +20 DR / +50 HP (torso +100), now T-51b style |
| C | Riveted Plate | New `RPA_PA_RaiderBrute_*_Lining_C` |
| D | Reinforced Plate | New, `_D` |
| E | Hardened Plate | New, `_E` |
| F | Rust King Plate | New, `_F` |

Each new lining has a loose mod MISC (`RPA_pa_comp_RaiderBrute_*`) and a COBJ
(`RPA_co_PA_RaiderBrute_*`). The new records use FormIDs 0x800–0x82F in `RPA_Fixes.esp`.

## FIS fix
- Brute and Scrapper ARMO overrides prefix the item name with `[PA_Raider]`.
- The Raider T-45 INNR override inserts a one-rule ruleset at the front:
  `[PA_Raider]` when the item has `dn_PowerArmor_T45`. VNAM is the rule count, so it is 1.

## Debug plugin
`RPA_Fixes - Debug Chem Station.esp`: 18 COBJs, one per piece. Workbench `WorkbenchChemlab`,
category `RecipeUtility`, no components, no conditions. Crafted pieces come out with the default
(lining A) template.

## Records in RPA_Fixes.esp
18 ARMO overrides, 4 OMOD overrides (Brute lining B), 16 new OMOD, 16 new MISC, 16 new COBJ,
1 INNR override. Masters: Fallout4.esm, DLCNukaWorld.esm, CWRaidPAT45.esp,
DesRustKing-RaiderBrutePowerArmor.esp, DesRivetsAndRage-AScrappyRaiderArmorPack.esp.
