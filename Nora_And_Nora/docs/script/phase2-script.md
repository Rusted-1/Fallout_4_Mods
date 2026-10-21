# Nora and Nora: Phase 2 Script
**Relationship tiers 1 to 3, from the Vault 111 choice to "acceptance and basic friendship".** Draft 1, built from `notes/interaction-ideas.md` and the answers of 2026-10-21.

## How to read this
Same conventions as `phase1-script.md`:
- **NORA** = organic Nora, **SYNTH** = synth Nora, **NATE** = the player (text only, full lines shown with XDI).
- Buttons: **[Y]** agree or kind, **[B]** refuse or harsh, **[X]** sarcastic, **[A]** ask.
- **Affinity** is noted after each choice: Love / Like / Dislike / Hate / none.
- **Line IDs** are `P2-<scene>-<number>`. Keep them when editing so voice files stay matched.

**Where this starts:** right after Phase 1 **Choice 1: Come with us**. If synth Nora was left waiting and you later choose "Come with us", it starts then.

## Timeline at a glance

| Step | When | What happens |
|---|---|---|
| Tier 1 starts | Choice 1 in Vault 111 | Tense ambient lines. SYNTH starts bringing a gift once per game day |
| Gift check-in | After the 5th gift | SYNTH asks "Am I doing well?" (4 choices) |
| NORA's first talk | 2 game days after the check-in | NORA talks about SYNTH. What she says depends on the check-in choice |
| Tier 2 starts | 4 game days after NORA's first talk | Calmer ambient lines. NORA asks "Can I talk to you about... her?" |
| Tier 3 starts | 3 game days after NORA's tier 2 talk, adjusted by your choices (2 to 5 days) | Friendly ambient lines, compliments, stimpak aid. SYNTH asks "Can I talk to you?" |

**Timer changes from your choices** (all applied to the 3-day wait for tier 3):

| Choice | Change |
|---|---|
| Tier 2, choice 2 ("She's nice") | −1 day |
| Tier 2, choice 3 ("Keeping her at arm's length") | +1 day |
| Tier 2, choice 4 ("Dumb machine") | +2 days, and starts the **cruel path** |

The tier 3 talk itself also changes how fast tier 4 arrives (noted in that section). Tier 4 is Phase 4.

**The cruel path.** It starts at tier 2 with "She's just a dumb machine". The tier 1 gift choice 4 ("If this is all she's good at") doesn't start it, but it does change SYNTH's tier 3 talk. On the cruel path the tiers still advance, just more slowly.

**Hurt counter: when she leaves on her own.** Every **Hate** from SYNTH in these scenes adds 1. At **3**, she leaves (see "She leaves" at the end). That works the same as Phase 1 choice 4: a 3-day timer, then the battle site. Being "super manipulative" so that she stays and shuts down instead belongs to the identity work in Phase 4. For now, the counter always leads to her leaving.

---

## Tier 1: Unease and tension

### Ambient: SYNTH, asked "How are you holding up?"

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-T1-001 | SYNTH | I'm okay. Really. I'm just... trying to figure out what I'm for. | Forced brightness that slips |
| P2-T1-002 | SYNTH | She doesn't talk to me much. I don't blame her. I wouldn't talk to me either. | Rueful, small laugh |
| P2-T1-003 | SYNTH | I still reach for my wedding ring sometimes. Then I remember whose ring it is. | Quiet, hurt |

### Ambient: SYNTH idle remarks

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-T1-010 | SYNTH | I'll keep an eye out for supplies. It's the least I can do. | Eager to help |
| P2-T1-011 | SYNTH | Nice weather. For the end of the world, I mean. | Awkward attempt at small talk |
| P2-T1-012 | SYNTH | I'm not going anywhere. Just so you know. | Soft, reassuring herself as much as him |

### Ambient: NORA, asked "Your thoughts?"
NORA otherwise keeps her normal Nora Spouse lines in tier 1, as the design asks.

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-T1-020 | NORA | She's trying. I'll give her that. Doesn't mean I have to like it. | Dry, grudging |
| P2-T1-021 | NORA | Every time she laughs, I hear myself. It's like hearing your voice on a tape recorder. | Unsettled |

