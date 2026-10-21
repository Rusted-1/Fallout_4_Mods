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

## Batch generation in xVASynth (Steam)
`Phase 1 xVASynth batch.csv` holds all 89 lines in xVASynth's batch format: `game_id, voice_id, text, vocoder, out_path, pacing, pitch_amp`.

1. **Pick your voice model(s)** in xVASynth under the Fallout 4 game, and note each model's **voice ID**. It's shown in the model's details, and listed in the model's `.json` file in xVASynth's `models` folder.
2. **Fill in the voices.** Open the CSV in Notepad (not Excel; Excel can change the format) and use Find and Replace:
   - `VOICE_ID_SYNTH_NORA` → your synth Nora voice ID
   - `VOICE_ID_ORGANIC_NORA` → your organic Nora voice ID (the same one if you want both to share a voice)
3. **Turn on the "Lip and Fuz Generator" plugin** (Fallout 4 lip format) if you want `.lip`/`.fuz` files made at the same time.
4. **Batch mode:** drag the CSV into xVASynth's batch window and click Synthesize.
5. **Output:** every file goes to `Nora and Nora\Sound\Voice\NoraAndNora.esp\PlayerVoiceFemale01\` inside xVASynth's own folder, under its final name (`00000900_1.wav` …). That's the game's folder layout, so the `Sound` folder can be dropped straight into the mod.

**Tuning**
- **No emotion column:** batch mode doesn't read emotion. Each line's emotion is approximated with `pitch_amp` (pitch variation):
  - 0.9 for sad or quiet lines
  - 1.0 for neutral
  - 1.15–1.2 for happy, surprised, scared or angry
- **Pacing:** left at 1.0 everywhere.
- **Fixing a line:** for lines that don't land, re-do them one at a time in xVASynth's normal editor using the Delivery notes, and save over the same file name.
- **Vocoder:** blank, so xVASynth picks the best one the model supports.
