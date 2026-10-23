# Nora and Nora: Phase 4 Script
**Relationship tiers 4 and 5, the broken phase, the duo romance and Eternal Lovers.** Draft 2, 2026-10-23 (your edits), built from
`notes/interaction-ideas.md` and `notes/phase4-decisions.md`. Your own wording is kept; lines marked **(new)** in the
Delivery column are mine, to edit or replace.

## How to read this
Same conventions as the Phase 2 script:
- **NORA** = organic Nora, **SYNTH** = synth Nora, **NATE** = the player (text only).
- Buttons: **[Y]** agree or kind, **[B]** refuse or harsh, **[X]** other, **[A]** ask.
- Line IDs are `P4-<scene>-<number>`. Keep them when editing so voice files stay matched.

## Timeline at a glance

| Step | When | What happens |
|---|---|---|
| Tier 4 | 4 game days after tier 3 is reached, adjusted by the tier 3 talk (−2 to +2 days) | Flirting starts, they get upset when the other is downed. NORA: "Hey, sweetie, can I talk to you?" |
| Tier 5 | 4 game days after NORA's tier 4 talk (3 with "really enjoy having her around", 5 with "I just don't know") | Both approach: "Hey honey, can we talk to you?" Duo romance question |
| Romance asked again | 12 game days after you decline or say you need to think | A greeting from both, then the final question again |
| Broken phase | "She's just a machine" in NORA's tier 4 talk (mean version) | Tier 5 locked. SYNTH only gives flat lines; no reactions, no commentary |

Which version of NORA's tier 4 talk you get: **mean** if the cruel flag is set (tier 1 check-in "If that's all you're
good at" or tier 2 "Dumb machine", and not cleared by "I'm sorry" in the tier 3 talk), otherwise **nice**.

---

## Tier 4: Close

### Ambient (tier 4 and up)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-T4-001 | SYNTH | You know, you're not so bad when you're not glaring at me. | Teasing, toward NORA (new) |
| P4-T4-002 | NORA | Careful. I might start liking you. | Dry, smiling (new) |
| P4-T4-003 | SYNTH | Same hair, same freckles. Somehow it looks better on you. | Flirty (new) |
| P4-T4-004 | NORA | Flatterer. Don't stop. | Amused (new) |

### Combat: when the other one goes down

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-CB-001 | SYNTH | Nora! No, no, no. Get up. Please get up! | Panicked (new) |
| P4-CB-002 | NORA | Hey! Stay with me! Don't you dare! | Panicked (new) |

### NORA's tier 4 talk

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-T4-010 | NORA | Hey, sweetie. Can I talk to you? | Warm, a little serious |

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P4-T4-011 | Y | Everything okay? | Everything okay? | none |
| P4-T4-012 | X | Anything for you. | Anything for you. | none |
| P4-T4-013 | B | Not right now. | Not right now. | Ends the talk; she asks again next time you talk to her |
| P4-T4-014 | A | Sure! | Sure! | none |

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-T4-015 | NORA | Oh, okay. Just get back to me soon, okay? | Disappointed but kind (after "Not right now") |

#### Nice version

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-T4-020 | NORA | Thank you. I've been thinking, and from what I've seen of you, you think the same way. | Earnest |
| P4-T4-021 | NORA | I've come to really enjoy her company, and I think you have too. She's a lot like me in a lot of ways. | Fond |
| P4-T4-022 | NORA | But I've seen her change, too. I see a lot of myself in her, but she's becoming her own person. Her choices, her interests, they're different from mine. | Thoughtful |
| P4-T4-023 | NORA | I'm still not a fan of asking for a lot of money, but she most definitely is. I think she's a real keeper. What do you think? | Laughing, then sincere |

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P4-T4-030 | Y | Agree completely. | Yes, I agree completely. | NORA Like, SYNTH Like |
| P4-T4-031 | X | Really enjoy her. | Honestly, I've come to really enjoy having her around. | NORA Love, SYNTH Love. Tier 5 wait **−1 day** |
| P4-T4-032 | A | Trust your judgment. | I'm still a little uneasy around her, but I trust your judgment. | NORA Like |
| P4-T4-033 | B | Still thinking. | I'm still thinking that through. | none |

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-T4-034 | NORA | I knew it. She'll be glad to hear it. | Happy (after Y or X) (new) |
| P4-T4-035 | NORA | That's fair. Give her time. She'll earn it. | Understanding (after A or B) (new) |

