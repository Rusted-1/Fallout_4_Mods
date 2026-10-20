# Nora and Nora: Phase 1 Script
**From the first meeting to the Vault 111 choice.** Draft 2, built from `notes/interaction-ideas.md` and the answers to draft 1's questions.

## How to read this
**Speakers**
- **NORA**: the organic Nora from Nora Spouse. Sharp, dry, protective. A lawyer before the war. Calls Nate "hon" or "honey".
- **SYNTH**: synth Nora from Synthetic Love. Same memories, same voice. Here she is warmer, more anxious, and clings to "normal".
- **NATE**: the player. Choices follow the vanilla four-button wheel:
  - **[Y]** agree or kind
  - **[B]** refuse or harsh
  - **[X]** sarcastic
  - **[A]** ask
  
  Each choice has a short label (the vanilla wheel) and the full line (shown by XDI). XDI also allows more than four choices, which is used where noted.

**Voicing**
- NORA and SYNTH both use the vanilla female player voice (`PlayerVoiceFemale01`).
- **NATE is text-only.** No audio is recorded for him. With **Extended Dialogue Interface (XDI)** installed, the wheel shows his full line. Without it, players see the short label. Either way the dialogue works. XDI 1.3.6 matches the old-runtime game (1.10.163).
- The **Delivery** column is the direction for the AI voice tool.
- Lines that might be swapped for a vanilla recording are checked separately (voice catalog task). Treat every line here as needing new audio until then.

**Line IDs**: `P1-<scene>-<number>`. Keep them when editing so voice files stay matched.

**Affinity**: the effect is noted after each choice: Love / Like / Dislike / Hate / none.

---

## Scene 1: First Meeting (Diamond City)
**Replaces Synthetic Love's original intro when Nora Spouse's Nora has already been found.**

**Conditions**
- Synthetic Love's encounter is starting (`p865_COMNoraQuest01`).
- Nora Spouse's "O Spouse, Where Art Thou?" is complete.

**Two versions**
- **1A: NORA is with you.** The main version below.
- **1B: NORA is not with you.** SYNTH joins you happily. She panics the first time she sees NORA, whether NORA catches up with you or you go back to her (Scene 1C).

### 1A: NORA is following you
SYNTH spots Nate first and runs to him. She doesn't notice NORA yet.

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S1-001 | SYNTH | Oh my God... Nate? Nate! It's you, it's really you! | Disbelief breaking into joy, running up |
| P1-S1-002 | SYNTH | I looked everywhere. I didn't think I'd ever see your face again. | Breathless, near tears, happy |
| P1-S1-003 | SYNTH | We're together again. That's all that matters, honey. We can find Shaun together, just like we planned. | Clinging, relieved, words tumbling out |

**NATE choices**

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P1-S1-010 | Y | Nora...? | Nora...? But... | Confused. Goes to 011 |
| P1-S1-011 | B | Back up. | Whoa. Back up. Who are you? | Goes to 012 |
| P1-S1-012 | X | Seeing double. | I think I'm seeing double. | Goes to 013 |
| P1-S1-013 | A | How are you here? | How did you get here? | Goes to 014 |

The SYNTH reply to each, below, then NORA cuts in on every branch.

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S1-020 | SYNTH | Yes, it's me! Why are you looking at me like that? | Smile faltering |
| P1-S1-021 | SYNTH | Who am I? Honey, it's me. It's Nora. | Hurt, laughing it off |
| P1-S1-022 | SYNTH | Seeing... what? What's that supposed to mean? | Puzzled, a little stung |
| P1-S1-023 | SYNTH | I... I walked. I don't really remember. Does it matter? I'm here now. | Brushes it off too quickly |

