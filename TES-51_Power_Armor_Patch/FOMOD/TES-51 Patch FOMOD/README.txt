TES-51 Power Armor - Fix Patch  (FOMOD)
=======================================
Install by dragging the ZIP onto Vortex's Mods screen. The installer asks three
questions.

REQUIREMENTS
------------
  Fallout4.esm
  SkyrimInspiredPowerArmor.esl    <- 4estGimp's ESL conversion, Nexus 85030

  The original mod and its 1.2 Update must also be installed for meshes and
  materials, even with their .esp disabled.

  ENABLE ONLY ONE of SkyrimInspiredPowerArmor.esl and .esp. With both enabled
  the game loads two complete copies of the mod - two sets of armour, two shops,
  and two map markers:

      .esl marker  01000A24
      .esp marker  0100A31B

  These are separate records in separate plugins. The patch fixes whichever one
  you chose at install time; it cannot reach the other. Disable the one you
  are not using in Vortex's PLUGINS tab (not the Mods tab - the mod's meshes and
  textures must stay installed either way).

  The .esl is recommended: light-flagged, and it already removes a deleted
  vanilla reference and an identical-to-master edit that the .esp still has.

  Do NOT install the third-party "Update 1.3" file. It is a byte-for-byte copy
  of the 1.2 Update plugin and fixes nothing.

INSTALLER OPTIONS
-----------------
Step 1  Components
          Plugin Fixes  - the patch plugin (ESL-flagged, costs no load slot)
          Textures      - re-encoded textures, must overwrite the TES-51 mod
          MPAM patch    - TES-51 / More Power Armour Mods compatibility,
                          auto-recommended if More Power Armour Mods.esp is active
          FIS / FallUI  - tags every TES-51 piece as power armour for FIS
                          (needs Plugin Fixes; only tick it if FIS is installed)
          Kat's kits    - TES-51 patch for Kat's Power Armor Repair Kits,
                          auto-recommended if Some_Assembly_Required_Repair_Kits.esp
                          is active

Step 2  Base Plugin           (only if Plugin Fixes was ticked)
          Which TES-51 plugin you actually run - 4estGimp's .esl or the
          original .esp. ONLY ONE OF THEM MAY BE ENABLED.

          There is a separate map marker inside each plugin. A patch built
          for one cannot touch the other's, so with both enabled the shop
          keeps appearing on the map no matter what. This choice also picks
          the matching More Power Armour Mods patch.

Step 3  Trophy Effects        (only if Plugin Fixes was ticked)
          Unique Legendaries  - six distinct named legendaries
          Original Tiered     - keeps the ladder, fixes the bug only

Step 4  Debug                 (only if Plugin Fixes was ticked)
          Chemistry station recipes - all seven armour pieces and all eight
          trophy items, one Steel each, under the UTILITY tab

LOAD ORDER
----------
None needed. TES51_Patch.esp masters SkyrimInspiredPowerArmor.esl, so it always
loads after it, and TES51_FIS.esp masters TES51_Patch.esp, so it always loads
after that. The Textures component must win its file conflict against the
TES-51 Power Armor mod - Vortex will ask.


WHAT THE PLUGIN FIXES
=====================
MAP MARKER
  "Bethesda Comics" had its map marker flagged Visible and Can Travel To, so it
  appeared on the Pip-Boy the moment you left the vault and could be fast
  travelled to before you found it. Now starts undiscovered.
  The location record also pointed at an unrelated vanilla map marker. Fixed.

TROPHIES
  All six granted nothing at all. Fallout 4 wires power armour bonuses two ways:
  paint jobs set a PA_<Special>_AV value plus a matching enchantment that reads
  it, while direct upgrades use the raw SPECIAL actor value with no enchantment.
  The trophies had been copied from a paint job - they set the paint values with
  no enchantment attached, so nothing in the game ever read them.

TORSO LINING MODEL C
  Gave Health +60, the same as Model B. The series is 60/60/180/240/300 - C was
  left at B's value. Now +120.

HOT ROD FLAMES PAINT
  Accumulated its strength value at +2 per piece where every vanilla paint uses
  +1, so it hit the "all pieces painted" threshold after only three. Now +1.

