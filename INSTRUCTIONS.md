# README

Thank you for downloading In-Depth Pronouns for Ren'Py! I hope this code will help you add more customization to your game.

There are a lot of bits and bobs that make up this code, so here is an overview of your next steps:

1. Make sure all the pronouns rpy files are inside your game/ folder somewhere. You can keep them in the pronouns/ subfolder, like YourGame/game/pronouns/pronoun_setup.rpy
2. If you're using a version of Ren'Py before 7.5 (e.g. 7.4.11 or earlier), you will need to remove or comment out some code in `pronoun_screens.rpy`. At the bottom of `screen term_customization` is a line that looks like `if GetFocusRect("term_drop"):`. You will need to remove/comment that code until the end of the screen. Slightly earlier in that same screen is the screen action `CaptureFocus("term_drop")`. You will also need to replace that with the action `CycleCustomTerm(current_key, term)`. This will allow you to click to cycle through pronouns instead of using a dropdown.
3. Otherwise, you're ready to go! Add the line `jump test_select_pronouns` somewhere early on in your script so you can test out the features.

The `test_one_pronoun_set` label demonstrates the simplest version of this code, where the player picks between pre-set pronouns without any further customization options.

The `test_custom_pronouns` brings up a screen where players can input their own pronouns. Players can then separately select which sorts of terms they want to use.

The `multiple_pronouns` label has two versions. The first is set up using a series of choice menus, most suited for if you're unfamiliar with screen language but still want to give players more involved customization. This label allows players to choose multiple pronoun sets, including the option to enter their own. They can then choose which terms they want to use, and how frequently they would like the game to randomize their pronouns.

Absent from the choice menu options is:

- The ability to customize pronoun randomization percentages. By default, all pronouns are weighted equally likely to be chosen when the game randomizes pronouns.
- The ability to fine-tune term preferences. This choice menu only allows players to set a general preference which will be used for all terms, with no options to fine-tune words for particular term groups.

These are both adjustable in the `pick_multiple_pronouns` screen, but are omitted from the choice menu approach due to it being very cumbersome to implement as a series of choices. However, the choice menu approach is an extremely suitable option if you want to allow players more control over their terms and also have multiple pronouns, while keeping the required coding very minimal.

Finally, there is the screen version of the `multiple_pronouns` label. It calls a special screen, `pick_multiple_pronouns`. This screen unleashes the full potential of the pronouns systems - not only can players mix and match pronoun sets, enter their own, adjust the frequency each pronoun set will be used, but they can also use the *Advanced* option for terms to fine-tune the words people use to refer to them.

## Adding Pronouns to your Project

If the options presented in the label demos above suit your project's needs, you can simply pop that code wherever your game needs it, and optionally update any of the screens in `pronoun_screens.rpy` to suit the styling of your game.

To add to or adjust existing pronoun values, head over to `pronoun_setup.rpy`. This file has the code where you can declare different pronoun sets, verbs, and any terms you might need for your game. There are plenty of examples to demonstrate how to add and adjust them to your needs.

You can also adjust any of the screens in `pronoun_screens.rpy` for your project. Where possible, custom actions have been added to simplify a lot of the buttons and inputs. You need to keep a lot of the logical stuff the same (button actions, input values), but the styling and positioning is up to you!

## Final Notes

Thanks for reading through this README! If you use this code in your project, you can credit me as Feniks with a link to my website https://feniksdev.com/ - I also post Ren'Py tutorials on there! You can follow me on itch.io at https://feniksdev.itch.io/ to be notified of any future tool releases as well. In particular, I am releasing a multi-thumb slider soon which will complement the pronoun code and can be used as a frequency slider.

If you found this code useful, consider dropping me a ko-fi at https://ko-fi.com/fen/ I appreciate the support to help me keep releasing useful Ren'Py tools!
