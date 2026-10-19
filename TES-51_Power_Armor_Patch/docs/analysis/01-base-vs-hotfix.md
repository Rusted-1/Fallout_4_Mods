# TES-51 Power Armor — analysis of the official 1.2 files

Files examined:
- `TES-51 Power Armor Update 1.2-17956-1-2\SkyrimInspiredPowerArmor.esp` (169,533 bytes) + loose assets
- `TES-51 PA Update 1.2 HOT FIX-17956-1-2HOTFIX\SkyrimInspiredPowerArmor.esp` (169,646 bytes)

## Plugin facts (both)
- Master: Fallout4.esm only. No AWKCR/AE dependency.
- HEDR form version 0.95. 993 records (base) / 994 (hotfix).
- Not ESL-flagged. FormIDs run up to `0100CB3D` — past the `0xFFF` ESL ceiling, so ESL needs FormID compaction first.
- Header NextObjectID = `0x3E0F` (base) / `0x45BD` (hotfix), but max used object ID is `0xCB3D`. **Header is wrong**; CK will reissue live FormIDs.

## What the hotfix actually changes
Exactly one functional change: adds `COBJ 010045BC co_Armor_Power_TES51_Helm2`, the crafting recipe for
`ARMO 01000FA5 Armor_Power_TES51_Helm2` ("TES-51 Helm Mk II"). Components match the Mk I helmet recipe
(`0001FABD` x7, `0001FA9C` x1, `0001FA91` x2).

The other 91 "changed" records are byte-order / serialization noise, verified sub-record by sub-record:
- MSWP material-swap pairs re-ordered (same content)
- FURN + REFR VMAD script properties re-ordered
- CELL `XCLR` region list reversed; `XCLC` unused land-flag bytes differ
- OMOD property structs: an unused scratch dword flips `0x00000218` -> `0x000001FD`

The hotfix is a **full replacement** of the 1.2 ESP (same filename), not an add-on. It only takes effect if it
overwrites the 1.2 plugin.

## Defects found (present in BOTH versions)
1. **Deleted vanilla reference** — `REFR 0016BDE6` carries the Deleted record flag (0x20) in
   `CELL 0000E116 BackBayCarDealershipExt`. Classic CTD source. Fix = undelete + disable (UDR).
2. **Probable ITMs** — full copies of `WRLD 0000003C Commonwealth`, `CELL 00018AA2` (Commonwealth persistent
   cell) and `FLST 0005F814 do_ModMenuSlotKeywordList` (15 LNAM entries, all vanilla, nothing mod-added).
   Confirm against Fallout4.esm, then clean.
3. **Previsibines** — the mod overrides `CELL 0000E116` keeping vanilla `VISI`/`RVIS`/`PCMB`/`XCRI` while
   deleting a ref inside it, and ships no regenerated previs/precombine meshes.
4. **NextObjectID wrong** (see above).
5. **Navmesh** — 4 NAVM (all in the mod's own interiors `01007382`, `0100AACA`) plus an override of
   `NAVI 00000FF1`.

## Assets
- Loose files only, no BA2.
- **No mipmaps** on any DDS checked (`mips=1`): `TES51_Body_d`, `TES51_Body_n`, `TES51_Helmet2_n`.
- **Normal maps compressed as DXT1/BC1** — wrong format for FO4 normals (should be BC5/ATI2, or BC7/DXT5).
- `TES51_Redux\TES51_Helmet2_n.dds` is 4096x4096 DXT1, no mips (8 MB).

## Verified clean
- All VMAD scripts referenced are vanilla (`DN054PaintJobCertificateScript`, `PowerArmorBatteryInsertScript`,
  `loadelevatordoorscript`). No missing custom scripts.
- Magazine scripts correctly point at the mod's own GLOBs/MESGs despite vanilla property names.
- `ONAM` correctly lists the overridden vanilla ref.

## Content inventory
7 ARMO (torso, 2 arms, 2 legs, Helm, Helm Mk II), 87 OMOD, 86 COBJ, 12 MSWP, 2 WEAP (steel sword, steel
warhammer), 2 INNR, 3 LSCR, 3 GLOB + 3 BOOK paint-job magazines, 1 LVLI, 2 custom interiors
(`000TES51BethesdaComics`, `000TES51BethesdaBasement`) with an elevator, 594 REFR.