#### Mean version

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-T4-040 | NORA | We need to talk. It's about her. | Serious |
| P4-T4-041 | NORA | I know you don't really see her as a person, and I admit I've been having second thoughts myself. | Careful |
| P4-T4-042 | NORA | It's odd, seeing my own face, my own body, down to my tattoos, on someone else. | Uneasy |
| P4-T4-043 | NORA | But I don't think she's a simple machine. She's something more. I don't think you should be as dismissive of her as you've been. | Firm |
| P4-T4-044 | NORA | Still... she could be on the Institute's side, secretly. What do you think? | Doubtful |

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P4-T4-050 | Y | Too hard on her. | You're right. I think I've been too hard on her. I'll go easier on her. | NORA Like, SYNTH Like. Tier 5 wait 4 days. Clears the cruel flag |
| P4-T4-051 | A | I just don't know. | I just don't know. She looks like you, she sounds like you, but she's not. I don't really know what to think. | none. Tier 5 wait **+1 day** |
| P4-T4-052 | X | Just a machine. | Sweetie, she's just a machine. Those emotions she's feeling are all just calculated. She's not a person, she's a thing. Useful, however. | SYNTH Hate. **Tier 5 locked; broken phase** |
| P4-T4-053 | B | Take her out. | You're right, we can't trust her. She's seen too much. We need to take her out. | NORA Dislike, SYNTH Hate. **SYNTH turns hostile** |

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-T4-054 | NORA | Thank you. That's all I wanted to hear. | Relieved (after Y) (new) |
| P4-T4-055 | NORA | Me neither, honestly. | Quiet (after A) (new) |
| P4-T4-056 | NORA | ...If that's what you really think. | Cold, disappointed (after X) (new) |
| P4-T4-057 | SYNTH | I'm a person! A person! | Screaming, shaking (after B, she turns hostile) |

---

## Tier 5: Together

### Ambient (tier 5)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-T5-001 | SYNTH | Remember that night? The three of us, under the streetlight in the park? | Dreamy, flirty |
| P4-T5-002 | NORA | Which one of us are you asking? | Teasing |
| P4-T5-003 | SYNTH | Both of you. | Laughing |
| P4-T5-004 | NORA | You know she put a radroach in my bedroll last night. | Mock outrage (new) |
| P4-T5-005 | SYNTH | You put my good boots in the river first. | Laughing (new) |
| P4-T5-006 | NORA | You're doing good out here, honey. Really good. | Proud (new) |
| P4-T5-007 | SYNTH | We trust you. Both of us. Don't forget that. | Warm (new) |

