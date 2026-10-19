# 01 — How Vulpine Race applies the transformation

Findings from reading Vulpine Race V5.1's own plugins. No Creation Kit or xEdit was
available, so both files were parsed straight from their binary form with
`tools/esp.py`.

## VulpineRace.esm — record census

| Record type | Count | What it is |
|---|---|---|
| CLFM | 262 | Colour forms (fur / eye colour options) |
| HDPT | 222 | Head parts — muzzles, ears, hair, eyes |
| TXST | 77 | Texture sets |
| NPC_ | 22 | Sample / preset characters |
| ARMA | 6 | Armor addons — the actual body and skin geometry |
| ARMO | 2 | Armor wrappers for the skin |
| RACE | 1 | `VulpineRace`, FormID `01000F99` |
| MGEF / SPEL / FLST | 1 each | Supporting forms |

Author string on the plugins: `BeardOfSocrates and RussianPrince`.

### There is exactly one RACE record

It is **not** split into male and female variants. Sex differences are handled *inside*
that single race, via separate male/female mesh and material slots. This is the reason a
per-sex toggle is impossible with static records alone — see
[`../patch/v1-design.md`](../patch/v1-design.md).

### Vulpine ships no body mesh of its own

Its skin ARMA points at the stock vanilla paths
`Actors\Character\CharacterAssets\MaleBody.nif` and `FemaleBody.nif`, and gets the fox
look purely from custom textures and materials layered on top.

### There are no Papyrus scripts anywhere in the mod

Nothing runs at game time. Everything is static plugin data, which rules out any runtime
sex-check approach inside the mod itself.

## VulpinePlayer.esp — where the race gets attached

A tiny ESL-flagged plugin. It overrides exactly three NPC_ records, and all three point
their RNAM (race) field at the same Vulpine race form:

| FormID | Editor ID | RNAM | Who this is |
|---|---|---|---|
| `00000007` | `Player` | `01000F99` | The player character — both sexes share it |
| `000A7D34` | `MQ101PlayerSpouseMale` | `01000F99` | Nate as an NPC (only if you play Nora) |
| `000A7D35` | `MQ101PlayerSpouseFemale` | `01000F99` | Nora as an NPC (only if you play Nate) |

Masters: `Fallout4.esm`, `VulpineRace.esm`.

One useful detail: on the Player record the `ATKR` (attack race) field was left at
`00013746` — vanilla HumanRace. That confirmed the FormID to revert to without needing a
copy of `Fallout4.esm` on hand.

## Why this makes the fix easy for a Nate playthrough

Playing as Nate, the player character is the `Player` record and Nora in the intro is
`MQ101PlayerSpouseFemale` — a completely separate record. Reverting the first and leaving
the second alone gives exactly the desired split.
