# 02 — The Robo Leg mod was a red herring

Years ago on Xbox, loading *Eli's Robo Leg Outfits* after Vulpine Race appeared to make
the male player human again. The same trick never worked on PC. The working hypothesis
was that the outfit mod contained a script or a conflicting record that reverted the male
player. Parsing the plugin disproved it.

## Eli_Robo Leg Outfits.esp contains zero override records

Every record in it carries a FormID in the plugin's own index space — they are all
brand-new forms, nothing with master index `00`:

| Record type | Count |
|---|---|
| ARMO | 12 |
| ARMA | 12 |
| COBJ | 12 |
| FLST | 2 |
| KYWD | 1 |
| ENCH | 1 |
| CONT | 1 |

It has **no NPC_ records and no RACE records**, and it never references the player. At
the plugin level it is structurally incapable of overriding Vulpine Race, no matter where
it sits in the load order.

Reproduce with:

```
python3 -I tools/esp.py "<path>/Eli_Robo Leg Outfits.esp"
```

## What it does ship

Inside its `Main.ba2`, replacement body meshes at
`Meshes\Actors\Character\PlayerCharacterAssets\MaleBody.nif` and `FemaleBody.nif`.

Fallout 4 keeps player body assets in `PlayerCharacterAssets` separately from the NPC
assets in `CharacterAssets`. An asset-level collision along those lines is the most
plausible explanation for the effect seen on Xbox.

## Conclusion

Incidental asset collision, not a designed override, and not worth reproducing. It would
be fragile, and it could never have cleanly separated Nate from Nora anyway.

The Robo Leg mod is **not required** for this patch, and the patch does not conflict with
it if the outfits are wanted.
