# 08 — Quest reactions: both Noras

Working copy: the "Quest Reactions: Both Noras" doc on claude.ai (https://claude.ai/artifact/JzY9BhF5k8NVXbCXY4qeTS).
Read from the game files (2026-10-22): Nora Spouse's `CompanionNoraAffinity` script, vanilla reaction points in Fallout4.esm
(`CA_DialogueBump_TopicInfoScript` lines and `CA_QuestStage_Bump` stages), and the game's string tables for the line text.

- **Real Nora:** 644 reactions across 108 quests and places (44 Loves, 280 Likes, 234 Dislikes, 86 Hates). Neutral moments left out.
- **Synth Nora:** Synthetic Love fills in none of vanilla's per-quest reaction points. She reacts only to generic events:
  settlement help (Likes) / refusal (Dislikes), Institute evacuation in The Nuclear Option (Likes), the selfish outcome of
  Diamond City Blues (Dislikes, via her Selfish trait), everyday actions (see 07), and this mod's scenes.
- Far Harbor, Nuka-World and Automatron: neither mod adds reactions there.

## Real Nora: main quest
| Quest | You pick / outcome | Real Nora |
| --- | --- | --- |
| **Dangerous Minds (memories)** | Quest outcome (stage 1100) | Likes |
| **Getting a Clue** | "Please, all I want to do is find my son. The man who owned that house kidnapped him." | Likes |
|  | "Please, all I want to do is find my baby. The man who owned that house kidnapped him." | Likes |
|  | "Please, Mayor McDonough. This man Kellogg kidnapped my son. I need to find him." | Likes |
|  | "Please, Mayor McDonough. This man Kellogg kidnapped my baby. I need to find him." | Likes |
|  | "Don't lie to me, Nick. You're one of them. They made you." | Dislikes |
| **The Enemy of My Enemy** | "Doesn't matter what he knew. I'd kill him again in a heartbeat." | Likes |
|  | "I was so blinded by anger.... I just wanted him dead. Now look what I've done." | Likes |
|  | "Bullshit. You're a synth, Valentine! Tell me what you know!" | Dislikes |
| **The Nuclear Option** | Quest outcome | Loves |
| **The Nuclear Option (Brotherhood)** | "It's none of your damned business Ingram. Now get us out of here." | Hates |
|  | "He's a synth, Ingram. He's not really my son." | Hates |
|  | "We don't have time for this, Proctor. Get us out of here." | Hates |
|  | (line not found) | Hates |
| **The Nuclear Option (Minutemen)** | "There's no time to argue about this. Activate the relay." | Dislikes |
|  | "It's none of your goddamn business, Sturges. Activate the relay." | Hates |
|  | "He's not my son. He's a synth." | Hates |
|  | "Is there a problem, Sturges?" | Hates |
| **The Nuclear Option (Railroad)** | "We're going to pull this off." | Likes |
|  | "He's not my son, Tom. He's a synth." | Hates |
|  | "It's none of your damned business, Tom. Get this thing running." | Hates |
|  | "There's no time to argue, Tom. Get this thing running now." | Hates |
| **Unlikely Valentine** | "This is all just a misunderstanding, Skinny. You know that. You let us walk and we won't come back." | Likes |
|  | "Darla, listen to me. You have a home to go back to. You don't want to throw your life away with these thugs." | Likes |
|  | "Look at yourself. Darla is playing you for a sap. You're better than this. You're better than her." | Likes |
|  | "That wasn't the plan originally, but hey, tempting." | Dislikes |
|  | "You're fat, you're ugly, and it's time you and your crazy bitch said goodbye." | Hates |
|  | "Skinny's no good for you, Darla. You put a bullet in him, and I just might let you go." | Hates |
## Real Nora: faction quests
### Minutemen

| Quest | You pick / outcome | Real Nora |
| --- | --- | --- |
| **Defend The Castle** | Quest outcome (stage 400) | Likes |
| **Form Ranks** | Quest outcome (stage 50) | Likes |
| **Inside Job** | Outcome: I ran the Network Scanner holotape on the Institute computer network. Sturges is now analyzing the data for any useful intelligence on the Institute. | Likes |
| **Old Guns** | "Easy. I just didn't know there were any other Minutemen out there." | Likes |
|  | Outcome: I've built and successfully test-fired the artillery at the Castle. I can now call in artillery fire from nearby batteries with the smoke grenades from the Castle armory. | Likes |
|  | "I'd like to see you try." | Dislikes |
| **Resettle Refugees** | "I'm not going to help you. You're on your own." | Dislikes |
| **Returning the Favor** | "Whatever the Minutemen need, you can count on us. We got a decent workshop here, and Connie's sure to go leaner on her prices after what you've done." | Likes |
|  | "I'm sure she'll go lean on her prices after what you've done. And feel free to use our workshop. Least we can do." | Likes |
| **Sanctuary** | Outcome: Sanctuary is well on its way to becoming a thriving settlement. | Likes |
|  | "Okay. I'll do it." | Likes |
|  | "I'd be glad to help." | Likes |
|  | "I'd be glad to help. Just tell me what you need." | Likes |
|  | "No. I'm not your savior. I have my own problems to deal with." | Dislikes |
| **Taking Independence** | Outcome: The Castle is back under out control, and Radio Freedom can now broadcast across the whole Commonwealth. | Likes |

### Railroad

| Quest | You pick / outcome | Real Nora |
| --- | --- | --- |
| **Boston After Dark** | Outcome: I safely got High Rise and H2-22 to Ticonderoga Safehouse. It's time to report back to Doctor Carrington. | Likes |
|  | "A trader always has to move his merchandise efficiently." | Likes |
|  | "I didn't sign up to babysit your ass." | Likes |
|  | "He may have a good reason to be paranoid." | Likes |
|  | "So, is there anyone you like?" | Dislikes |
| **Concierge** | "You lose your nerve? You know the risks we take in this line of work." | Dislikes |
| **Memory Interrupted** | Outcome: Glory has accidentally been given the same job. So the two of us are going to eliminate the Gen 1s in Malden Center. After we've done that H2-22 can be safely moved from the Memory Den. | Likes |
|  | "I didn't get a chance to say goodbye." | Likes |
|  | Quest outcome (stage 360) | Dislikes |
| **Mercer Safehouse** | Outcome: Mercer Safehouse is fortified and clear of hostiles. Time to let PAM know the good news. | Likes |
| **Precipice of War** | "Relax, Tom, you'll be all right." | Likes |
|  | "Another of your paranoid fantasies." | Dislikes |
| **Railroad (late game)** | Quest outcome | Likes |
| **Railroad HQ** | "Hit me, Tom." | Dislikes |
| **Road to Freedom** | "I risk my life for people every day. Makes no difference to me if it's a human or a synth." | Likes |
|  | "Once I pledged my life to protect my countrymen. I don't see this as any different." | Likes |
|  | "The Institute's going to pay for what they've done to my family." | Likes |
|  | "I don't want anyone else to suffer at their hands." | Likes |
|  | Quest outcome (stage 130) | Dislikes |
|  | Quest outcome (stage 609) | Dislikes |
|  | "No, probably not." | Dislikes |
| **Rockets' Red Glare** | "I promise." | Loves |
|  | Quest outcome (stage 940) | Likes |
|  | Quest outcome | Likes |
|  | "Hold on, you'll make it through." | Likes |
|  | "I don't have time for this." | Hates |
| **To the Mattresses** | Outcome: With the fall of Captain Sally, the L&L Gang has finally been put down. Everyone back at HQ, especially Desdemona, will want to hear this. | Loves |
|  | "I miss Glory, too, Desdemona." | Likes |
| **Tradecraft** | "I appreciate all you've done." | Likes |
|  | Outcome: I impressed Desdemona enough with my actions at Switchboard that she asked me to join the Railroad. | Likes |
|  | "I'm not asking for you to commit suicide, Ricky." | Likes |
|  | "Mostly true. But there wasn't a 100 of them and Deacon was with me the whole way." | Likes |
|  | "Someone has to stop them." | Likes |
|  | "Whether it's synths or humans I'm against slavery." | Likes |
|  | "Ease up there, pal, or we're going to have a problem." | Dislikes |
|  | "Your sacrifice will never be forgotten, Ricky." | Dislikes |
|  | "Every word he said was true and then some." | Dislikes |
|  | "No, I have no problem with the Institute." | Dislikes |
|  | "I don't think you can enslave a machine." | Dislikes |
| **Weathervane** | "I can't believe Dez approved this hare-brained scheme." | Dislikes |

### Brotherhood of Steel

| Quest | You pick / outcome | Real Nora |
| --- | --- | --- |
| **Blind Betrayal** | "I won't do it. Danse deserves a chance to explain himself." | Loves |
|  | Outcome: I've decided to allow Paladin Danse to live, but he needs to flee the Commonwealth immediately. I should escort him outside the bunker to make sure he leaves safely. | Loves |
|  | "No. I won't do it, Danse." | Loves |
|  | "After all the sacrifices I've made and all the battles I've fought for the Brotherhood, you need to listen to me. You owe me that much." | Loves |
|  | "I can't do it, Danse. It's not right." | Loves |
|  | Quest outcome (stage 160) | Likes |
|  | "Isn't there some other way?" | Likes |
|  | "All right, I'll hear him out." | Likes |
|  | Outcome: Paladin Danse is dead. I should retrieve his holotags to use as proof of his demise. | Dislikes |
|  | "I don't know what to say." | Dislikes |
|  | Outcome: Paladin Danse is dead. I should speak to Elder Maxson as soon as possible. | Dislikes |
|  | "I'm not making any promises." | Dislikes |
|  | "With pleasure. I'll make him pay for lying to us." | Hates |
|  | "If it needs to be done, then so be it." | Hates |
|  | "For the good of the Brotherhood, he needs to die... but I won't pull the trigger myself." | Hates |
|  | "For the good of the Brotherhood, he needs to die." | Hates |
| **Call to Arms** | "No, I need to move on." | Likes |
|  | "I'd be honored to join." | Likes |
| **Duty or Dishonor** | "They're a threat to the base. They have to be destroyed." | Likes |
|  | "I have to report this. When I do, they'll come for you. You need to get away before that happens." | Likes |
|  | "We do what the Brotherhood expects of us. We eradicate them." | Likes |
|  | "No." | Likes |
|  | (line not found) | Likes |
|  | "I won't say anything." | Dislikes |
|  | "Yes." | Dislikes |
|  | Outcome: Initiate Clarke was stealing rations to feed the ghouls in the airport ruins. I need to report his death to Captain Kells. | Hates |
|  | "You've betrayed the Brotherhood of Steel. That's unforgivable." | Hates |
| **Feeding the Troops** | "Donate a portion of your crops to the Brotherhood, and it will not be forgotten." | Likes |
|  | "Deal." | Likes |
|  | "The Brotherhood needs food. Better to donate it willingly and keep them friendly." | Likes |
|  | "No deal." | Dislikes |
|  | "How about 500 caps?" | Dislikes |
|  | "You will hand over a portion of your crops to the Brotherhood." | Dislikes |
|  | Quest outcome (stage 35) | Hates |
| **Fire Support** | "I'll continue to help, but you owe me an explanation first." | Likes |
|  | "At this rate, you'll be dead within two days. And I want no part of it." | Likes |
|  | "That all depends. How much are you paying?" | Dislikes |
| **From Within** | Outcome: Doctor Li has been killed. I should return to Elder Maxson with the bad news. | Hates |
| **Liberty Reprimed** | Outcome: I was able to convince Doctor Li to work on Liberty Prime without incident. I should inform Proctor Ingram of my progress. | Likes |
|  | "If not for the Brotherhood, do it for Doctor Virgil." | Likes |
|  | "Help us end the Institute's greed." | Likes |
|  | Quest outcome (stage 176) | Likes |
|  | "Because we care what happens to the Commonwealth." | Likes |
|  | "If something's wrong, maybe I can help." | Likes |
|  | Outcome: In order for her to agree to work on Liberty Prime, I was forced to threaten Doctor Li. I should inform Proctor Ingram of my progress. | Dislikes |
|  | Quest outcome (stage 178) | Dislikes |
|  | "I don't care about that. I'm looking for Professor Scara." | Dislikes |
|  | "If you don't work on Prime, I'll have you shot." | Hates |
| **Outside the Wire** | Outcome: I've given Proctor Ingram the holotape filled with the Institute's encrypted data. | Likes |
| **Shadow of Steel** | "If you cared about them, you'd leave them to their own devices." | Likes |
|  | "Going to be a quick war with that thing on our side." | Likes |
|  | "I'm guessing that diplomacy isn't on Elder Maxson's mind." | Likes |
|  | "After rolling that thing in, you've certainly started a war." | Likes |
|  | "I can see that. They're playing with fire, and we need to save them." | Dislikes |
| **Show No Mercy** | Outcome: Elder Maxson was pleased with my work at Fort Strong and has provided me with Vertibird Signal Grenades to call in a vertibird if I need it for travel. | Likes |
|  | "Consider it done." | Likes |
|  | "Absolutely. Wiping them out was a pleasure." | Likes |
|  | "This seems like a waste of time." | Dislikes |
|  | "They're no different from anyone else." | Dislikes |
| **Spoils of War** | "Fair enough. It would be helpful to have you along." | Likes |
|  | "It would be helpful if you tagged along." | Likes |
| **The Lost Patrol** | Quest outcome (stage 120) | Likes |
|  | "Drop the gun, and we'll talk." | Likes |
|  | "They're dead, Paladin. I recovered their tags." | Likes |
|  | "They're dead. I'm sorry." | Likes |
|  | "I'm not sure." | Dislikes |
|  | "Is that all?" | Dislikes |
|  | Quest outcome (stage 145) | Hates |

### Institute

| Quest | You pick / outcome | Real Nora |
| --- | --- | --- |
| **A House Divided** | "I know you're angry, but there's a better way to handle this." | Likes |
|  | "Can we talk about this?" | Likes |
|  | "Put them on probation. Limit their access to quarters and non-working areas." | Likes |
|  | "You're beaten, Doctor Higgs. Your plan failed, Now open the door." | Likes |
|  | "There's no need to drag this out. I believe they learned their lesson." | Likes |
|  | "I had a more direct solution in mind." | Dislikes |
|  | "I'm ending this right now." | Dislikes |
|  | "They were prepared to let everyone starve to death. They have to die." | Dislikes |
| **Airship Down** | Outcome: It's over. The Brotherhood has been annihilated. I can safely return to the Institute. | Hates |
| **Appropriation** | Outcome: I've acquired some Brotherhood of Steel blueprints, and now I need to take them to Doctor Watson. | Dislikes |
| **Building a Better Crop** | Quest outcome (stage 70) | Loves |
|  | "They just need to be convinced Bill's wrong. That won't be hard." | Likes |
|  | "A man's life is at stake, and you're fishing for a bribe? You're pathetic." | Likes |
|  | "I know you're in a tough situation here, but lives are at stake. Please help me." | Likes |
|  | Quest outcome (stage 90) | Dislikes |
|  | "They aren't your wife and kids. Don't lose perspective here." | Dislikes |
|  | "Jesus, what a mess. You've really screwed up." | Dislikes |
|  | "If that what it takes, fine." | Dislikes |
| **End of the Line** | "Of course I'm not going to go through with it. So how do I deal with it?" | Loves |
|  | "You're alive, so what do you think?" | Loves |
|  | "I'm afraid you all have to die." | Hates |
| **Pinned** | "The Institute wants the same things you do. We can find a way to work together." | Likes |
|  | "Far as I can tell, you were only in "harm's way" because you screwed this up." | Dislikes |
|  | "Oh screw you. There are plenty of things I'd rather have done than come fix your mess." | Dislikes |
|  | "I know for a fact they won't hurt that man, and if you get in the way, I'm going to have to take you down." | Hates |
|  | "I'm here for the Institute, not for you." | Hates |
| **Plugging a Leak** | "Hold on. Let's just talk about this." | Likes |
|  | "Put that gun away, now." | Likes |
|  | "Skip to the part where this has anything to do with me." | Dislikes |
|  | "Maybe if you offered me the right incentive..." | Dislikes |
| **Political Leanings** | Quest outcome (stage 40) | Dislikes |
| **Reclamation** | Quest outcome (stage 40) | Dislikes |
| **Synth Retention** | "On second thought, nah." | Loves |
|  | "I'm not going to destroy this man's identity and free will. Killing him would be more humane." | Loves |
|  | "You have my word. Give me you what you've got, and we'll leave." | Likes |
|  | "Good, I'd like to avoid any unnecessary violence." | Likes |
|  | "Hell no. I'll think just take what I want." | Dislikes |

## Real Nora: side quests
| Quest | You pick / outcome | Real Nora |
| --- | --- | --- |
| **Cambridge Polymer Labs** | Quest outcome (stage 100) | Likes |
| **Charles View Amphitheater (cult)** | "I'm a friend of the family. Maybe I can talk some sense into her." | Likes |
|  | "I'm going to see her, one way or another. Your choice." | Dislikes |
|  | "I killed the last guy who was running this scam. In case that matters to you." | Dislikes |
|  | "Okay, fine. Here's everything I've got." | Hates |
|  | "Here, this is everything I have." | Hates |
| **Confidence Man** | "Don't worry. I've got your back." | Likes |
|  | "Definitely. We'll be fine." | Likes |
|  | "Just keep a cool head, okay? Don't think about it too much." | Likes |
|  | "You're an idiot for dealing with these goons in the first place." | Likes |
|  | "You're welcome, Vadim. We weren't going to leave you to these guys." | Likes |
|  | "You came through it all pretty well, Travis. That's good to hear." | Likes |
|  | "Are you serious?" | Likes |
|  | "That's a horrible idea." | Likes |
|  | "I'm not some thug. I don't get involved in stuff like that." | Likes |
|  | "Look, Vadim's had dealings with those guys before. Why they took him doesn't matter. Getting him back does." | Likes |
|  | "No, Travis. This is between Vadim and those men. It's not your fault." | Likes |
|  | "Don't be such a coward." | Dislikes |
|  | "Not likely. Chances are at least one of us won't make it out of this alive." | Dislikes |
|  | "I hope so. I'm tired of your shitty, whiny attitude." | Dislikes |
|  | "I guess that'd be one way to handle it." | Dislikes |
|  | "Look, either you can go visit Travis, or you can go visit the doctor. Your choice." | Dislikes |
|  | "Yes. This is absolutely your fault, and it's on your head if something happens to Vadim. So start talking." | Dislikes |
|  | "Sounds good to me." | Hates |
| **Dependency** | "You need to get help, Bobby. Go see Rachel. She has medicine that will treat you." | Likes |
|  | "You're right. He needs help." | Likes |
|  | "You're just a waste of space. I could care less what you do." | Dislikes |
|  | "Here. Have some Jet. On the house." | Dislikes |
|  | "Let him die. One less junkie in the Commonwealth." | Dislikes |
|  | "He's a lost cause." | Dislikes |
| **Diamond City Blues** | "Paul, put the gun away. Nobody needs to get shot here." | Loves |
|  | "Put the guns away before this gets out of hand." | Loves |
|  | (line not found) | Likes |
|  | "I'm sorry he's dead. Things just got out of hand." | Likes |
|  | "Why don't you see if Cooke is going to listen?" | Likes |
|  | "She's not going to come kill us." | Likes |
|  | "I'm not doing it. You do whatever you want." | Likes |
|  | "That works for me." | Likes |
|  | "Stay calm. There's no need to panic." | Likes |
|  | "You'll have to find someone else for this one." | Likes |
|  | "I promise." | Likes |
|  | "And you promise to not tell Marowski that I had anything to do with this?" | Likes |
|  | "Still not interested." | Likes |
|  | "Okay, I'll let you go." | Likes |
|  | "I did all the work, so I'm keeping everything I got." | Dislikes |
|  | "Sorry, I barely know the guy." | Dislikes |
|  | "I haven't seen him." | Dislikes |
|  | "Neslon was a punk who was in way over his head. Good riddance." | Dislikes |
|  | "You'll have to find someone else for this one." | Dislikes |
|  | "Find someone else to be your assassin." | Dislikes |
|  | "I'll do it." | Dislikes |
|  | "70-30 seems more like it." | Dislikes |
|  | "I heard Paul Pembroke ambushed him during some kind of chem deal." | Dislikes |
|  | "No. I'm taking all of it as the rest of my payment." | Dislikes |
|  | "I'll definitely kill you if you don't tell me." | Dislikes |
|  | "I heard it was Marowski. Nelson was buying chems from him." | Dislikes |
|  | (line not found) | Dislikes |
|  | "You can do better than that. 200 and you've got a deal." | Hates |
|  | "Better just shoot him, Paul." | Hates |
|  | "You should be the one to do it." | Hates |
|  | "Throw in another 200 caps and I'll take care of Marowski for you." | Hates |
|  | "The simple solution is just to kill her." | Hates |
|  | "Maybe we should kill her first." | Hates |
|  | "You've got a deal. Marowski's as good as dead." | Hates |
|  | "Make it worth my while. 300 caps." | Hates |
|  | "You've got a deal. Paul is as good as dead." | Hates |
| **Egret Tours Marina** | Quest outcome (stage 11) | Likes |
|  | Quest outcome (stage 202) | Likes |
|  | Quest outcome (stage 203) | Likes |
|  | Quest outcome (stage 510) | Likes |
|  | Quest outcome (stage 512) | Likes |
|  | Quest outcome (stage 514) | Likes |
|  | Quest outcome (stage 20) | Dislikes |
|  | Quest outcome (stage 201) | Dislikes |
|  | Quest outcome (stage 511) | Dislikes |
|  | Quest outcome (stage 701) | Dislikes |
|  | Quest outcome (stage 703) | Dislikes |
|  | Quest outcome (stage 702) | Hates |
| **Egret Tours Marina (afterwards)** | Quest outcome (stage 25) | Likes |
|  | Quest outcome (stage 15) | Hates |
| **Gun Run** | Quest outcome (stage 90) | Likes |
|  | Quest outcome (stage 100) | Hates |
| **HalluciGen, Inc.** | "I don't know what's going on, but you need to get out of here. Now!" | Likes |
|  | "It's okay. I'm a friend." | Likes |
|  | "Open the damn door, or I'll break it down." | Dislikes |
| **Here Kitty, Kitty** | "That's all?" | Dislikes |
|  | Quest outcome (stage 400) | Hates |
| **Hole in the Wall** | "Here. Take the cure and use it on the boy." | Loves |
|  | "Give him half, and I'll take the other half." | Dislikes |
|  | "There's only one dose. I got bit and infected by one of those damn mole rats. I'm going to use it on myself." | Hates |
|  | "Let him die. I'm keeping it." | Hates |
| **Human Error** | "That's a deal I won't accept." | Loves |
|  | "You can't seriously want to kill all the synths..." | Loves |
|  | Quest outcome (stage 450) | Likes |
|  | "I'm here to rescue the survivors from Stockton's caravan." | Likes |
|  | "That's fair. They're at some compound nearby." | Likes |
|  | "I just want answers. About Stockton's caravan. Nothing more." | Likes |
|  | "I'm not interested in your deal." | Likes |
|  | "I just want to talk with whoever's in charge here. I'm sure we can come to an arrangement." | Likes |
|  | "You can keep your caps." | Likes |
|  | "Surely, there's room for compromise? I get Stockton's survivors and we stay... friends. I'd have to know more, though." | Likes |
|  | "Don't kill the girl. Spare her." | Likes |
|  | "Someone needs to destroy the Institute." | Likes |
|  | Quest outcome (stage 90) | Dislikes |
|  | "I did more than half the work on this job. My share should reflect that." | Dislikes |
|  | "No deal." | Dislikes |
|  | "I'll take the deal." | Dislikes |
|  | "I'm coming in one way or the other. At least with the easy way you still get to breathe." | Dislikes |
|  | "Give me the caps and I'll drop the whole thing." | Dislikes |
|  | Quest outcome (stage 490) | Hates |
|  | "Continue your work, then." | Hates |
| **In Sheep's Clothing** | "Quick. Take this Stimpak." | Loves |
|  | "You're going to stand trial, and these people are going to have justice." | Loves |
|  | "Doctor, come quick. Danny Sullivan's been shot." | Likes |
|  | "Doctor, I need your help. Someone's been shot." | Likes |
|  | "Fine. Get out of here and don't come back." | Likes |
|  | "Mayor McDonough, I can help you, but not when you're holding a hostage. Let her go." | Likes |
|  | "Hell, I'd vote for him again." | Dislikes |
|  | "Time to shut you up for good." | Dislikes |
|  | "Goodbye, McDonough." | Dislikes |
|  | "Just let go. It'll all be over soon." | Hates |
| **Kid in a Fridge** | "Then let's go find your home." | Loves |
|  | "No. What kind of person are you?" | Loves |
|  | "Never. Billy stays with me." | Loves |
|  | "Over my dead body. These people are under my protection." | Loves |
|  | "I think I'll just keep him." | Loves |
|  | "The house is empty. Looks like they left in a hurry." | Likes |
|  | "I hate to tell you this, but your parents are probably dead." | Dislikes |
|  | Quest outcome (stage 45) | Hates |
|  | "You'll have to figure out your own life." | Hates |
|  | "Only 200 caps? You can do better." | Hates |
|  | "Sold. Kid, I found you a new home." | Hates |
|  | "You can have them. Why should I risk my life?" | Hates |
|  | "How about I sell them to you?" | Hates |
| **Last Voyage of the U.S.S. Constitution** | "A sad state of affairs for such an historic ship." | Likes |
|  | Quest outcome (stage 950) | Likes |
|  | "I changed my mind. I'm not going to work with you." | Likes |
|  | "Surely, we can work something out." | Likes |
|  | "No deal. I'm with Ironsides." | Likes |
|  | "This must be a misunderstanding. You invited me aboard." | Likes |
|  | "Whoa, whoa. Easy there." | Likes |
|  | "You should just abandon the ship." | Dislikes |
|  | Outcome: Mandy Stiles sabotaged the Turbopump Bearings. Now I just need to install them in the rocket and report to Ironsides. | Dislikes |
|  | "Here you go." | Dislikes |
|  | "Fine. Take it." | Dislikes |
|  | "Yeah, I'm in. What's the plan?" | Dislikes |
|  | "Try that and you'll be nothing but scrap metal, pal." | Dislikes |
| **Long Time Coming** | Outcome: Nick and I killed Eddie Winter. Now Nick says he has one more thing to take care of. Suppose I should follow his lead. | Likes |
| **Mystery Meat** | Quest outcome (stage 25) | Loves |
|  | Quest outcome (stage 951) | Likes |
|  | Outcome: I cut a deal with Theodore and he has agreed to give me a cut of the profit in exchange for sparing him and looking the other way about using ghoul meat in the cans. | Dislikes |
|  | Quest outcome (stage 955) | Hates |
| **Nuka-Cola Needs** | "Here you go." | Likes |
|  | "I'm... gonna go..." | Dislikes |
|  | "Drink. Some. Water." | Dislikes |
| **Out of the Fire** | Outcome: I've helped reunite Jake and his father. I should speak with Abraham. | Likes |
|  | Quest outcome (stage 55) | Dislikes |
|  | Quest outcome (stage 501) | Dislikes |
|  | Quest outcome (stage 504) | Dislikes |
|  | Quest outcome (stage 722) | Dislikes |
|  | Quest outcome (stage 350) | Hates |
|  | Quest outcome (stage 502) | Hates |
|  | Quest outcome (stage 503) | Hates |
|  | Quest outcome (stage 505) | Hates |
| **Painting the Town** | "Actually, I already have some paint right here." | Likes |
|  | "Paint retrieval. I'm on it." | Likes |
|  | "Happy to help. It's been an honor." | Likes |
|  | "Don't worry. I won't." | Likes |
|  | "Forget you, pal." | Dislikes |
|  | "People don't like it, too bad." | Dislikes |
|  | "Fetch work? Do it yourself." | Dislikes |
|  | ""The Wall seems happy with it?" Oh god." | Dislikes |
|  | "This is the part where I get paid." | Dislikes |
|  | "Only if you throw in some more money." | Dislikes |
| **Pickman's Gift** | Outcome: I saved the killer Pickman, and to thank me, he gave me a key to the safe in his gallery. | Dislikes |
| **Prep School** | Quest outcome (stage 200) | Loves |
| **Quincy Ruins** | Quest outcome (stage 100) | Likes |
| **Recruiting Hancock** | "If you leave your caps and run, I'll take them to Hancock and say I put you down. No one has to die." | Likes |
|  | "You don't have to worry. I'll figure out some way to make things right with Hancock." | Likes |
|  | "I don't have time to run your errands for you." | Likes |
|  | "I'll take care of it." | Dislikes |
|  | Quest outcome (stage 30) | Hates |
|  | (line not found) | Hates |
| **Rotten Landfill** | Quest outcome (stage 220) | Likes |
| **Story of the Century** | "No matter how much you want to give up, don't. You have to have hope. That you'll see them again. Or at least, that you'll know the truth." | Loves |
|  | "Honestly, seeing everyone surviving out here? Rebuilding the world? It gives me hope." | Likes |
|  | "You can only take it one day at a time. Just keep going. That's all anyone can do." | Likes |
|  | "I've been having too much fun blowing things up to think about it." | Dislikes |
|  | "Find who's responsible, and make them pay. Simple as that." | Dislikes |
| **The Big Dig** | "Come on Bobbi, at least if we leave now we leave with our lives." | Likes |
|  | Quest outcome (stage 260) | Dislikes |
|  | "I think I deserve a bigger cut for my role in all this. " | Dislikes |
|  | "You can do better than that." | Dislikes |
|  | "I'm in." | Dislikes |
|  | "You can let Mel out of here or I will break him out. Your choice." | Dislikes |
|  | "You lied to us, Bobbi. And you have to pay. " | Dislikes |
|  | "I am going to see this through, Bobbi." | Dislikes |
| **The Devil's Due** | Outcome: I returned what the Gunners stole and took the Deathclaw egg back to its nest. | Likes |
| **The Devil's Due (afterwards)** | Quest outcome (stage 30) | Likes |
| **The Disappearing Act** | "You've killed a man, doctor. You're going to pay for it. Put the gun down, and come with me." | Likes |
|  | "You made a mistake, but you can still do the right thing, doctor. Just think this through." | Likes |
|  | "Look, I need to get down there. Now are you gonna help me or not?" | Dislikes |
|  | Quest outcome (stage 60) | Hates |
|  | (line not found) | Hates |
| **The Gilded Grasshopper** | Outcome: I've uncovered the secret of the Gilded Grasshopper - Shem Drowne hid his treasure in his own grave. And now it's mine. | Likes |
| **The Marowski Heist** | "Here, it's yours." | Likes |
|  | "No, not interested." | Dislikes |
|  | "No, we're done." | Dislikes |
|  | "I think it's worth a lot more than that." | Dislikes |
|  | "Yeah, I'll do it." | Hates |
|  | "Sure." | Hates |
|  | "I'll do it for 400 each." | Hates |
|  | "I'll do it for 400." | Hates |
| **The Secret of Cabot House** | "Thanks for your help." | Likes |
|  | "Sorry, I shouldn't have said that." | Likes |
|  | "I have a vial of that serum with me. Here, looks like you need it." | Likes |
|  | "I'm sorry about Lorenzo." | Likes |
|  | "So you've just been waiting for me to show up to do something about those assholes?" | Dislikes |
|  | Quest outcome (stage 1260) | Dislikes |
|  | "You can believe whatever wacko theories you want, as long as I get paid." | Dislikes |
|  | "Just one more crazy Cabot." | Dislikes |
|  | "You're just sorry that you lost your source of immortality juice." | Dislikes |
| **The Sight** | "The Sight isn't worth killing yourself over, Mama Murphy. It doesn't have to define what you are, or what you can give." | Loves |
|  | "I told you no! You're going off this junk. Now. Or you're going to answer to me." | Likes |
|  | "No. You're an addict. You need help." | Likes |
|  | "You need to stop using chems. I'm serious." | Likes |
|  | "Here. Already have some." | Dislikes |
|  | "I'll see if I can find some." | Dislikes |
|  | "You're right. Using chems is your choice." | Dislikes |
|  | "Here. One hit of Jet." | Dislikes |
|  | "Here you go." | Dislikes |
|  | "Here. Go easy." | Dislikes |
|  | "I'll find some." | Dislikes |
|  | "Mentats. Got it." | Dislikes |
|  | "I've got it." | Dislikes |
|  | "I'll look for some." | Dislikes |
|  | "Yeah. Here you go." | Dislikes |
|  | "Med-X, huh? Okay." | Dislikes |
| **The Silver Shroud** | Outcome: Sinjin's down and Kent's been saved. I should check in on him. Kent looks pretty rattled. | Loves |
|  | "Friends don't make you weak. They make you strong." | Loves |
|  | "Leave Kent out of this. I'm the one you want." | Loves |
|  | "Good on you for trying to make the world better." | Likes |
|  | "Don't sell yourself short." | Likes |
|  | "If you just quit then the bad guys have already won." | Likes |
|  | "This whole Commonwealth is a... nightmare." | Likes |
|  | "It seems like people are finally rebuilding and recovering from the nuclear war." | Likes |
|  | "Stop selling to children, miscreant. Or face my wrath." | Likes |
|  | "Last chance. No. More. Kids." | Likes |
|  | "I am the instrument of justice and I cannot fall. Death has come for you, evildoer. And I am its Shroud." | Likes |
|  | "You touch a hair on Kent's head and you're a dead man." | Likes |
|  | "He'd... He'd. Episode 23." | Likes |
|  | "You have taken your last life, villain." | Likes |
|  | "This ends now." | Likes |
|  | "I'm thinking I'll keep the costume." | Dislikes |
|  | "You know you're completely nuts, right?" | Dislikes |
|  | "How about I just walk away?" | Dislikes |
|  | "Someone wants me to put you out of business. For the right price I could look the other way." | Dislikes |
|  | "Hand over the caps." | Dislikes |
|  | "I don't give a damn about Kent. There's a bounty on your head." | Dislikes |
|  | Quest outcome (stage 445) | Hates |
|  | Quest outcome (stage 1330) | Hates |
| **Vault 81** | "I'm just a traveler. I thought I'd take a look around." | Likes |
|  | "Let me in, damn it. You really don't want me for an enemy." | Dislikes |
| **Virgil's Cure** | Quest outcome (stage 34) | Likes |
|  | "All right." | Likes |
|  | "Go ahead. Just... try to make it quick, all right?" | Hates |
|  | Quest outcome (stage 100) | Hates |
## Real Nora: places and random encounters
| Quest | You pick / outcome | Real Nora |
| --- | --- | --- |
| **Abernathy Farm** | "There's nothing worse than losing a child. Believe me, I know." | Loves |
|  | "Farming's hard work." | Likes |
|  | "Make it five. Deal?" | Dislikes |
|  | "You call this a farm? It's pathetic." | Dislikes |
|  | "If your daughter was that stupid, she got what she deserved." | Dislikes |
| **Bunker Hill** | "Synths are weapons built by the Institute." | Likes |
|  | "It's always good to help people." | Likes |
|  | "You should look after yourself." | Dislikes |
| **Concord (around the Museum of Freedom)** | "He's a good dog. Smart, too." | Likes |
|  | "The feeling's mutual, Preston." | Likes |
|  | "Actually, I already grabbed the Fusion Core. We're set. " | Likes |
|  | "Can't be too hard. I'll see what I can do." | Likes |
|  | "Sorry. Sounds rough." | Likes |
|  | "Whatever it is, I'll stop it." | Likes |
|  | "All right, Garvey. I'm in." | Likes |
|  | "It's no big deal." | Likes |
|  | "Just trying to do what's right, ma'am." | Likes |
|  | "Actually, I already grabbed a Fusion Core. We're set. " | Likes |
|  | "Actually, I got a minigun right here. We're set." | Likes |
|  | "Dumb mutt's going to get me killed." | Dislikes |
|  | "I'm on my own side, Garvey." | Dislikes |
|  | "Stop kidding yourself. You're nothing to me." | Dislikes |
|  | "I can't. You'll have to find somebody else." | Dislikes |
|  | "The answer's no. I'm out." | Dislikes |
|  | "So we're doomed." | Dislikes |
|  | "I got my own problems." | Dislikes |
|  | "Heroism's for kids and suckers." | Dislikes |
|  | "I don't know. We'll see. " | Dislikes |
| **Diamond City** | "It was America's pasttime. A sport that united families on warm summer days. And it wasn't violent. Mostly." | Loves |
|  | "And miss basking in your delightful personality?" | Likes |
|  | "Get the Bloatfly Gland. Got it." | Likes |
|  | "I'll find him. You have my word." | Likes |
|  | "A card, a mitt, and a ball. Got it." | Likes |
|  | "Actually, I already did that." | Likes |
|  | "I'm on it." | Likes |
|  | "I try to protect people, if that's what you mean." | Likes |
|  | "Think I have something already." | Likes |
|  | "No way. I'm not hunting flies." | Dislikes |
|  | "No way am I getting mixed up in this." | Dislikes |
|  | "Hey, I'd love to help, but there's the small matter of expenses." | Dislikes |
|  | "100 caps seems light. I need more." | Dislikes |
|  | "Sweeten the deal with some money, and I might be interested." | Dislikes |
|  | "She's a synth. Definitely." | Dislikes |
|  | "I don't think so." | Dislikes |
|  | "Depends. What's this worth to you?" | Dislikes |
|  | "Blood. Bullets. And Money. All the way." | Dislikes |
|  | "I do a job, I get paid." | Dislikes |
|  | "Who-Gives-A-Crap Rays." | Dislikes |
| **Diamond City entrance (Piper at the gate)** | "Always believed in freedom of the press." | Likes |
|  | (line not found) | Likes |
|  | "I don't take orders from you." | Dislikes |
|  | "Newspapers just like to stir up trouble." | Dislikes |
|  | (line not found) | Dislikes |
| **Diamond City entrance (super mutant attack)** | "Damn. Not afraid of mutants, huh? You're our kind of gal." | Loves |
|  | "Damn. Not afraid of mutants, huh? You're our kind of guy." | Loves |
|  | "Mutants sure are hard to kill, huh? Thanks for the assist." | Loves |
| **Diamond City schoolhouse** | "A child needs all the love you can give them..." | Loves |
|  | "Is it one eighty?" | Likes |
|  | "I think they just need to know the world isn't going to collapse around them at any minute." | Likes |
|  | "If you love someone, hold on to them. Tomorrow you might not have the chance." | Likes |
|  | "Sorry. Didn't mean to interrupt." | Likes |
|  | "Everything you love will just get taken away from you in the end." | Dislikes |
|  | "It's the square root of "who gives a crap."" | Dislikes |
|  | "I go where I want." | Dislikes |
| **Drinkin' Buddy** | Quest outcome (stage 40) | Likes |
|  | Quest outcome (stage 501) | Dislikes |
| **Goodneighbor** | "I had a beautiful house, white picket fence, and a lawn with the greenest grass you'd ever seen. It was... peaceful." | Loves |
|  | "Hey, you know you could head back to Sanctuary. I'll come visit. I promise." | Loves |
|  | "I loved the song. It was perfect." | Likes |
|  | "Actually, I already took care of those Super Mutants." | Likes |
|  | "You got a deal, Daisy." | Likes |
|  | "No thanks." | Likes |
|  | "It's random murder. I'm out..." | Likes |
|  | "All that chem use definitely prepared you for a career in politics..." | Likes |
|  | "Junkie. You could've gotten yourself killed." | Likes |
|  | "Actually, I've already been to Pickman Gallery..." | Likes |
|  | "Scout out Pickman Gallery. On it." | Likes |
|  | "God, it was awful... Pickman was a serial killer. He was using dead bodies for his... art..." | Likes |
|  | "Goodneighbor seems like an okay place. Just make the most of it." | Dislikes |
|  | "Well, you kill enough people, sooner or later something's bound to make you immortal." | Dislikes |
|  | "You're not my problem. Now get out of my way." | Dislikes |
|  | "Tangle with Super Mutants? No thanks." | Dislikes |
|  | "I don't think that's enough money to cover clearing out a whole building." | Dislikes |
|  | "Actually, I already have something from there..." | Dislikes |
|  | "All right, Fred. We have a deal." | Dislikes |
|  | "Your offer's a little low, Fred." | Dislikes |
|  | "I'll get it done." | Dislikes |
|  | "I might be interested, but let's talk money, Hancock." | Dislikes |
|  | "You should have seen it. Pickman was using dead bodies as a canvas. It was raw, but... beautiful..." | Dislikes |
|  | "Three locations? That's a lot of time... A lot of bullets..." | Hates |
|  | (line not found) | Hates |
| **Goodneighbor (at the gate)** | "Sounds like anarchy." | Likes |
|  | "Unless it's "keep-dumb-assholes-away-from-me" insurance, I'm not interested." | Likes |
|  | "You better back off, or you're the one who's going to need insurance." | Dislikes |
| **Graygarden** | "This place seems familiar. I think I saw a bit about it on the news, back before the war." | Likes |
|  | "Robots can do simple tasks, sure, but you need a human being to make the big decisions." | Likes |
|  | "Well, it's definitely unique. Sort of hard to miss." | Likes |
|  | "I've got an idea. Let's make a deal." | Dislikes |
|  | "A tin can that talks like a femme fatale is still a tin can." | Dislikes |
| **Order Up** | "I'll talk to her. Maybe we can work this out." | Likes |
|  | "Scumbag. You made him an addict." | Likes |
|  | "Looks to me like they shouldn't have bought that Jet, and you shouldn't have sold it to them." | Likes |
|  | "Looks like you got some trouble. I could help." | Likes |
|  | "I want to help you, Trudy. What can I do?" | Likes |
|  | "Not going to happen, Trudy." | Likes |
|  | "Look, you owe them money. If you just pay them, then this will be over. Everyone walks away without getting hurt." | Likes |
|  | "Sounds like the family should pay what they owe you." | Dislikes |
|  | "Lock and load. Let's do this." | Dislikes |
|  | "You stop waving that gun in my face, or it's gonna involve me." | Dislikes |
|  | "If I help, I expect to get paid." | Dislikes |
|  | "All right, Trudy. I'll get rid of him." | Dislikes |
|  | "You're not dealing with Wolfgang, anymore. You're dealing with me. Now hand over that money before this gets ugly." | Hates |
|  | "Wolfgang and I had a deal. If I'm going to back out on it, I'll need more." | Hates |
|  | "Your offer seems a little low for a man's life." | Hates |
| **Runaway Synth** | "If he was with the Institute, don't you think killing him would just make them madder? Let him go. It's safer that way." | Loves |
|  | "You need to let him go. Think about it. If he meant to hurt you, wouldn't he have done it already?" | Loves |
|  | "You're not killing anyone." | Likes |
|  | "You're not killing anyone." | Dislikes |
|  | Quest outcome | Dislikes |
|  | "This is between you folks. I'm not getting involved." | Dislikes |
|  | "Rescues don't come cheap. Pay up." | Dislikes |
|  | Quest outcome | Hates |
|  | "And now it's your turn." | Hates |
|  | "You know what? You should kill him." | Hates |
|  | "If you don't let him go, I'll kill you both myself." | Hates |
|  | "You don't need to be afraid of the Institute. You let him go or I'll kill you both myself." | Hates |
| **Skylanes Flight 1665** | "Is that a secret compartment? All right, Ness. What's really going on here?" | Likes |
| **Synth versus Synth** | Quest outcome (stage 111) | Likes |
|  | "Just kill this thing and be done with it." | Likes |
|  | "Look. All I need is for you to put down the gun. Then we can talk this through." | Likes |
|  | "You know what? Just kill him." | Likes |
|  | Quest outcome (stage 112) | Dislikes |
|  | "You won't be doing anything if I take you down you first." | Dislikes |
|  | "This is none of my business." | Dislikes |
|  | Quest outcome (stage 122) | Dislikes |
|  | "You know what? Just kill him." | Dislikes |
|  | "You're not the one that's going to die here." | Dislikes |
|  | "Just kill this thing and be done with it." | Hates |
|  | Quest outcome (stage 121) | Hates |
| **The Slog** | "It's pretty clever, making a tarberry bog out of an old swimming pool." | Likes |
|  | "I think it's a great idea." | Likes |
|  | "I think you look pretty good." | Dislikes |
|  | "The first word that comes to my mind is "ugly."" | Dislikes |
|  | "Acting friendly isn't going to change the fact that you look and smell like walking corpses." | Dislikes |
| **Vault 81** | "I'm sorry. I didn't know." | Likes |
|  | "He was a junkie. He got what he deserved." | Hates |
| **Warwick Homestead** | "No wonder your crops are doing so well." | Likes |
|  | "I don't care how fertile the soil is, this place reeks." | Dislikes |

## Suggested Phase 3 work
Give synth Nora her own reactions to vanilla's reaction points (listen for the companion reaction event the way Nora Spouse does),
starting with the synth-related moments: The Nuclear Option ("He's not my son. He's a synth."), Bunker Hill ("Synths are weapons
built by the Institute."), Tradecraft ("I don't think you can enslave a machine."), Getting a Clue, Blind Betrayal, Synth Retention,
Human Error, Runaway Synth, Synth versus Synth, Road to Freedom, Kid in a Fridge.
