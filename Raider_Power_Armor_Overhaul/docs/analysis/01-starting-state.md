# 01 — Starting state of the three mods

Read from the plugins on 2026-10-17, compared against vanilla `Fallout4.esm`.

## Plugins
| Mod | Plugin | Masters | Notes |
|---|---|---|---|
| CW Raider T-45 1.0.1 | `CWRaidPAT45.esp` (ESL-flagged) | Fallout4.esm | Own INNR `00RaidT45PAdn_PowerArmor` (copy of vanilla `dn_PowerArmor` with "Raider T-45" text) |
| Rust King - Brute PA 1.1 | `DesRustKing-RaiderBrutePowerArmor.esp` (ESL-flagged) | Fallout4.esm, DLCNukaWorld.esm | Also adds a location, the ghoul boss Lonnie, notes and holotapes |
| Rivets And Rage 1.10 | `DesRivetsAndRage-AScrappyRaiderArmorPack.esp` (ESL-flagged) | Fallout4.esm, DLCNukaWorld.esm | Also adds regular raider armor, helmets and masks |

Rust King and Rivets And Rage are by the same author. Their power armor records use the same
layout and the same internal FormIDs.

## Base stats before the patch (full set: helm + torso + 4 limbs)
| Set | DR | ER | RR | Part HP | Weight | Best upgrade (max set DR) |
|---|---|---|---|---|---|---|
| Vanilla Raider | 500 | 250 | 1050 | 350 | 102 | Raider II lining (620) |
| Scrapper | 500 | 285 | 1050 | 350 | 102 | Welded Plate (620) |
| Brute | 500 | 285 | 1050 | 350 | 102 | Welded Plate (620) |
| Raider T-45 | 570 | 310 | 1050 | 380 | 92 | All vanilla T-45 linings b–f (1170) |
| Vanilla T-45 (ref) | 500 | 310 | 1050 | 450 | 92 | T-45f (1100) |
| Vanilla T-51 (ref) | 740 | 490 | 1050 | 680 | 92 | T-51f (1340) |

Findings:
- Scrapper and Brute were clones of vanilla raider PA (+5 ER per piece).
- Raider T-45 carries `ma_PA_T45`, so it takes every vanilla T-45 mod, including all linings and the
  jet pack. At T-45f it beat real T-45f.
- All three are injected by script into the vanilla raider PA leveled lists with no level gating.
  CW injects per piece into `LL_Armor_Power_Raider_*`. Rust King and Rivets And Rage inject their
  set list into `LLI_Armor_Power_Raider`.

## FIS / FallUI icons
The installed FIS is the static-sorting version (`FIS-Naming-Weap-Armo-EN.esp`). It tags vanilla
power armor by inserting a `[PA_Raider]` / `[T45]` / … ruleset at the front of the vanilla
`dn_PowerArmor` INNR.

None of the three mods uses vanilla `dn_PowerArmor`:
- Brute and Scrapper have no INRD at all, so FallUI fell back to name matching in
  `AutoTags_en.ini`. "Raider Brute Power …" matched `Raider=[SetRaider]` (the regular raider armor
  icon) and "Scrapper Power …" matched `Power=[PowerArmor]` (the generic PA head).
- Raider T-45 uses its own INNR, so FIS never tags it. Its names contain "T-45" and pick up `[T45]`.

The FIS readme does not allow modifying or redistributing FIS files. The fix therefore lives only
in my own plugin.
