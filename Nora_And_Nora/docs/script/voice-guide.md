# Nora and Nora: Phase 1 Voice Guide

`Phase 1 voice sheet.csv` lists **89 lines**:
- **Synth Nora:** 55 lines
- **Organic Nora:** 34 lines
- **Nate:** none. He's text only, and XDI shows his lines in full.

## The sheet's columns

| Column | What it's for |
|---|---|
| **File name** | Save the line under exactly this name, e.g. `00000907_1.wav`. These are the dialogue IDs reserved for the patch (`0x900`–`0x958`), so the game will find each file without renaming. |
| **Line ID** | Matches `phase1-script.md`. Use it to find the line in context. |
| **Speaker** | Both Noras use the same voice (the vanilla female player voice). Vary the performance, not the voice: synth Nora is warmer and more anxious, organic Nora drier and steadier. |
| **Text** | Exactly what she says. *Emphasis* is listed in Delivery as "stress: …". |
| **Emotion** | One-word tag for tools with an emotion setting: neutral / happy / sad / angry / fear / surprise. A starting point; the Delivery note is the real direction. |
| **Delivery** | Acting direction. |
| **Scene** | Where the line plays. |

The CSV opens in Excel or Google Sheets and sorts by any column. Sorting by **Speaker** lets you record one Nora at a time.

## Recording
- **Format:** WAV, mono, 16-bit. 44.1 kHz is a safe rate for Fallout 4 voice files.
- **Length:** trim silence at the start and end. A short tail (about 0.2 s) sounds natural.
- **Folder:** put finished files in
  `Sound\Voice\NoraAndNora.esp\PlayerVoiceFemale01\`
  Both Noras go in the same folder. The file name decides which line it is.

## Tools (free)
- **xVASynth** is the usual free, offline AI voice tool for Bethesda modding, with many Fallout 4 voice models.
  - Check its model list for a **female player / Sole Survivor** model. I couldn't confirm one exists from the model list available online.
  - If there isn't one, pick the closest female model and use the Delivery notes to shape it.
- **Lip-sync without the Creation Kit:** the xVASynth plugin **"Lip and Fuz Generator"** (Nexus, Skyrim SE mod 55605) supports Fallout 4. It makes `.lip` files, and optionally `.fuz` files, with no CK needed. It needs `FaceFXWrapper.exe` placed in its folder.
- If you only produce `.wav` files, that's fine. Drop them in the Nora_Nora_Synth folder and I'll check names, levels and length before they go into the patch.

## Rules that keep the files matching
- **Don't rename files.** If a line is rewritten later, it keeps its file name.
- **New lines get new numbers.** Phase 1 uses `0x900`–`0x958`. The next lines start at `0x959`.
- **Cutting a line just retires its number.** Nothing else shifts.
