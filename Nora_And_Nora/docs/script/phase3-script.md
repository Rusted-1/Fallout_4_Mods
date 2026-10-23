# Nora and Nora – Phase 3 Script (draft 2): Synth Nora and synths

Draft 2, 2026-10-23: your edits from draft 1, in the same table format as the Phase 1 and 2 scripts so the voice sheet
can be built from it. Reactions are your calls from the "Quest Reactions: Both Noras" doc and the design notes.

Each reaction line plays right after the "Synth Nora liked that." pop-up, the way vanilla companions comment. Where
Organic Nora answers, her line plays straight after. None of these play in the broken phase.

Format: `| ID | Speaker | Line | Delivery |`. Player choices: `| ID | Button | Label | Line | Effect |`.

Where the lines go:
- Sections 1–4 (vanilla game): NoraAndNora.esp.
- Section 5 (Subversion): a separate light plugin, "NoraAndNora - Subversion.esp", installed only when Subversion is.

## 1. Synths as people (vanilla quests)

Bunker Hill: "Synths are weapons built by the Institute." (Synth Dislikes)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P3-SP-001 | SYNTH | Weapons. Is that what you think I am? | Hurt, quiet |

Getting a Clue: "Don't lie to me, Nick. You're one of them. They made you." (Synth Hates)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P3-SP-010 | SYNTH | He's helped every person in this city, and that's what you lead with? | Angry |

The Enemy of My Enemy: "Bullshit. You're a synth, Valentine! Tell me what you know!" (Synth Hates)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P3-SP-011 | SYNTH | He's trying to help us. Stop it. | Cold, sharp |

Road to Freedom: "Makes no difference to me if it's a human or a synth." (Synth Loves)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P3-SP-020 | SYNTH | Thank you. | Moved, soft |

Tradecraft: "Whether it's synths or humans I'm against slavery." (Synth Loves)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P3-SP-021 | SYNTH | Somebody had to say it out loud. Thank you. | Warm |

The Nuclear Option (Institute ending): evacuating (Synth Likes) / not evacuating (Synth Dislikes)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P3-SP-030 | SYNTH | Get them out. All of them. Even the ones who'd never do the same for me. | Urgent |
| P3-SP-031 | SYNTH | There were synths down there who never chose any of this. | Shaken |

## 2. Shaun (Institutionalized)

She now fully understands she is a synth; she resents Shaun for the memories but still loves him, and stays resentful
of the Institute while Shaun runs it. Plays once, after meeting Father.

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P3-SH-001 | SYNTH | He made me. He picked which memories I'd get. He picked you. | Numb |
| P3-SH-002 | SYNTH | And I still want to hold him. How is that fair? | Breaking |
| P3-SH-003 | NORA | Because he's yours too. Whatever that means now. | Gentle |
| P3-SH-004 | SYNTH | I'm not setting foot in that place again unless I have to. Not while he's in charge. | Resolved |

## 3. Faction choices

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P3-FC-001 | SYNTH | People helping people. I can get behind that. | Warm (join the Minutemen, Synth Likes) |
| P3-FC-002 | SYNTH | This was the right choice. Out of all of them. | Relieved (Minutemen ending, Synth Loves) |
| P3-FC-003 | NORA | It really was. | Agreeing |
| P3-FC-010 | SYNTH | They don't even ask what I am. They just ask if I'm safe. | Moved (join the Railroad, Synth Loves) |
| P3-FC-011 | SYNTH | Synths like me get to choose now. Rights. Freedom. Imagine that. | Hopeful (Railroad ending, Synth Loves) |
| P3-FC-012 | NORA | She's right. They're good people. | Agreeing |
| P3-FC-020 | SYNTH | They'd shoot me on sight if they knew. You know that, right? | Worried (join the Brotherhood, Synth Dislikes) |
| P3-FC-021 | NORA | They're our best chance at finding Shaun. | Firm |
| P3-FC-022 | SYNTH | A steel hand. Sure. But at what cost? | Bitter (Brotherhood ending, Synth Dislikes) |
| P3-FC-023 | NORA | Nobody's touching you. Not while I'm here. | Protective (tier 3 or higher only) |
| P3-FC-030 | SYNTH | Better you than him. It still hurts, though. | Sad (Institute ending, Synth Likes) |
| P3-FC-031 | NORA | For both of us. | Quiet |
| P3-FC-040 | SYNTH | There were good people up there. I still feel safer. | Conflicted (Brotherhood destroyed, Synth Likes) |
| P3-FC-041 | NORA | A lot of good people. | Sad |
| P3-FC-050 | SYNTH | The Commonwealth will be better without them. | Relieved (Institute destroyed, Synth Loves) |
| P3-FC-051 | NORA | It will. | Agreeing |