**NORA cuts in** (all branches)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S1-030 | NORA | Get away from him. | Cold, hard, stepping between them |
| P1-S1-031 | SYNTH | Excuse me? Who do you think you... | Turning, irritated, then freezing |
| P1-S1-032 | SYNTH | ...No. No, that's not... | Stunned whisper, seeing her own face |
| P1-S1-033 | NORA | Who are you? No. *What* are you? | Controlled anger, lawyer's cross-examination |
| P1-S1-034 | SYNTH | I'm Nora. I'm his wife. I don't know who you are, or what kind of sick joke this is. | Shaking, defensive, voice rising |
| P1-S1-035 | NORA | I'm his wife. I was in that pod. I've been standing next to him for weeks. | Flat, certain |
| P1-S1-036 | SYNTH | That's a lie. I was in that pod. I remember the cold. I remember the man with the scar. I remember... being shot. | Panicked, insisting, voice cracking |
| P1-S1-037 | NORA | So do I. | Quiet. That's what scares her |
| P1-S1-038 | SYNTH | Then you're the copy. You have to be. Nate, tell her! | Desperate, turning to Nate |

**NATE choices**

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P1-S1-040 | Y | Everyone calm down. | Everybody take a breath. Nobody's getting hurt here. | none |
| P1-S1-041 | B | You're not my wife. | I've been with my wife this whole time. You're not her. | SYNTH Dislike |
| P1-S1-042 | X | Twice the trouble. | Great. I spent two hundred years on ice and now I've got two of you. | none |
| P1-S1-043 | A | Prove it. | If you're really Nora, prove it. | none |

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S1-050 | SYNTH | I can't breathe... I can't... okay. Okay. | Hyperventilating, forcing calm (after 040) |
| P1-S1-051 | SYNTH | Don't say that. Please don't say that to me. | Wounded, barely holding together (after 041) |
| P1-S1-052 | SYNTH | This isn't funny, Nate. None of this is funny. | Angry tears (after 042) |
| P1-S1-053 | SYNTH | Prove it? I... yes. Yes, I can prove it. | Seizing on the idea (after 043) |
| P1-S1-060 | SYNTH | Vault 111. Take me back to the vault. My pod is there. I'll show you where it happened. I'll show you both. | Fixated, urgent, not quite rational |
| P1-S1-061 | NORA | Hon, that thing is wearing my face and saying my words. You want to take it home? | Low, to Nate, appalled |
| P1-S1-062 | SYNTH | I'm not a *thing*. | Sharp, hurt |

**NATE choices (recruits SYNTH)**

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P1-S1-070 | Y | We'll go to the vault. | All right. We go to Vault 111, and we find out the truth. Together. | NORA none, SYNTH Like |
| P1-S1-071 | B | Only to settle this. | Fine. We go to the vault to settle this. Then we're done. | SYNTH Dislike |
| P1-S1-072 | X | Road trip. | Family road trip. What could go wrong. | none |
| P1-S1-073 | A | Nora, your call? | Nora, what do you think? | Goes to 074 |
| P1-S1-074 | NORA | I think we keep it where we can see it. Fine. The vault. | Grudging, practical |
| P1-S1-075 | SYNTH | Thank you. You'll see. Both of you will see. | Shaky relief |
| P1-S1-076 | NORA | It walks in front of me. | Final word, cold |

**Quest:** Synthetic Love's "Cold Comfort" objective text becomes **"Travel with Nora to Vault 111."** The "examine the corpse" part is gone, because Nora Spouse removes the body.

### 1B: NORA is not with you
Short version. SYNTH runs to Nate the same way (001–003). Then:

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S1B-001 | NATE | Nora... I left you at the settlement. How did you get here before me? | Confused, wary |
| P1-S1B-002 | SYNTH | Settlement? What settlement? I've been searching for you since I woke up. | Genuinely lost |
| P1-S1B-003 | NATE | Come with me. We need to talk. | Careful, decided (text only) |
| P1-S1B-004 | SYNTH | Of course. Anywhere. As long as I'm with you. | Trusting, happy |

SYNTH joins as a follower. Until she meets NORA, she uses her normal Synthetic Love lines. She is cheerful and doesn't yet know anything is wrong. **Scene 1C** plays the first time she and NORA are near each other: NORA reaching you, or you bringing SYNTH to wherever NORA is waiting.

### 1C: First time they stand together (after 1B)
SYNTH sees NORA first, and the panic starts:

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S1C-001 | SYNTH | Nate... who is that? Why does she... why does she look like me? | Slowing, confused, then frightened |
| P1-S1C-002 | SYNTH | No. No, no, no. That's not possible. | Backing away, breathing fast |