NAMING - 38 loose items
  Each loose upgrade item now carries the name of the upgrade it installs.
  Previously "TES-51 Core Assembly" installed "Adrenaline Boost", "TES-51
  Targeting HUD" installed "Detect Life", and "TES-51 Sun Regen Mod" was a
  leftover developer placeholder.

TEXT
  Six missing upgrade descriptions written. One grammar fix.
  One stray property removed from the "No Upgrade" steel sword mod.


UNIQUE LEGENDARIES (optional)
=============================
Each trophy becomes a distinct choice rather than a rung on a ladder, and the
armour piece is renamed to match - "TES-51 Left Arm of Brahmin's Endurance".

  Brahmin's Endurance      arms    END +2, LCK +1, regenerates 5 health every
                                   3 seconds (works in combat), Damage and Energy
                                   Resistance rise as health drops
  Hunter's Calling         arms    STR +2, CHA +1, reflects some melee damage,
                                   15% less damage from ghouls, super mutants, animals
  Yao Guai's Gaze          helmet  STR +2, PER +1, less damage standing still,
                                   faster Action Point regeneration
  Deathclaw's Persistence  helmet  AGI +2, STR +1, less damage sprinting,
                                   sprinting costs fewer Action Points
  Forsworn's Rejection     helmet  PER +2, STR +1, CHA -1,
                                   15% less damage from humans and robots
  Briarheart's Denial      torso   AGI +2, END +1, CHA -1, chameleon,
                                   time slows when health runs low

Every effect is a stock Fallout 4 legendary effect or actor value, except
Brahmin's health regeneration. Fallout 4 has no regeneration legendary, so it
uses the game's own constant restore-health effect (the one behind Jack
Cabot's regeneration) at 5/3 health per second. It heals smoothly rather than
in 3-second pulses, and unlike Life Giver's regen it keeps working in combat.

Wearing the same arm trophy on both arms is allowed and stacks the SPECIAL
bonuses. The legendary effects themselves are on/off switches and will not
double.

NEEDS TESTING
  No vanilla item sets more than one creature-type damage reduction at a time.
  Hunter's Calling sets three and Forsworn's Rejection sets two. The shared perk
  should evaluate each independently, but that cannot be proven from the files -
  only in game. If one of them turns out not to apply, that is the reason.


NEW ARMOUR TIERS
================
Eight new linings above Model F, so the armour keeps up late game. Models A-F
are untouched. Each new tier goes in the same lining slot as A-F, so a piece
wears one lining at a time: a new tier replaces Model F, it does not stack on
top of it.

Every tier is Model F plus the bonus below. Health is per arm, leg and helmet;
the torso gets four times that, the same ratio Models B-F use.

                      Damage  Energy  Rad   Health        Perks (plus Science! 1)
  Model F (existing)   +100    +100     -    +75 / +300   Armorer 4
  Iron Reinforcement   +120    +105     -    +90 / +360   Armorer 4, Scrapper 1
  Steel Reinforcement  +140    +120    +5   +100 / +400   Armorer 4, Scrapper 2
  Bonemold             +150    +125   +10   +105 / +420   Armorer 4, Scrapper 2, Medic 1
  Dwarven              +170    +140   +25   +120 / +480   Armorer 4, Scrapper 2, Blacksmith 1
  Orcish               +175    +150   +20   +130 / +520   Armorer 4, Scrapper 2, Blacksmith 2
  Ebony                +185    +160   +35   +180 / +720   Armorer 4, Scrapper 2, Blacksmith 3
  Dragonplate          +190    +165   +45   +195 / +780   Armorer 4, Scrapper 2, Blacksmith 3, Chemist 1 *
  Daedric              +205    +180   +75   +275 / +1100  Armorer 4, Blacksmith 3, Nuclear Physicist 3 *

  * Dragonplate and Daedric need Science! 2 instead of Science! 1.

