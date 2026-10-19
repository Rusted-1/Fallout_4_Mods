VULPINE RACE - HUMAN NATE PATCH
================================

WHAT IT DOES
------------
Vulpine Race's "VulpinePlayer.esp" points three character records at the
Vulpine race:

    Player                    <- your character
    MQ101PlayerSpouseMale     <- Nate, when you play as Nora
    MQ101PlayerSpouseFemale   <- Nora, when you play as Nate

This patch overrides ONE of those records -- "Player" -- and sends it back
to the vanilla HumanRace. Every other record is left exactly as Vulpine
Race shipped it.

Result when you play as Nate:
    Nate (you)  = human
    Nora (NPC in the pre-war intro) = Vulpine, untouched


INSTALLING WITH VORTEX
----------------------
1. In Vortex, go to the Mods tab.
2. Drag this .zip onto the drop area, or use "Install From File".
3. Click Enable once it appears in the list.
4. Let Vortex deploy.

Load order sorts itself. The patch declares VulpinePlayer.esp as a master,
so the game and LOOT will always place it after Vulpine Race. You do not
need to drag anything manually.

The plugin is ESL-flagged, so it does not consume one of your 255 regular
plugin slots.


TURNING IT OFF
--------------
Fallout 4 has no race selector in the character creation mirror -- race is
locked by the Player record. So this is not an in-game toggle. The plugin
itself is the switch:

    enabled  = human Nate
    disabled = Vulpine Nate


IMPORTANT: START A NEW GAME
---------------------------
Change the player's race on an existing save and Fallout 4 tends to mangle
the head mesh -- you get an invisible or distorted face that is a pain to
fix. Install this before starting a new character.


REQUIREMENTS
------------
Fallout 4, Vulpine Race V5.1 (VulpineRace.esm + VulpinePlayer.esp).


A NOTE ON THE ROBO LEG MOD
--------------------------
The old Xbox trick was not doing what it looked like. Eli's Robo Leg
Outfits contains no override records at all -- only new outfits, armor
addons and recipes. It never touches race or the player, so load order
could not have made it override Vulpine at the plugin level. What it does
ship is a replacement PlayerCharacterAssets\MaleBody.nif, and that asset
collision is the likeliest cause of what you saw. You do not need the Robo
Leg mod installed for this patch to work, and this patch does not interfere
with it if you do want the outfits.