Then the 1A lines from **P1-S1-030 to P1-S1-076** play as normal, starting with NORA's "Get away from him." The vault trip and the ambient lines below start from here.

---

## Ambient: on the road to Vault 111
**Active from recruitment until the party reaches the Vault 111 cryo hall.** SYNTH's normal idle lines and "How are you doing?" answers are replaced by these. NORA's lines are mixed in at a lower rate than her normal idles.

### SYNTH: asked "How are you holding up?" / "Your thoughts?"

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-AM-001 | SYNTH | I'm fine. I'm fine. I'll be fine when we get to the vault. | Repeating, rushed |
| P1-AM-002 | SYNTH | I keep going over that morning. The coffee, the news. Codsworth. Shaun crying. I remember all of it. Why would I remember all of it if it wasn't mine? | Pleading, half to herself |
| P1-AM-003 | SYNTH | Every time I close my eyes I'm back in that pod. Is that normal? Tell me that's normal. | Scared, small |
| P1-AM-004 | SYNTH | She looks at me like I'm something on the bottom of her shoe. My own face, looking at me like that. | Hurt, bitter |
| P1-AM-005 | SYNTH | Can we walk faster? I need to see it. I need you to see it. | Urgent |

### SYNTH: idle remarks while travelling

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-AM-010 | SYNTH | Vault 111 is north of Sanctuary. Up the hill. I know the way. Of course I know the way. | Muttering, reassuring herself |
| P1-AM-011 | SYNTH | What if she's right? ...No. No. | Whisper, shutting it down |
| P1-AM-012 | SYNTH | I can feel my heartbeat. Real people have heartbeats. | Quiet, clutching at proof |
| P1-AM-013 | SYNTH | I remember our wedding. The rain. You dropped the ring. | Soft, almost a question |
| P1-AM-014 | SYNTH | Why can't I remember waking up? | Sudden, confused, almost a sob |

### NORA: idle remarks and "Your thoughts?"

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-AM-020 | NORA | Remind me again why we're escorting an Institute machine to our front door. | Dry, low to Nate |
| P1-AM-021 | NORA | It even fidgets like me. That's the worst part. | Unsettled |
| P1-AM-022 | NORA | When we get to the vault, it's going to see an empty pod. *My* empty pod. And then what? | Grim |
| P1-AM-023 | NORA | I keep waiting for it to slip up. It doesn't. | Uneasy |
| P1-AM-024 | NORA | Don't let it walk behind you, hon. | Warning |

### Exchanges between them (rare, at most one per game day)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-AM-030 | SYNTH | Do you remember the blue dress? The one with the buttons? | Testing, hopeful |
| P1-AM-031 | NORA | It was green. | Flat |
| P1-AM-032 | SYNTH | ...It was green. | Shaken, quietly |
| P1-AM-040 | SYNTH | You don't have to keep staring at me. | Uncomfortable |
| P1-AM-041 | NORA | Someone has to. | Cold |
| P1-AM-050 | SYNTH | What did you study? At law school? | Trying to make conversation |
| P1-AM-051 | NORA | You tell me. | Challenge |
| P1-AM-052 | SYNTH | ...Contracts. You hated contracts. *I* hated contracts. | Unsure whose memory it is |
| P1-AM-053 | NORA | Don't. | Quiet, rattled |

---

## Scene 2: Vault 111
**Conditions:** "Cold Comfort" is active and the party enters the Vault 111 cryo hall. Both Noras are present (UCF or tag-along mode).

### 2A: The pods

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S2-001 | SYNTH | Here. Here it is. This is where they put us. | Rushing ahead, hushed |
| P1-S2-002 | SYNTH | That one's yours, honey. And this one... this is mine. | Hand on the pod, certain |
| P1-S2-003 | SYNTH | It's empty. Of course it's empty, I'm right here. See? I told you. | Triumphant for a second |
| P1-S2-004 | NORA | It's empty because I climbed out of it. | Quiet, steady |
| P1-S2-005 | NORA | The door opened. I was bleeding. I fell on the floor right there. I found stimpaks in the overseer's office, and I sat against that wall until I could stand. | Each detail deliberate, looking at the spots |
| P1-S2-006 | NORA | So tell me. How did *you* get out? | Not cruel. Genuinely asking |
| P1-S2-007 | SYNTH | I... I got out. I walked out. I... | Reaching for it, nothing there |
| P1-S2-008 | SYNTH | I remember the cold. I remember the shot. And then I'm in Diamond City. There's nothing in between. Why is there nothing in between? | Rising horror |
| P1-S2-009 | SYNTH | Nate. Nate, why can't I remember? | Breaking |

