# v1.0 — design and changelog

## Goal

Play as Nate with a human Sole Survivor, while Vulpine Race keeps working everywhere
else — in particular Nora in the pre-war intro must stay Vulpine and completely
untouched. The fix had to be a small standalone plugin installable through Vortex, not a
rewrite or a repack of the original mod.

## What the patch changes

| Record | Before | After |
|---|---|---|
| `Player` (`00000007`) | RNAM = `01000F99` (VulpineRace) | RNAM = `00013746` (HumanRace) |
| `MQ101PlayerSpouseFemale` (`000A7D35`) | RNAM = `01000F99` | not touched |
| `MQ101PlayerSpouseMale` (`000A7D34`) | RNAM = `01000F99` | not touched |

That is the whole diff: **one 4-byte field in one record.**

The Player record is lifted out of `VulpinePlayer.esp` byte for byte and only the RNAM
value is rewritten, so every other property Vulpine set — perks, keywords, hair colour,
default outfit, voice type, template flags — is preserved identically. No Vulpine record
is modified, removed or reordered. `tools/verify.py` asserts this with a subrecord-level
diff against the source plugin.

## Plugin properties

| Property | Value | Why |
|---|---|---|
| Filename | `VulpineNateHuman.esp` | |
| Masters | `Fallout4.esm`, `VulpineRace.esm`, `VulpinePlayer.esp` | Mastering `VulpinePlayer.esp` forces the game and LOOT to load the patch after it. No manual load-order dragging needed |
| TES4 flags | `0x00000200` (ESL / light) | Override-only plugin, so light-flagging is safe. Does not consume one of the 255 regular plugin slots |
| Record compression | cleared | The source record was zlib-compressed; the patch writes it plain. Functionally identical, easier to inspect |

## Design notes and limits

**There is no in-game race toggle.** Fallout 4, unlike Skyrim, has no race selector in the
character creation mirror — it offers male or female only, and race is locked by the
Player record. So this is not something flipped in-game. The plugin *is* the switch:
enabled means human player, disabled means Vulpine player.

**Both sexes are affected.** Male and female share the single `Player` record, so the patch
makes the player human whichever sex is chosen at the mirror. That is fine for a Nate
playthrough, but a Vulpine *player* Nora would mean disabling the patch for that save.

**A true per-sex split is not achievable with static records.** It would need a Papyrus
script on a startup quest reading `Game.GetPlayer().GetActorBase().GetSex()` and calling a
race swap — feasible, but a different build, and it needs the Creation Kit or a compiler.

**LooksMenu skin.** Vulpine's F4EE skin definition is keyed to `VulpineRace.esm`, so it
simply will not apply to a HumanRace player. No cleanup needed.

**Start a new game.** Changing the player's race on an existing save is a well-known way to
corrupt the head mesh in Fallout 4 — invisible or scrambled faces that are unpleasant to
repair.

## Status

Built and verified at the file level; `tools/verify.py` passes all checks. **Not yet
confirmed in game** — see the README for what to check on the first run.