### NORA and SYNTH's tier 5 talk

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-T5-010 | NORA | Hey, honey. Can we talk to you? | Nervous, warm |
| P4-T5-011 | SYNTH | Please, honey. It's important. | Nervous |

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P4-T5-012 | Y | What's up? | What's up? | none |
| P4-T5-013 | A | What do you need? | Of course. What do you need? | none |
| P4-T5-014 | X | Anything for you two. | Anything for you two. | none (special replies) |
| P4-T5-015 | B | Not right now. | Not right now. | Ends the talk; they ask again next time |

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-T5-016 | NORA | Oh, okay. Just get back to us soon, okay? | Disappointed (after "Not right now") |
| P4-T5-017 | NORA | Thank you. | Relieved (after Y or A) |
| P4-T5-018 | SYNTH | Anything, huh? Hmm. I can think of a few things. | Flirty (after X) |
| P4-T5-019 | NORA | Same. That's what we want to talk about. | Flirty (after X) |
| P4-T5-020 | NORA | We wanted to talk to you about, well... us. | Nervous |
| P4-T5-021 | SYNTH | Yeah. The three of us. | Nervous |
| P4-T5-022 | NORA | You see, the more we've been traveling, the more... emotions I feel toward both of you. | Vulnerable |
| P4-T5-023 | SYNTH | I feel the same way. | Soft |
| P4-T5-024 | NORA | These feelings in my heart for you, my love, have never been stronger. With all we've seen, done, and been a part of. | Loving, to Nate |
| P4-T5-025 | NORA | Most others would have given up. You just kept going, and going. You held your head high and never stopped. | Loving, proud |

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P4-T5-030 | Y | I love you too. | I love you too. | NORA Love |
| P4-T5-031 | X | Thank you. | Thank you. | NORA Like |
| P4-T5-032 | B | Withhold judgment. | I'll withhold judgment until the end. | none |
| P4-T5-033 | A | Where is this going? | Where are you going with this? | none |

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-T5-040 | NORA | Thanks. But now, there's another thing. Another room in my heart opened. Not just for the two of us, but for three. | Toward SYNTH |
| P4-T5-041 | SYNTH | Same for me. I still love my husband, and that will never, ever change. | Earnest |
| P4-T5-042 | SYNTH | But now I love two people at the same time. I love you too, Nora. And you, my Nate. | Tearful, happy |
| P4-T5-043 | NORA | I love you both as well. It's just... these emotions, these feelings. I don't know how to take them all in. | Overwhelmed |
| P4-T5-044 | NORA | Can I love... Nora, and you, at the same time? | Hopeful, scared |

| ID | Button | Label | Line | Effect |
|---|---|---|---|---|
| P4-T5-050 | Y | I love you both. | Of course! I love both of you. I was terrified I was going to have to choose only one of you. Now I can love you both. | **Duo romance. Unlocks Eternal Lovers.** NORA Love, SYNTH Love |
| P4-T5-051 | B | It's too much. | No, I'm sorry. It's too much for me. I don't know if I can do that. | Declined; asked again in 12 game days |
| P4-T5-052 | X | I need to think. | Oh, uh. I need to think about this. | Ends the talk; asked again in 12 game days |
| P4-T5-053 | A | You two fell in love? | Wait, you two have fallen in love with each other? | Replies, then the choice again |

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-T5-054 | SYNTH | Yes, we have. I know, I'm surprised too. But we didn't fall in love with just us. | Shy, honest (after A) |
| P4-T5-055 | NORA | We fell in love with the three of us. All of us. | Warm (after A) |
| P4-T5-060 | SYNTH | Really? Oh, Nate. | Overjoyed (after Y) (new) |
| P4-T5-061 | NORA | Then it's settled. The three of us. Always. | Tearful, happy (after Y) (new) |
| P4-T5-062 | NORA | We understand. Really, we do. | Sad but kind (after B) (new) |
| P4-T5-063 | SYNTH | We're not going anywhere. | Gentle (after B) (new) |
| P4-T5-064 | NORA | Take your time, honey. We'll be here. | Gentle (after X) (new) |

### Asked again (12 game days after B or X)

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-T5-070 | NORA | Honey... have you thought any more about us? All three of us? | Hopeful, careful (new) |
| P4-T5-071 | SYNTH | We'd understand if the answer's still no. | Quiet (new) |

Then the four choices P4-T5-050 to 053 again.

### Eternal Lovers (perk, on "I love you both")
> You understand what love is, no matter what form, where they are from, or who they are. Thanks to your relationship
> with both Noras, they each gain 100 hit points, and you heal 1 HP per second and take 50% less fire, cryo and poison
> damage.

Permanent once unlocked, like a vanilla companion perk.

### After tier 5: talks about the future