## 4. Synth-hunting moments

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P3-HU-001 | SYNTH | He didn't know either. Thank you for not making him pay for it. | Grateful (Blind Betrayal: spare Danse, Synth Loves) |
| P3-HU-002 | SYNTH | He served them his whole life. This is how they repay him. | Bitter (Blind Betrayal: execute Danse, Synth Hates) |
| P3-HU-010 | SYNTH | Good job, sweetie. | Proud, warm (Human Error: free Amelia Stockton, Synth Loves) |
| P3-HU-011 | SYNTH | You let them keep her. You let them keep testing. | Cold (Human Error: side with Dr. Chambers, Synth Hates) |
| P3-HU-020 | SYNTH | He ran. I'd have run too. | Sad (Synth Retention: return the escaped synth, Synth Dislikes) |

## 5. Subversion

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P3-SV-001 | SYNTH | You warned them. You didn't have to. | Grateful (spare the Railroad, zzReformQuest 20, Synth Loves) |
| P3-SV-002 | SYNTH | If anyone can change that place, it's you. I'm with you all the way. | Determined (become Director, zzMarch 10, Synth Likes) |
| P3-SV-003 | NORA | Same. Let's make the world a better place. | Warm |
| P3-SV-010 | SYNTH | They're free. Every one of them. | Overjoyed (meeting ends, synths free, zzReformQuest 75, Synth Loves) |
| P3-SV-011 | NORA | About time. | Dry |
| P3-SV-012 | SYNTH | Freedom, bought like that? | Disturbed (kill the dissenters, zzReformQuest 57, Synth Dislikes) |
| P3-SV-013 | SYNTH | I wanted them free. Not like this. | Hollow (purge the Directorate, zzDirector 13, Synth Dislikes) |
| P3-SV-014 | NORA | A dictator, huh? Gosh, it's as if we've learned nothing from a rather large war two hundred years ago. | Sarcastic |
| P3-SV-020 | SYNTH | You took everything he was. Just like that. | Cold (X6-88's memory wipe, zzReformQuest 88, Synth Hates) |
| P3-SV-021 | NORA | Huh. | Uneasy |
| P3-SV-030 | SYNTH | Let the whole Commonwealth hear it. | Proud (tell Piper, zzPiper 100, Synth Loves) |
| P3-SV-031 | NORA | Families can trust each other again. You did good, hon. | Warm |
| P3-SV-032 | SYNTH | Say it again. I want to hear it again. | Happy (announce the new policies, zzHope 20, Synth Likes) |
| P3-SV-033 | NORA | Solid. That should keep things running smooth. | Approving |
| P3-SV-040 | SYNTH | That's exactly what they made me for. Pretending to be someone. | Bitter (Maxson replaced by a synth, zzNextLevel 100, Synth Hates) |
| P3-SV-041 | NORA | Why? We went through this ourselves. | Upset |
| P3-SV-042 | SYNTH | Would you do that to me? If it made things easier? | Hurt (Danse reset by the SRB, zzSAllGoodMan 100, Synth Hates) |
| P3-SV-043 | NORA | Danse... I'm sorry. | Sad |
| P3-SV-050 | SYNTH | No more coursers. No more cages. | Relieved (Minutemen occupy the Institute, zzInstantKarma 100, Synth Likes) |
| P3-SV-051 | NORA | Hell yeah. For the people, of the people. | Fired up |

### Scene: "They're free... am I?" (after the synths are freed, tier 2 or higher)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P3-SV-100 | SYNTH | They're free. Every synth down there. So... am I? | Uncertain, hopeful |
| P3-SV-101 | NORA | Hell yeah you are. | Firm, warm |

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P3-SV-110 | Y | Always were | You always were. | Synth Loves |
| P3-SV-111 | B | Free to choose | You're free to choose. Stay or go. | Synth Likes |
| P3-SV-112 | X | With me | You're with me. That's different. | No reaction |
| P3-SV-113 | A | Not the same | You're a synth. It's not the same. | Synth Dislikes; counts toward Hurt |

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P3-SV-120 | SYNTH | Then I choose this. I choose you two. | Happy, tearful (after Y) |
| P3-SV-121 | SYNTH | Then I'm staying. Because I want to, not because I'm told. | Steady (after B) |
| P3-SV-122 | SYNTH | ...Okay. I'll take that. | Small (after X) |
| P3-SV-123 | SYNTH | Right. Of course. | Hurt, quiet (after A) |
| P3-SV-124 | NORA | She's earned it. | Warm (after Y or B) |

## Changes from your draft (spelling only, so xVASynth reads them right)
- P3-HU-002 "repayhim" → "repay him"; P3-HU-010 "sweeite" → "sweetie".
- P3-SV-003 "Lets make the world a better." → "Let's make the world a better place." (check)
- P3-SV-031 "Familys … agian … hun" → "Families … again … hon".
- P3-SV-033 "Solidm should keep things running smooth." → "Solid. That should keep things running smooth." (check)
- P3-SV-041 "throught" → "through"; P3-SV-051 "peaple" → "people"; "200 years" spelled out for the voice.
- Your "Hell yeah you are." on the scene opener is Organic Nora's line P3-SV-101, before the player answers.

## Open question
- Shaun's Parentage (Subversion holotape): only a one-off talk, or should "not related to Shaun" change her Shaun lines too?