### Exchanges between them (rare, at most one per game day)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-T1-030 | SYNTH | Coffee? Well. Something brown and hot, anyway. | Offering a cup, hopeful |
| P2-T1-031 | NORA | ...Thanks. | Takes it, doesn't look at her |
| P2-T1-050 | SYNTH | Do you want me to take watch tonight? | Careful, polite |
| P2-T1-051 | NORA | I'll take it. | Flat, firm |

*Cut: the rifle exchange (P2-T1-040 to 042). Its files 00000963–00000965 are retired; delete them if you made them.*

### Gifts (once per game day, up to 5 before the check-in)
SYNTH walks up to Nate and hands over an item. The game picks the item: ammo for Nate's equipped weapon, stimpaks or RadAway, a small pile of caps, or rare junk (screws, gears, adhesive, circuitry, nuclear material). No reply from Nate is needed.

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-GF-001 | SYNTH | Found these. I think they fit your gun? | Shy, holding them out |
| P2-GF-002 | SYNTH | Here. Stimpaks. You get hurt more than you let on. | Concerned, a little bossy |
| P2-GF-003 | SYNTH | Some caps. Don't ask where I found them. Actually, it was a mailbox. That's... legal, right? | Guilty laugh |
| P2-GF-004 | SYNTH | Screws, and some good adhesive. I know you like building things. | Pleased with herself |
| P2-GF-005 | SYNTH | I don't know what this is, but it looked important. | Hopeful, unsure |

### The check-in: "Am I doing well?" (after the 5th gift)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-CK-001 | SYNTH | Can I ask you something? Am I... doing well? With all of this? I just want to be useful to you. | Nervous, wringing her hands |

**NATE choices**

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P2-CK-010 | Y | You don't need to prove anything. | This isn't necessary. You don't need to prove yourself to me with things. Show me with what you do. | SYNTH Like, NORA Love. **Gifts stop** |
| P2-CK-011 | A | Keep up the good work. | You're doing great. Keep it up. | SYNTH Like, NORA none. Gifts continue |
| P2-CK-012 | X | Thanks for looking out. | You don't have to, but I really appreciate you keeping an eye out. Thank you. | SYNTH Love, NORA Love. Gifts continue, **favouring rare junk** |
| P2-CK-013 | B | If that's all you're good at. | If this is all you're good at, you should stick with it. | SYNTH Dislike, NORA Dislike. Gifts continue (sad lines) |

**SYNTH replies**

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-CK-020 | SYNTH | Oh. Okay. Actions, not things. I can do that. I *want* to do that. | Surprised, then lighter (after 010) |
| P2-CK-021 | SYNTH | Really? Okay! I'll keep looking. | Bright, relieved (after 011) |
| P2-CK-022 | SYNTH | You... thank you. That means more than you know. I'll find you the good stuff. The really good stuff. | Moved, smiling through it (after 012) |
| P2-CK-023 | SYNTH | ...Right. Of course. I'll stick with it. | Hurt, swallowing it (after 013) |