**NATE choices**

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P1-S2-010 | Y | It's okay. | Hey. Hey. Look at me. It's going to be okay. | SYNTH Like |
| P1-S2-011 | B | You know why. | You know why, Nora. | SYNTH Dislike |
| P1-S2-012 | X | Bad memory. | Maybe you just have a bad memory. | none |
| P1-S2-013 | A | What do you remember? | What's the last thing you really remember? | none |

### 2B: The breakdown (all branches)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S2-020 | SYNTH | No... no, no, no. She's real. She's the real one. She's been with you this whole time. | Collapse begins, sinking down against the pod |
| P1-S2-021 | SYNTH | Then what am I? Somebody built me. Somebody *made* me remember my baby. | Sobbing |
| P1-S2-022 | SYNTH | I'm not anybody. I'm a recording of somebody. | Hollow, crying |

SYNTH plays a crying or kneeling idle and stays at the pod. NORA takes Nate a few steps away.

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S2-030 | NORA | Hon. Over here a second. | Low, pulling him aside |
| P1-S2-031 | NORA | I don't like this. I don't like *it*. I don't know what the Institute wants with a copy of me, and that scares the hell out of me. | Honest, troubled |
| P1-S2-032 | NORA | But look at her. That isn't an act. Whatever she is, she's hurting. | Reluctant pity |
| P1-S2-033 | NORA | I think she should come with us. If nothing else, so we can keep an eye on her. | Decided, practical |
| P1-S2-034 | NORA | It's your call, though. It always is. | Handing it over |

---

## Scene 3: The Choice
NATE goes back to SYNTH. She looks up.

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S3-001 | SYNTH | So. What happens to me now? | Small, bracing |

**NATE choices**

| ID | Button | Label | Line | Outcome |
|---|---|---|---|---|
| P1-S3-010 | Y | Come with us. | You're coming with us. Whatever you are, you're not alone. | **Choice 1.** NORA Like, SYNTH Love |
| P1-S3-011 | A | I need time. | I need some time to think about this. Stay here, and I'll come back. | **Choice 2.** None for either |
| P1-S3-012 | B | You're an abomination. | You're a synth. An Institute abomination wearing my wife's face. | **Choice 3.** NORA Dislike, SYNTH Hate, turns hostile |
| P1-S3-013 | X | Go your own way. | I'm not going to hurt you. But you're not coming with us. | **Choice 4.** NORA Like, SYNTH Dislike, then a confirmation |

The X button is used for choice 4 because it's the odd one out. Swap it with B if the wheel reads wrong in game.

### Choice 1: Come with us

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S3-020 | SYNTH | You mean it? You... thank you. Thank you, thank you. I'll be useful, I promise. You won't regret it. | Overwhelmed gratitude, tears and laughing |
| P1-S3-021 | NORA | All right. Let's go. On your feet. | Brisk, hand out to help her up |
| P1-S3-022 | SYNTH | ...Thank you. Both of you. | Taking the hand, surprised |

**Result:** SYNTH becomes a normal companion. The Nora↔Nora relationship starts at **Tier 1: Unease and tension**. The ambient lines above stop.

### Choice 2: I need time

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S3-030 | SYNTH | I understand. I'd need time too. I'll be here. I don't really have anywhere else. | Quiet, resigned, not bitter |
| P1-S3-031 | NORA | Fair enough. We'll come back. | Neutral |

**Result:** SYNTH stays in Vault 111 (sandbox near the pods). Talking to her again offers the same four choices, without the breakdown.

**FOMOD option: "Synth Nora's patience"**
- **Waits forever** (default): she stays until you decide.
- **Leaves after a while:** if you don't come back within 7 in-game days, she leaves the vault the same way as choice 4. That starts the 3-day timer and the battle-site encounter.

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S3-032 | SYNTH | (Note left on her pod, "leaves" option only) I waited. I understand. I'm going to find my own way to be useful. Take care of her. | Written, calm, sad |