In the workbench they are named Model G to Model N ("Model G: Iron
Reinforcement" ... "Model N: Daedric"). The workbench lists upgrades in
alphabetical order, so the letters keep them in protection order straight
after Model F.

Every recipe costs the Model F recipe for that piece plus 5 of each component.
Weight and value carry on the Model A-F step of +5% per tier (Daedric +65%).

The armour is renamed to match - "Ebony TES-51 Torso", "Daedric TES-51 Left
Arm of Hunter's Calling" - and each tier carries its own workbench description.

Built from vanilla records only: each tier is a copy of the mod's own Model F
lining with new numbers, so it uses the same slot, filter keywords and loose
mod model.


FIS / FALLUI (optional)
=======================
For FIS - The NEW FallUI Item Sorter (Nexus 60580) and FallUI - Icon Library
(Nexus 60579).

Every TES-51 piece already carries the vanilla ArmorTypePower keyword, but FIS
tags power armour through vanilla's dn_PowerArmor naming rule, and TES-51 uses
its own (dn_PowerArmor_TES51_INNR). So FIS never tagged it.

TES51_FIS.esp adds the "[PowerArmor]" tag at the front of TES-51's naming
rule, the same way FIS's own static-sorting plugin does it for vanilla power
armour. FallUI reads the tag and files the pieces under power armour.

The FOMOD picks the right copy for your base plugin and trophy choice - it
carries the full naming rule, so it must match the main patch.

Without FIS the tag shows up as plain text in the name. Don't tick it unless
FIS is installed.


MORE POWER ARMOUR MODS PATCH (optional)
=======================================
The old TES-51-MPAM.esp was built against SkyrimInspiredPowerArmor.ESP. You are
now running 4estGimp's .ESL, in which most FormIDs were renumbered during the
ESL compaction - so the old patch pointed at the wrong records, or at nothing.

It has been rebuilt against the .esl. Every TES-51 reference was remapped by
EditorID and then verified: all 49 structural references resolve to exactly the
same records they did before, with no mismatches and nothing left dangling.

  Masters   Fallout4.esm, More Power Armour Mods.esp, SkyrimInspiredPowerArmor.esl
  88 records, ESL-flagged (highest new object id 0xE36, inside the light range)
  12 overrides of TES-51 records - the six armour pieces and six standard linings
  76 new records - 25 slot-two utility mods with their items and recipes

It does not touch the trophies, so it is independent of the Trophy Effects
choice above. It shares no records with the main patch either.

Note: the slot-two copies keep their original names ("TES Core Assembly",
"TES Targeting HUD"). Those do not match the corrected names the main patch
gives the slot-one versions. That was left alone deliberately - the differing
names may be what tells the two slots apart in the workbench menu.


KAT'S POWER ARMOR REPAIR KITS PATCH (optional)
==============================================
For Kat's Power Armor Repair Kits (Nexus 53558). Built the same way as Kat's
own per-armour add-ons:

  TES-51 Repair Kit   crafted at a chemistry station, REPAIR KITS category,
                      same cost and perks as Kat's T-60 kit (Science! 1,
                      Armorer 2): 10 Steel, 2 Circuitry, 2 Adhesive,
                      2 Gears, 2 Screws - Kat's recipe, unchanged
  Repairs             every TES-51 piece now repairs with 1 kit, the torso with
                      2 - all seven pieces including the Helm Mk II

  Plugin    SAR_Repair_Kits_TES51.esp (ESL-flagged)
  Masters   Fallout4.esm, Some_Assembly_Required_Repair_Kits.esp,
            SkyrimInspiredPowerArmor.esl (or .esp - chosen from your base plugin)

It only touches the seven TES-51 repair recipes, which nothing else in this
FOMOD edits, so it is independent of every other option.


TECHNICAL
=========
  Masters      Fallout4.esm, SkyrimInspiredPowerArmor.esl
  ESL-flagged  yes - all new records sit in 0x001-0xFFF, so no load order slot
  New records  104 for the new tiers (8 keywords, 32 linings, 32 loose mods,
               32 recipes), 6 keywords (Unique Legendaries), 15 recipes (Debug)
  Overrides    the TES-51 naming rule, in every variant, to name the new tiers

  The plugin carries the Commonwealth worldspace and persistent cell records.
  It does not modify either - they are copied byte for byte from the ESL and are
  only present because the file format requires them as the structural parents
  of the map marker.

  Nothing here touches previsibines. PRP compatible; also fine without PRP.
