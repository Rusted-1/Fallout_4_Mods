# TES-51 — defect list mapped to Austin's requested fixes

Source: `TES-51 PA Update 1.2 HOT FIX` plugin (the best base to patch from).

---

## 1. Location visible / fast-travelable from game start

**Root cause found.** `REFR 0100A31B` — the "Bethesda Comics" map marker, in the Commonwealth
persistent cell.

```
NAME  = 00000010  (MapMarker)
XMRK  = (present)
FNAM  = 03        <-- bit0 Visible + bit1 Can Travel To
FULL  = "Bethesda Comics"
TNAM  = 38 00     (marker type)
XLKR  = 00000000 / 0100A31C
XLRL  = 00002CF0  (vanilla Commonwealth location)
```

**Fix:** `FNAM` = `00`. Marker then starts undiscovered and is discovered by proximity like any vanilla
location.

**Two related linkage oddities to verify against a vanilla marker:**
- `LCTN 01008470 TES51_BethesdaComicsLocation` has `MNAM = 000A8C6D` — a *vanilla* reference, not the
  mod's own marker `0100A31B`. Looks like leftover from whatever location record was duplicated.
- The marker's `XLRL` points at `00002CF0` (Commonwealth) rather than `01008470`.

The interior cell itself is wired correctly: `CELL 01007382` has `XLCN = 01008470`, `XEZN = 01008471`.

---

## 2. Upgrades that do not apply their effects

Decoded all 87 OMOD property blocks. Property indices used: 0 Enchantments, 3 Keywords, 4 Weight,
5 Value, 6 Rating, 9 DamageTypeValues, 10 actor-value modifier, 11 Health, 12 ColorRemappingIndex,
13 MaterialSwaps.

### 2a. Trophies — confirmed broken
Every trophy OMOD is described as "Increases Strength and Charisma" but has **no `Enchantments`
property at all**. They only add a keyword plus modifiers on high-range FormIDs:

| OMOD | Name | Effects present |
|---|---|---|
| `01000FAF` / `01000FB2` | Hunter's Trophy (Brahmin) R/L | kw `01000FAD`; `[0023C9DF] +1`, `[0023C9E2] +1` |
| `01000FAC` | Hunter's Trophy (Yao Guai) | kw `01000FAD`; `[0023C9DF] +1`, `[0023C9E2] +1` |
| `01002E73` | Hunter's Trophy (Deathclaw) | kw `01002E72`; `[0023C9DF] +2`, `[0023C9E2] +2` |
| `01003DD0` / `01003DD4` | Great Hunter's Trophy R/L | kw `01002E72`; `[0023C9DF] +2`, `[0023C9E2] +2` |
| `01004D55` | Forsworn Hunter's Trophy (RadStag) | kw `01003DD3`; `[0023C9DF] -1`, `[0023C9E2] +2`, `[0023C9E5] +1` |
| `01003DD5` | Forsworn Hunter's Trophy (torso) | kw `01003DD3`; `[0023C9DF] -1`, `[0023C9E2] +2`, `[0023C9E5] +1` |

Contrast with the mods that demonstrably work, which use the **low-range** SPECIAL actor values:
- `010054C3` Sensor Array — "Increases Perception" — `[000002C3] +2`
- `010054C0` Scholar's Focus — "Increases Intelligence" — `[000002C6] +2`
- `01004D15` Pocketed Greaves — carry weight — `[000002DC] +50`

So the working mods point at `0000_02Cx` AVIFs; the trophies point at `0023_C9xx`.
**`0023C9DF` / `0023C9E2` / `0023C9E5` still need to be resolved against Fallout4.esm.**

Also: helmet and arm trophies share a keyword (`01000FAD` for Brahmin+Yao Guai, `01002E72` for
Deathclaw+Great), so they are mutually exclusive and give identical bonuses.

### 2b. Paint jobs — enchantment copy-paste
- `01004D08` BOS, `01003D9F` Hot Rod Flames, `01004D05` Military all add the **same** enchantment
  `00238383`.