### Choice 3: Abomination

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S3-040 | NORA | Nate... Fine. Let's get this over with. | Disgusted with all of it, looking away |
| P1-S3-041 | SYNTH | Maybe I'm not the original. But I'm a person! I'm a *person*! | Scream, standing, rage and terror |

**Result:** SYNTH turns hostile and can be killed. Synthetic Love's own murder and hatred handling applies from here. Killing her still counts as murder for companions who care about that.

After she's dead:

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S3-045 | NORA | That's that. | Flat, quiet, not looking at the body |
| P1-S3-046 | NORA | Can we get out of here now? Please. | Tired, wanting to leave the vault behind |

### Choice 4: Go your own way
First, a confirmation:

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S3-050 | SYNTH | Please. Please don't do this. I won't get in the way, I won't say a word, I'll just... please. | Desperate, begging |
| P1-S3-051 | SYNTH | Please reconsider. | Barely audible |

The same four choices are offered again (010–013). Picking **X** again confirms choice 4. Any other button switches to that choice. With XDI, the confirmation can be a fifth option instead: **"I'm sure." / "I'm sorry. I've made up my mind."**

On confirmation:

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-S3-060 | NORA | Good riddance. | Clipped, but she doesn't look back at her |
| P1-S3-061 | SYNTH | ...Okay. | Hollow |

**Result:**
- SYNTH is removed as a companion and becomes a plain NPC in Vault 111.
- **After 3 in-game days**, she leaves the vault.
- The **death-site encounter** becomes available (Random Encounter Framework add-on).

---

## Choice 4 aftermath: the battle site
**Encounter setup (for the systems task, not voiced)**
- SYNTH dead, wearing **T-51c power armor**. Fallback if that's unstable: her body next to the frame.
- Her inventory, or on her body if the power armor is skipped:
  - light combat armor, left and right arms
  - medium combat armor chest and legs
  - automatic laser rifle
  - plasma grenades
  - stimpaks
- **2 dead coursers** and **8 dead synths** around her.
- When the encounter loads, a small quest starts: **"Investigate the battle site."** It stays loaded until the note is read, and reading the note completes it.

### Note: "Nora's Final Wish"
*The user's text, typos fixed, wording kept.*

> I'm not a real person, am I? I've come to accept this. I know my husband, if I can call him that, is still out there with the real me. I hope they can find happiness in this horrid world.
>
> I won't stop looking for my son. Even though I know he isn't my organic son, he is still mine in my heart, or whatever I have. I've acquired some new gear and have been tracking some of the disappearances and other synth sightings related to the Institute. If I've mapped out the sightings and disappearances right, the next one will be a local farm's wife.
>
> Not again. I won't let them do it to another family like the half-assed try they did to mine. I'm going to stop them. They will regret messing with my family and all the others they have destroyed.
>
> I'm coming for you, Institute, if it's the last thing I do.

### Reactions when the note is read (if NORA is with you)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P1-NT-001 | NORA | She went after them. On her own. | Stunned |
| P1-NT-002 | NORA | "A local farm's wife." She was trying to save someone. | Reading it again, voice catching |
| P1-NT-003 | NORA | ...She really did think like me. | Quiet, guilty |

**NATE choices**

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P1-NT-010 | Y | She was brave. | She died trying to protect people. That's who you are, too. | NORA Like |
| P1-NT-011 | B | It was a machine. | It was a machine doing what it was built to do. | NORA Dislike |
| P1-NT-012 | X | Should've stayed home. | Should've stayed in the vault. | NORA Dislike |
| P1-NT-013 | A | You okay? | Are you okay? | none |
| P1-NT-020 | NORA | I sent her away. "Good riddance." That's what I said. | Regret (after 013) |

---

## Decisions (from draft 1 review)
1. **1B:** she follows; the panic plays when she first meets NORA (1C).
2. **Choice 2:** waiting forever or leaving after a while is a **FOMOD option**.
3. **Choice 3:** NORA says "That's that" and asks to leave.
4. **The note's farm:** the user is choosing from the farm list (see chat).
5. **Nate:** text only, with XDI showing full lines.