Ambient conversations between the two, at most one per game day. Which "kids" talk plays depends on Shaun.

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-FU-001 | SYNTH | I want to have a lot of kids. | Dreamy |
| P4-FU-002 | NORA | Really? How many? | Curious |
| P4-FU-003 | SYNTH | Ten. Maybe eight. | Serious |
| P4-FU-004 | NORA | That many!? Why? | Shocked, laughing |
| P4-FU-005 | SYNTH | The idea of that many little ones in me, and then running around my feet... it fills my heart with joy. | Glowing |
| P4-FU-006 | NORA | Dang. I just wanted one, or three more. You have ambition. | Laughing |
| P4-FU-007 | SYNTH | Thanks. | Proud |
| P4-FU-010 | SYNTH | When this is all over, I want us to settle down somewhere. A real family. The three of us. | Hopeful (new) |
| P4-FU-011 | NORA | I'd open a law office. Somebody has to bring some law back to the Commonwealth. | Determined (new) |
| P4-FU-012 | NORA | And I want to take up hunting. | Playful (new) |
| P4-FU-013 | SYNTH | I don't even know if I can have children. What I am... | Worried (new) |
| P4-FU-014 | NORA | Then we'll figure it out together. | Reassuring (new) |
| P4-FU-020 | NORA | I want to find our baby first. Before I can even think about a family again. | Determined (Shaun still missing) (new) |
| P4-FU-021 | SYNTH | I understand. We'll find him. | Gentle (Shaun still missing) (new) |
| P4-FU-030 | NORA | I found my baby boy, and he's an old man running the Institute. I don't know how to think about new kids after that. | Conflicted (Shaun found, alive) (new) |
| P4-FU-031 | SYNTH | I understand. I just hope you'll think about it. | Hopeful (Shaun found, alive) (new) |
| P4-FU-040 | NORA | I think having kids again will take some time. I'm still healing. But when I'm ready... I'd happily have a few. | Tender (Shaun dead) (new) |
| P4-FU-041 | SYNTH | Me too. A lot of them. | Warm (Shaun dead) (new) |

---

## The broken phase

From "She's just a machine" in NORA's tier 4 talk. Tier 5 is locked. SYNTH's greeting and idle lines are replaced by
these; she has no likes or dislikes any more and makes no comments.

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-BR-001 | SYNTH | Yes, sir. | Flat, robotic |
| P4-BR-002 | SYNTH | Affirmative, sir. | Flat, robotic |
| P4-BR-003 | SYNTH | Understood. | Flat (new) |
| P4-BR-004 | SYNTH | As you wish. | Flat (new) |
| P4-BR-005 | SYNTH | Awaiting instructions. | Flat (new) |
| P4-BR-006 | NORA | What did you do to her? | Horrified, quiet (once, after the broken phase starts) (new) |

---

## Synth Nora's own romance (Synthetic Love's romance)

When you romance synth Nora on her own (her mod's romance, separate from the duo romance). Romance only if you were kind
to her the entire time.

| ID | Speaker | Line | Delivery |
|---|---|---|---|
| P4-RO-001 | SYNTH | Yes! Yes! I love you too. I know I'm not your original love... or am I? Gosh, this synth thing is so confusing. | Overjoyed, laughing |
| P4-RO-002 | SYNTH | I will love you no matter what. Let's have the largest family the wasteland has ever seen! I love you so much. | Overjoyed |
| P4-RO-010 | NORA | You're doing what? With her? No. No! | Hurt, angry (tier 3 or lower: NORA Hates) (new) |
| P4-RO-011 | NORA | Wait... you're marrying her? Why? I'm right here. | Confused (tier 4) (new) |
| P4-RO-012 | NORA | Oh, I love this. And I'll help with that large family. Count me in. | Delighted (tier 5: NORA Loves) |

## Decided
1. "I need to think about this" in the tier 5 talk: asked again after 12 game days, the same as declining.
2. Synth Nora's own romance: hooked into Synthetic Love's romance wherever it happens in its files; the lines above
   play then.