- `01003DA0` Skyforged Steel and `01003DA8` Winter Camouflage have **no enchantment at all**.
- All five paints carry `Rating Int ADD 0` — a no-op.
- `01003DA0` sets `Health` as **Float MUL+ADD 0.1** while every lining sets `Health` as **Int ADD**.

### 2c. Torso lining progression is wrong
Health per rank: A -, B 60, **C 60**, D 180, E 240, F 300. C should be 120.
(Arm/leg/helmet linings are clean: 15/30/45/60/75.)

### 2d. Verified NOT broken
Headlamp OMODs (`0100454B`-`01004550`) have no properties but do carry `MODL` mesh swaps — that is
correct for a cosmetic model mod.

---

## 3. Spelling / naming

### Real misspellings
- `RFGP` ×3 `NNAM` = "HangingFlourescentLightNS" -> "Fluorescent" (editor-only, not player-facing)
- EditorID `miscmod_PA_TES51_WintercamoPaint` — inconsistent casing
- EditorID `miscmod_PA_TES51_Helmet_Headlamp_Vaultboy` — inconsistent casing

### Grammar
- Soul Gem Bracers DESC: "Your aura (and fists) **are** charged..." -> "is charged"

### Loose-mod item name != the mod it installs (the real "naming conventions" problem)
| Loose item (MISC) | OMOD it installs |
|---|---|
| TES-51 Sharp Knuckles | Sharpened Knuckles |
| TES-51 Lightning Bracers | Soul Gem Bracers |
| TES-51 Lightweight Bracers | Lightweight Gauntlets |
| TES-51 Stealth Field | Nocturnal's Embrace |
| TES-51 Medic Pump | Kynareth's Blessing |
| TES-51 Emergency Protocols | Berserker Protocols |
| TES-51 Core Assembly | Adrenaline Boost |
| TES-51 Sun Regen Mod (placeholder name) | Daytime Adventurer |
| TES-51 Overdrive Servos | Sprinter's Greaves |
| TES-51 Kinetic Servos | Wanderer's Greaves |
| TES-51 Calibrated Shocks (L/R) | Pocketed Greaves (L/R) |
| TES-51 Optimized Servos | Lightweight Boots |
| TES-51 Targeting HUD | Detect Life |
| TES-51 Internal Database | Scholar's Focus |
| TES-51 Rad Scrubbers | Radiation Cleanser |
| TES-51 Recon Sensors | Hunter Tracking |
| TES-51 Headlamp Red | Headlamp Red Tactical |
| TES-51 Headlamp VaultBoy | Headlamp Vault Boy |
| TES-51 Skyforge Steel | TES-51 Skyforged Steel |
| TES-51 Great Trophy (L/R) | Great Hunter's Trophy |
| TES-51 Nordic War Paint | TES-51 Nordic Warpaint |
| TES-51 Winter Camo Paint | TES-51 Winter Camouflage |
| TES-51 Hot Rod Flames Paint | TES-51 Hot Rodder Flames |

### Missing descriptions
No `DESC` on: `01003DD5` Forsworn Hunter's Trophy, `01004D55` Forsworn Hunter's Trophy (RadStag),
`01003DAB` Nordic Warpaint, `01003DA8` Winter Camouflage, `01003DA0` Skyforged Steel,
`01003D9F` Hot Rodder Flames, and the six "Standard * Lining" OMODs.

---

## 4. "Useless miscmods"
- `01004D24` "No Upgrade Steel Sword Mod" — a physical loose item for a null mod
- `010054F8` "Standard Steel Warhammer Mod" — same
- `01004D1B mod_melee_TES51SteelSword_Null` carries a stray property (`prop10 Int ADD 1`) on a mod that
  is supposed to do nothing

---

## Blocker
Resolving `0023C9DF`, `0023C9E2`, `0023C9E5`, `00238383`, and confirming the ITMs requires
**Fallout4.esm**. Need the Fallout 4 `Data` folder connected.
