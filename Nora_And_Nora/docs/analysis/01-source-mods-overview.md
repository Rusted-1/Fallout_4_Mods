# 01 — How each Nora works

## Nora Spouse Companion 1.2 (House Variable) — the human Nora
- `NoraSpouse.esm` (ESM, masters only `Fallout4.esm`) + `NoraSpouse - Main.ba2` (BA2 v1, 92 scripts, ~950 voice files).
- Story: Nora's cryo pod was empty, she survived. Recruitment quest **"O Spouse, Where Art Thou?"** (`COMNoraFirstMeet`) starts when you head towards Sanctuary; she is found at **Abernathy Farm**.
- Companion NPC `NoraComp` (`01000F9A`), voice type `PlayerVoiceFemale01`, race Human.
- Overrides the vanilla Vault 111 dialogue quest (`DialogueVault111`) and edits the female spouse corpse NPC (`MQ102PlayerSpouseCorpseFemale`, `00026F36`): the readme says it **disables Nora's corpse in Vault 111**.
- Its own affinity quest (`COMNoraAffinityQuest`), relationship scenes, perk "Till Death Do Us Part", end-game dialogue for all factions, interjections in ~45 vanilla quests.

## Synthetic Love (Thrillvilled) — the synth Nora
- `p865_SyntheticLove.esp` + `p865_SyntheticLove - Main.ba2` (**BA2 v8**, Next-Gen format; 9 scripts, ~800 voice files).
- 8 installer versions (Next Gen / Automatron / Far Harbor / Nuka-World loadout, each with or without "Prevent Armor Damage"). DLC versions add the DLC as a master, which shifts the plugin's own index from 01 to 02, but the **object IDs and Editor IDs of all 1,376 records are identical** across all 8 versions.
- Story: found in **Diamond City**, insists she is "human as the day I was born". Quest **"Cold Comfort"** (`p865_COMNoraQuest01`): "Travel with Nora to Vault 111 and examine the corpse", which references the corpse NPC `00026F36`.
- Companion NPC `p865_CompanionNora` (`xx000F99`), voice type `PlayerVoiceFemale01`, uses the vanilla `CompanionActorScript` threshold system, with custom thresholds (Friend, Confidant) and a romance scene.

## Overlaps that matter for the patch
- **Vault 111 corpse:** Nora Spouse removes the body that Cold Comfort sends you to examine. The design replaces that beat: with the real Nora alive and travelling with you, she is the proof (see `notes/interaction-ideas.md`).
- **Synthetic Love's intro assumes Nate is a widower** ("This can't be happening. My wife died."). Needs a conditioned alternative when Nora Spouse's Nora is already recruited.
- **Same voice type:** both use `PlayerVoiceFemale01`, so vanilla female-player recordings can be reused for either, and every new line must be conditioned on the speaker.
- **Same face:** both copy the customised character-creation Nora.
