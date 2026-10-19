# v5b — Kat's Power Armor Repair Kits patch (2026-10-18)

**Status: built and verified against the files. Not yet tested in game.**

## Project folder moved (2026-10-19)
The user moved the project folder from `C:\Nu-uh\Fallout_4_TES_Power_Armor\` to **`C:\My very own mods\Fallout_4_TES_Power_Armor\`**. FOMOD source is now `C:\My very own mods\Fallout_4_TES_Power_Armor\TES-51 Patch FOMOD\`. All 17 plugin/installer/README files there were byte-compared against the build after the move: identical. Older docs that cite `C:\Nu-uh\...` refer to the same files at the old location.

Optional FOMOD component "Kat's Power Armor Repair Kits patch" (flag `kat`), auto-Recommended when `Some_Assembly_Required_Repair_Kits.esp` is active. Folders `Patch - Kat's Repair Kits` (ESL base) and `Patch (ESP) - Kat's Repair Kits` (ESP base), picked by the Base Plugin answer.

## How Kat's works
Fallout 4 repairs a power armour piece using the components of that piece's `co_Armor_Power_*` COBJ (no workbench keyword = repair recipe). Kat's overrides those to cost 1 repair kit (torso 2) and adds a kit MISC + chem-station recipe per armour type. Per-armour add-ons (e.g. `SAR_Repair_Kits_T65.esp`) follow the same pattern.

## SAR_Repair_Kits_TES51.esp
- ESL-flagged, 9 records. Masters: Fallout4.esm, Some_Assembly_Required_Repair_Kits.esp, SkyrimInspiredPowerArmor.esl/.esp.
- New MISC `kat_misc_tes51repairkit` "TES-51 Repair Kit" (clone of Kat's T-60 kit, DLC01 robot repair kit model).
- New COBJ `kat_co_misc_tes51repairkit`: chemistry station, category kat_key_repairkits ("REPAIR KITS"), 10 Steel, 2 Circuitry, 2 Adhesive, 2 Gears, 2 Screws; Science! 1 + Armorer 2 (same as Kat's T-60 kit).
- Overrides the 7 TES-51 repair recipes (co_Armor_Power_TES51_ArmLeft/ArmRight/Helm/Helm2/LegLeft/LegRight/Torso): 1 kit each, torso 2. Original cost was 7 Steel, 1 (0x1FA9C), 2 (0x1FA91); torso 10 Steel, 6, 2.
- No other option in the FOMOD touches these COBJs; the Debug option's chem-station recipes are separate new records.

## Build note
Copied base COBJs needed their CNAM remapped from master index 01 (the base, in its own file) to index 02 (the base's slot in this plugin, where 01 is Kat's). First build missed this — caught by the reference check before shipping.

## Installer change
"Base Plugin" step is now visible when Plugin Fixes, the MPAM patch or the Kat's patch is ticked (it was Plugin Fixes only, so ticking MPAM alone gave no base choice and installed nothing for it).