**NORA reacts** (she's been listening)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-CK-030 | NORA | That was a good thing you just did, hon. | Quiet, warm (after 010 or 012) |
| P2-CK-031 | NORA | That was cold, Nate. Even for her. | Disapproving, low (after 013) |

### Gifts after the check-in

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-GF-010 | SYNTH | Found some more for you. Still keeping an eye out! | Cheerful (after 011) |
| P2-GF-020 | SYNTH | Rare junk, as promised. Gears, and a little bit of circuitry. | Proud (after 012) |
| P2-GF-021 | SYNTH | Look at this. Nuclear material! Don't worry, I didn't lick it. | Teasing, delighted (after 012) |
| P2-GF-030 | SYNTH | Here. It's what I'm good for. | Flat, sad (after 013) |
| P2-GF-031 | SYNTH | More supplies. I'll get more tomorrow. | Dutiful, quiet (after 013) |

### NORA's first talk (2 game days after the check-in)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-N1-001 | NORA | Hon, got a minute? It's about her. | Low, pulling him aside |
| P2-N1-002 | NORA | She's not as bad as I thought. I hate saying it, but I'm starting to enjoy having her around. | Reluctant honesty |

Then one of these, matching the check-in choice:

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-N1-010 | NORA | What you told her about actions, not things? It gave her some confidence. You can see it in how she carries herself. | Approving (after CK-010) |
| P2-N1-011 | NORA | She's useful, I'll give her that. But I think there's more to her than collecting junk. | Thoughtful (after CK-011) |
| P2-N1-012 | NORA | You were honest with her, and she lit up like a Christmas tree. I've started helping her look. Don't tell her I said this, but it's kind of fun. | Warm, a little embarrassed (after CK-012) |
| P2-N1-013 | NORA | You were a little rough on her. I get it, believe me. I'm not exactly comfortable either. | Fair, measured (after CK-013) |

**NATE choices**

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P2-N1-020 | Y | I agree. | I agree with you. | none |
| P2-N1-021 | B | I don't. | I don't see it that way. | none |
| P2-N1-022 | A | Wait and see. | I'm going to wait and see. | none |

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-N1-030 | NORA | Fair enough. I just think she's got more in her than either of us expected. Room to grow. | Understanding, closing the topic |

**Result:** tier 1 is complete. Tier 2 starts **4 game days later**.
If CK-012 was chosen, NORA now brings an occasional gift too:

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-GF-040 | NORA | She found the gears. I found the screws. Don't let her tell you otherwise. | Dry, competitive |

---

## Tier 2: Mutual cooperation
The two work together more easily. NORA is still cautious, but her guard is lower.

### Ambient: exchanges between them

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-T2-001 | NORA | Left flank. You take it. | Brisk, after a fight starts |
| P2-T2-002 | SYNTH | On it. | Quick, pleased to be trusted |
| P2-T2-010 | SYNTH | You were right. It was green. The dress. | Wry, peace offering |
| P2-T2-011 | NORA | I know. ...It looked better on me. | Dry, the faintest smile |
| P2-T2-020 | NORA | You can take watch tonight. Wake me at two. | Matter-of-fact, a step forward |
| P2-T2-021 | SYNTH | I will. Thank you. | Touched, trying not to show it |

### Ambient: asked "Your thoughts?"

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-T2-030 | NORA | She covered me back there. I didn't ask her to. | Puzzled, softening |
| P2-T2-031 | SYNTH | She let me take watch last night. I know that sounds small. It isn't. | Quietly happy |

### NORA's tier 2 talk

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-N2-001 | NORA | Hey, honey. Can I talk to you about... her? | Hesitant, glancing toward SYNTH |

**NATE choices**

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P2-N2-010 | Y | Sure, what's up? | Sure. What's up? | none. Talk continues |
| P2-N2-011 | A | Is something wrong? | Is something wrong? | none. Talk continues |
| P2-N2-012 | B | Not right now. | Not right now. | none. NORA asks again next time you talk to her |
| P2-N2-013 | X | Yep. | Yep. | none. Talk continues |

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-N2-015 | NORA | Oh. Okay. Just get back to me soon, okay? | Slightly deflated (after 012) |
| P2-N2-020 | NORA | We've been traveling together for a while now, the three of us. And she seems... okay. She hasn't hated my company, anyway. I want to know what you think. | Open, a little vulnerable |

**NATE choices**

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P2-N2-030 | A | Helpful, but not trusted. | She's been very helpful, but I don't fully trust her yet. | NORA Like |
| P2-N2-031 | Y | I like her. | She's nice. I've talked to her a few times and I like her. I think we can trust her. | NORA Like, SYNTH Like. Tier 3 wait **−1 day** |
| P2-N2-032 | X | Arm's length. | I'm still not convinced she's on our side. I'm keeping her at arm's length. | SYNTH Dislike, NORA none. Tier 3 wait **+1 day** |
| P2-N2-033 | B | Just a dumb machine. | She's just a dumb machine, designed to serve. Nothing more. | NORA Dislike, SYNTH Hate. Tier 3 wait **+2 days**. **Starts the cruel path** |

SYNTH's reactions to 031–033 apply even though the talk is "aside": she overhears, as companions do in vanilla.

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-N2-040 | NORA | Hmm. My thoughts as well. | Nodding (after 030) |
| P2-N2-041 | NORA | I agree. I'm still a little uneasy with her, but I do like her. | Warm, honest (after 031) |
| P2-N2-042 | NORA | My thoughts exactly. I'll keep an eye on her. | Cool, agreeing (after 032) |
| P2-N2-043 | NORA | I don't trust her. But I also don't think she's a machine. She's something more. | Firm, a little shaken (after 033) |

**SYNTH overhears** (one line, a moment later)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-N2-050 | SYNTH | ...I heard that. Thank you. | Shy, glowing (after 031) |
| P2-N2-051 | SYNTH | Arm's length. Okay. I can work with arm's length. | Hurt but trying (after 032) |
| P2-N2-052 | SYNTH | ... | Silent. She turns away (after 033; no audio, plays a sad idle) |

**Result:** tier 3 starts after the adjusted wait (2 to 5 game days).

---

## Tier 3: Acceptance and basic friendship
They talk more, start complimenting each other, and help each other in combat.

### Ambient: compliments (rare, at most one per game day)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-T3-001 | SYNTH | That was a great shot. | Impressed, genuine |
| P2-T3-002 | NORA | You're not so bad yourself. | Dry, warm underneath |
| P2-T3-010 | NORA | Your hair looks good like that. | Offhand, almost surprised she said it |
| P2-T3-011 | SYNTH | It's your hair. | Teasing |
| P2-T3-012 | NORA | Then it looks *great*. | Deadpan, then a laugh |
| P2-T3-020 | SYNTH | You're good at this. Talking to people. Getting them to listen. | Admiring |
| P2-T3-021 | NORA | Three years of law school. You'd know. | Joking, the first time she's joked about it |

### Combat aid: stimpaks
When one of them is badly hurt in combat, the other uses one of her own stimpaks on her. **Throttled:** at most once per fight and at most once every 5 game minutes, and only below 35% health. The giver needs a stimpak in her own inventory. Gifted stimpaks from the gift system count.

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-CB-001 | SYNTH | Hold still! Stimpak! | Urgent, kneeling over her |
| P2-CB-002 | SYNTH | I've got you. I've got you. | Breathless, in combat |
| P2-CB-010 | NORA | Here. Don't you dare die on me. | Sharp, urgent |
| P2-CB-011 | NORA | Up. Come on, up. | Hauling her, combat breath |
| P2-CB-020 | SYNTH | Thanks. | Winded, grateful (after receiving) |
| P2-CB-021 | NORA | ...Thanks. I owe you one. | Winded (after receiving) |

### SYNTH's tier 3 talk

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-S3-001 | SYNTH | Hello! Can I talk to you? | Bright, a little nervous |

**NATE choices**

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P2-S3-010 | Y | Sure, what's up? | Sure. What's up? | none. Talk continues |
| P2-S3-011 | A | Is something wrong? | Is something wrong? | none. Talk continues |
| P2-S3-012 | B | Not right now. | Not right now. | none. SYNTH asks again next time you talk to her |
| P2-S3-013 | X | What do you want? | What do you want? | SYNTH small Dislike. **She stutters through what follows** |

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-S3-015 | SYNTH | Oh. Okay. Just get back to me soon, okay? | Deflated, covering it (after 012) |
| P2-S3-016 | SYNTH | Oh. I... s-sorry. I'll be quick. | Thrown, stammering (after 013, plays before either branch) |

**Which branch plays**
- **Cruel branch:** you chose tier 1 check-in 013 ("If that's all you're good at") **and/or** tier 2 choice 033 ("Dumb machine").
- **Kind branch:** anything else.
- The **stuttered versions** play after S3-013 ("What do you want?"). The cruel branch already stutters, so only the kind branch has a second recording.

### Cruel branch

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-S3-020 | SYNTH | Hey. I know you... uh. Don't... think that highly of me. But I just want to say thank you. For taking me along with you. | Halting, forcing it out |
| P2-S3-021 | SYNTH | You're... you're still the person I married all those years ago. I love you. But... do you still... even want to be around me? | Barely holding it together |

**NATE choices**

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P2-S3-030 | Y | I still want you around. | I know I've been... mean. But I still want you around. I'm still working through everything that's happened in this world. | NORA Like, SYNTH Love. Tier 4 wait **−1 day** |
| P2-S3-031 | A | I'm sorry. | I've been very cruel to you, and I have no excuse for that. I've been unfair in how I've treated you, and I want to say sorry. You are who you say you are. Just a little different. | NORA Like, SYNTH Love. Tier 4 wait **−2 days**. **Ends the cruel path** |
| P2-S3-032 | X | A useful machine. | Yeah, you're a useful machine. You watch my back and keep my wife alive. Other than that, you're not worth much. Just a poor copy. | NORA Dislike, SYNTH Hate. Tier 4 wait **+2 days** |
| P2-S3-033 | B | That vault was a mistake. | I made a mistake in that vault. I don't even think you're worth keeping around. | NORA Dislike, SYNTH Hate. **Re-opens the Vault 111 choice** (below) |

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-S3-040 | SYNTH | You... mean that? Okay. Okay. We can work through it. Together. | Fragile hope, laughing through tears (after 030) |
| P2-S3-041 | SYNTH | I don't... I don't know what to say. Thank you. I'm going to remember this. I'm good at remembering. | Overwhelmed, a wet laugh (after 031) |
| P2-S3-042 | SYNTH | A poor copy. Right. I'll... I'll keep her alive, then. | Hollow, very quiet (after 032) |

NORA, after 032 (she heard it):

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-S3-045 | NORA | Nate. That's enough. | Hard, quiet, stepping in |

### Kind branch

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-S3-050 | SYNTH | Thanks! Look, I know it was weird seeing... me. Yeah. Me, twice. And now that I understand this world a little better, I know how big a chance you took on me. | Warm, rehearsed but sincere |
| P2-S3-051 | SYNTH | I don't want that to go unsaid. I still see you as my husband. I don't really know what to think of... the other me. But I've enjoyed her company for a while now, and I want to thank you both. | Open, a little shy at the end |
| P2-S3-055 | SYNTH | Th-thanks. Look, I... I know it was weird seeing... me. Yeah. Me, twice. And now that I, um, understand this world a little better, I know how big a chance you took on me. | Stuttered version of 050 (after S3-013), flustered |
| P2-S3-056 | SYNTH | I don't want that to go... unsaid. I still see you as my husband. I d-don't really know what to think of the other me. But I've enjoyed her company for a while, and I want to... to thank you both. | Stuttered version of 051, recovering slowly |

**NATE choices**

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P2-S3-060 | A | I trust you. | Thanks for telling me. I respect you too. I trust you. | NORA Like, SYNTH Like |
| P2-S3-061 | Y | You're your own person. | Of course I still like you. You may not be the original, but you're your own special person. Never let that go. | NORA Love, SYNTH Love. Tier 4 wait **−1 day** |
| P2-S3-062 | X | A useful machine. | Yeah, you're a useful machine. You watch my back and keep my wife alive. Other than that, you're not worth much. Just a poor copy. | NORA Hate, SYNTH Hate. **Starts the cruel path** |
| P2-S3-063 | B | That vault was a mistake. | I made a mistake in that vault. I don't even think you're worth keeping around. | NORA Hate, SYNTH Hate. **Re-opens the Vault 111 choice** (below) |

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-S3-070 | SYNTH | You trust me. Okay. Good. That's... good. | Pleased, steadying (after 060) |
| P2-S3-071 | SYNTH | My own special person. I like the sound of that. I think I'll keep it. | Delighted, tearing up a little (after 061) |
| P2-S3-072 | SYNTH | Oh. I thought... never mind what I thought. | Stunned, closing up (after 062) |
| P2-S3-075 | NORA | Where the hell did that come from? | Angry, disbelieving (after 062) |

### "That vault was a mistake": the Vault 111 choice, re-opened
After S3-033 or S3-063:

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-RV-001 | SYNTH | Then say it. Whatever you're going to do with me, say it. I'd rather know. | Shaking, standing her ground |

The four Phase 1 choices are offered again, with the same labels and lines (P1-S3-010 to 013). Effects for each:

| Choice | What happens | Lines |
|---|---|---|
| **Come with us** (Y) | You take it back. SYNTH stays. NORA Like, SYNTH Like. Tier 4 wait +1 day | RV-010, RV-011 |
| **I need time** (A) | She goes back to Vault 111 to wait (see "Walking back to the vault"). Patience FOMOD option applies | RV-020 |
| **Abomination** (B) | She turns hostile, as in Phase 1 choice 3. NORA Hate | P1 S3-041 audio reused; RV-030 after she dies |
| **Go your own way** (X) | She goes back to Vault 111 (see below), then 3 days later the battle site | RV-040, RV-041 |

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-RV-010 | SYNTH | ...You scared me. Don't do that again. | Shaky relief, half angry |
| P2-RV-011 | NORA | You heard him. Let's go. | Brisk, protective, glaring at Nate |
| P2-RV-020 | SYNTH | I'll go back to the vault. It's the only place I know to wait. | Numb, practical |
| P2-RV-030 | NORA | Was that what you wanted? Was it? | Shaking with anger, not looking at him |
| P2-RV-040 | SYNTH | Okay. I'll go. Take care of her. She's the real thing. | Composed, crying quietly |
| P2-RV-041 | NORA | Nate... no. Not like this. | Pleading, too late |

### Walking back to the vault
For "I need time" and "Go your own way" above.
- SYNTH leaves as a companion and walks (or, if far away, travels off-screen) to Vault 111. Once there, she stays near the cryo pods (her pod, next to the spouse pod).
- **The player is told where she went:**
  - A message shows on screen: *"Synth Nora has gone back to Vault 111."*
  - A short quest objective is added: **"Synth Nora has returned to Vault 111"**, with a map marker on her. It clears when you speak to her there, or when she leaves for good.
- **"I need time":** at the vault, talking to her offers the four choices again, as in Phase 1 choice 2. If the patience option "Leaves after a while" is installed, its 7 days count from her arrival.
- **"Go your own way":** after 3 in-game days she leaves the vault. The battle-site encounter becomes available, same as Phase 1.

---

## She leaves (hurt counter reaches 3)
Plays the next time she's near Nate after the third Hate in Phase 2 scenes.

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-LV-001 | SYNTH | I can't keep doing this. Every time I think I've found a place with you, you remind me what I am. | Tired, past crying |
| P2-LV-002 | SYNTH | I'm going. Don't follow me. Please. | Quiet, final |
| P2-LV-003 | NORA | Nate. Go after her. ...Nate! | Urgent, then angry |

**Result:** she leaves as a companion. A note is left in Nate's inventory (*"Don't look for me"*), and the 3-day timer to the battle site starts. She does not go back to the vault.

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P2-LV-010 | SYNTH | (Note, not voiced) Don't look for me. I know what I am to you. I'm going to go be something to somebody else. Keep her safe. | Written, steady |

---

## Open questions (draft 1)
1. **Tier 2 timing:** I read "after four in-game days" as 4 days after NORA's tier 1 talk. Is that right?
2. **"Yep." in the tier 2 talk:** no reaction, as you asked. Should NORA notice the curt answer (a small sigh, no audio), or carry straight on?
3. **NORA's gifts after CK-012:** how often? I've assumed every 3 days, against SYNTH's daily gifts.
4. **The kind-branch "useful machine" (S3-062):** it starts the cruel path late. It's the only cruel-path start outside tier 2. Keep it?
5. **The leaving note:** OK to add it, or should she go without a word?
