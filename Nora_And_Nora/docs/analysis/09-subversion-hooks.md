# Subversion hooks for both Noras

Read from InstituteReformation.esp (Subversion 4.0B, by Toro Montana) on 2026-10-23. Subversion's files are not in
this repo; only its quest editor IDs and stage numbers are recorded here. Master: Fallout4.esm only; strings are inline.

## Moments and hooks (proposed reactions: Synth Nora / Nora)
| Moment | Hook | Synth | Nora |
| --- | --- | --- | --- |
| Spare the Railroad (refuse destruction) | zzReformQuest (01004C6A) 20 | Loves | Likes |
| Become Director to free synths | zzMarch (01006B8B) 10 | Likes | Likes |
| Meeting ends, synths free | zzReformQuest 75 | Loves | Likes |
| Expose Karlin (blackmail) | zzReformQuest 61 | - | Dislikes |
| Kill dissenters | zzReformQuest 57 | Dislikes | Hates |
| Purge the Directorate | zzDirector (0100B896) 13 | Dislikes | Hates |
| X6-88 memory wipe | zzReformQuest 88 | Hates | Dislikes |
| Tell Desdemona | zzReturnRR (0100C10F) 20 | Likes | Likes |
| Announce new policies | zzHope (0100D9DB) 20 | Likes | Likes |
| Tell Piper | zzPiper (0100C10C) 100 | - | Likes |
| Maxson replaced by a synth | zzNextLevel (0100D6A7) 100 | Hates | Dislikes |
| SRB resets Elder Danse | zzSAllGoodMan (0100D06B) 100 | Hates | Dislikes |
| West Coast BoS armistice | zzMAA (0100C20B) 100 | Likes | Likes |
| Armistice refused, war | zzMAA 101 | - | Dislikes |
| Sarah Lyons peace | zzThanksSarah (0100C6E2) 100 | Likes | Likes |
| Minutemen occupy the Institute | zzInstantKarma (0100D9C9) 100 | Likes | Loves |
| Virgil returns human | zzHomecoming (0100C8BF) 100 | Likes | Likes |
| Virgil stays a super mutant | zzReformQuest 29 | Likes | - |

Other useful stages: zzMarch 1500 (reform failed), zzReturnRR 40 (Railroad turned against you), stage 9001 on most
quests (Institute destroyed).

## Shaun's Parentage
Holotape NOTE zzSubShaunParentage (0100E3B1) runs terminal zzSUBTERMShaunParentage (0100E3B0), which sets global
zzDadToShaun (0100C694): 1 = player is Shaun's parent (default), 0 = not related.

## Scenes proposed (Phase 3 script)
Synths freed (tier talk "They're free... am I?"), becoming Director, Maxson replaced, Danse reset, Shaun's Parentage.
Working copy with open questions: the "Quest Reactions: Both Noras" doc.
