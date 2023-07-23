# In-Depth Pronouns for Ren'Py

Overview
--------

This tool for Ren'Py provides a comprehensive way of adding player-selectable pronouns to your game, including rarely-seen features such as:

*   Choose multiple pronoun sets, and determine how frequently you would like each set to be used
*   Customize how frequently pronouns are switched, with the option to randomize pronouns every line, every scene, or only manually
*   Enter your own set of custom pronouns, which can be used alongside any other pronoun sets
*   Select term preferences separately from pronouns – players can use they/them but still be called “sister”, “daughter”, “girlfriend”, or use he/him but be referred to as “sibling”, “child”, “partner”.
*   Enter your own terms to be referred to by, and fine-tune specific preferences. Maybe you use she/they but prefer "person" to "woman" and "sister" to "sibling" - that's possible.
*   Incredibly simple set up for not only pronouns but also verbs and gendered terms, with easily readable scripting. You can include or exclude as much functionality as you need.

Description
-----------

This code will add several new classes, functions, and screens to your game, all included inside several files inside a pronouns folder. The code is initially set up to support the pronouns they/them, she/her, he/him, and one player-inputted custom pronoun set, but can be modified to the needs of your project. The project supports players having just one pronoun set, and also supports players choosing multiple pronoun sets which the game will switch between based on player preference. It also has a comprehensive customization system for choosing preferences for terms like "sister", "brother", "sibling".

Instructions
------------

Download the repository and unzip it to get four rpy files. Place theses files into your Ren’Py game folder - I suggest you make a subfolder to store them in, e.g. `YOURGAME/game/pronouns/`. You should begin with a jump to the test label, `test_select_pronouns`, in your script so you can test it e.g. `jump test_select_pronouns` in the `start` label will let you test this code. The code is extensively documented so you can follow along and adapt it to suit the needs of your project.  

Read the INSTRUCTIONS.md included first for a quick overview of what's in each file and what to look at.  

Use
---

Roughly, set up includes lines like the following:

```renpy
define they = Pronoun("they", "she", "he", custom="they")
define them = Pronoun("them", "her", "him", custom="them")
define are = PronounVerb("are", "is")
define were = PronounVerb("were", "was")
define person = Term("person", "woman", "man", id="person")
define sibling = Term("sibling", "sister", "brother", id="sibling")
```

This will allow you to write lines in script like:

`"[they!c] [are] my [sibling]."`

This will appear in-game with the player-chosen pronouns and terms. The most common ways this will read are “She is my sister.”, “He is my brother.”, “They are my sibling.”.  

Compatibility
-------------

This code has been tested for compatibility with Ren’Py 7.5-7.6 and Ren’Py 8.0-8.1. One of the screens, `screen term_customization`, uses the `nearrect` displayable and `GetFocus` actions to create a dropdown, which was introduced in 7.5/8.0. If you are on an older version, you will need to update, remove, or refactor this screen to not use dropdowns in this manner. A description of which code to remove and replace for backwards compatibility with 7.4.11 and earlier is included in the README inside the zip file.  

The screens have also been coded with 1920x1080 project dimensions in mind. You will likely need to adapt the screens and styles to use in projects with different dimensions, though the code and logic is portable for any project dimensions.  

Otherwise, this code is expected to be compatible with any Ren’Py version past 7.4 (please leave a reply in the forums below if you encounter issues). It is also expected to remain compatible with future versions of Ren’Py, and I intend to support it into the future as well.

Terms of Use
------------

**You may:**

*   Use this code in commercial and noncommercial projects.
*   Modify and edit this code to suit your needs

**You may not:**

*   Resell all or part of this code as-is or sell it with modifications

Attribution should be credited as Feniks, with either a link to this page or to [https://feniksdev.com](https://feniksdev.com/)

Author’s Notes
--------------

This code is adapted from the code I wrote for [Our Life: Now & Forever](https://gbpatch.itch.io/our-life-nf) by GB Patch Games. Try the free demo to see how we handled character customization! 

I also have a listing for "multi-thumb bar" code (only available on itch.io, for a small fee), with code included so you can adapt it to be used for determining pronoun frequency for randomization. You can find it here: https://feniksdev.itch.io/multi-thumb-bar-for-renpy

![](https://img.itch.zone/aW1nLzEyODIzODk3LmdpZg==/original/c955SL.gif)  

For more Ren'Py tutorials, check out my website [https://feniksdev.com](https://feniksdev.com)!

## Like my work?

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/fen)
