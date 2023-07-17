################################################################################
## Demo Test Script
################################################################################
## Jump to this label to test out the various pronoun features.
label test_select_pronouns():
    ##############################
    ## This is code to reset pronouns to their defaults; for a regular game
    ## setup, you won't need this.
    $ reset_pronoun_variables(reset_custom=False)
    ##############################

    ## This screen displays an in-game button so players can adjust their
    ## pronouns after they've set them up. You can look at this screen in
    ## pronoun_screens.rpy. You may consider adding an additional button
    ## to your quick_menu or navigation screens so it's easy to access.
    show screen in_game_pronouns_button

    menu:
        "Which demo would you like to see?"
        "One pronoun set only":
            jump test_one_pronoun_set
        "One pronoun set with custom pronouns and terms":
            jump test_custom_pronouns
        "Multiple pronoun sets":
            jump multiple_pronouns
    return

################################################################################
##
## Single Pronouns #############################################################
##
## This is the most basic form of custom pronouns. The player will select their
## pronouns from a choice menu, and all the Term/Pronoun/PronounVerb objects
## will automatically match their selection so you can start scripting right
## away.
label test_one_pronoun_set():
    "This is a simple example to let players choose their pronouns."
    menu:
        "What are your pronouns?"
        "They/them":
            ## This is how you will set the player's pronouns. This string
            ## should match the ones you wrote in possible_pronouns.
            $ pronoun = "they/them"
        "She/her":
            $ pronoun = "she/her"
        "He/him":
            $ pronoun = "he/him"

    "Here is some sample dialogue:"
    call sample_pronoun_sentences()
    "That's all for this demo."
    jump test_select_pronouns


label sample_pronoun_sentences():
    ## You can use interpolation flags to assist in getting the right
    ## capitalization for pronouns and terms. See:
    ## https://www.renpy.org/doc/html/text.html#interpolating-data
    ## In this case, !c means the word will be capitalized ([they!c] -> They)
    "The [person] over there is my [sibling]. [they_re!c] wearing a red shirt."
    ## Note that you can add "n't" and such to the end of variables without
    ## having to make a whole new Term or PronounVerb for it.
    "Do you think [they] will come to the party? [they!c] [do]n't like parties."
    ## Don't forget to add [s] or [es] onto the end of verbs to make them
    ## conjugate correctly.
    "I'm pretty sure [they] like[s] parties, though. [they!c] told me so [themself], and I've seen [them] at a few."
    "It's [their] choice to come or not."
    ## Some special verbs like [have] need to be declared as a PronounVerb
    ## so they conjugate correctly (e.g. they have vs he has).
    "[they!c] [do]n't have a car, so [they] [have] to take the subway."
    ## There are some circumstances where you might reuse the same term for
    ## multiple situations; [person] can be both person/woman/man or
    ## person/lady/guy in this case, so a special person2 Term is made.
    "Can you take this to that [person2] over there? [they!c] need[s] it by tonight."
    "That [person]'s name is [Mx] Brown. [they!c] work[s] in research."
    return


################################################################################
## A test label for custom pronouns.
################################################################################
label test_custom_pronouns():
    "Now, we'll show a more complicated setup for the player to choose their pronouns and terms separately."
    ## This is the screen declared above
    $ quick_menu = False
    call screen enter_pronouns()
    $ quick_menu = True
    if _return == "cancel":
        "You didn't enter any custom pronouns."
        jump test_select_pronouns
    $ pronoun = "custom" ## This sets the pronoun to the custom input pronouns
    "Your pronouns are [they]/[them]."
    menu:
        "Which sort of terms do you prefer for yourself?"
        "Neutral e.g. person, child, sibling, kid, spouse, partner":
            ## This is how you can let players set their preferred terms.
            $ terms = "neutral"
        "Feminine e.g. woman, daughter, sister, girl, wife, girlfriend":
            $ terms = "feminine"
        "Masculine e.g. man, son, brother, boy, husband, boyfriend":
            $ terms = "masculine"
    "Understood! Here are some example sentences with custom pronouns and your term preferences."
    call sample_pronoun_sentences()
    jump test_select_pronouns


################################################################################
## Example label for multiple pronouns.
################################################################################
label multiple_pronouns():
    "This label will demonstrate how you can let players choose multiple pronouns for their playthrough."
    menu:
        "First, would you like to see this presented as a screen or as a series of choice menus?"
        "Choice menus":
            pass
        "Screen":
            $ quick_menu = False
            call screen pick_multiple_pronouns()
            $ quick_menu = True
            jump multiple_pronouns_demo

    menu pick_multiple_pronouns:
        "Please choose all pronouns you would like to use"
        "She/her" if "she/her" not in player_pronouns:
            ## This is how you add a pronoun to the player's set of pronouns.
            $ player_pronouns.append("she/her")
            ## Don't forget to set their current pronouns. Here we set it
            ## to this choice, so that we can be sure by the end that the
            ## player has an appropriate pronoun set.
            $ pronoun = "she/her"
            jump pick_multiple_pronouns # Loop
        "He/him" if "he/him" not in player_pronouns:
            $ player_pronouns.append("he/him")
            $ pronoun = "he/him"
            jump pick_multiple_pronouns
        "They/them" if "they/them" not in player_pronouns:
            $ player_pronouns.append("they/them")
            $ pronoun = "they/them"
            jump pick_multiple_pronouns
        "Custom" if "custom" not in player_pronouns:
            ## The screen from earlier to enter custom pronouns.
            ## If you're having trouble with this, you can also consider
            ## using renpy.input to get the pronouns from the player.
            $ quick_menu = False
            call screen enter_pronouns()
            $ quick_menu = True
            ## This lets us know if the player cancelled out of the screen.
            ## In this case, we will assume this means they don't want to
            ## use custom pronouns after all
            if _return == "cancel":
                jump pick_multiple_pronouns
            $ player_pronouns.append("custom")
            $ pronoun = "custom"
            jump pick_multiple_pronouns

        ## This has a check to make sure the player picked at least
        ## one set of pronouns.
        "That's all" if player_pronouns:
            pass

    ## You will need to run pretty_print_pronouns() after the player has set
    ## up their pronouns so it has up-to-date information.
    $ pretty_pronouns = pretty_print_pronouns()
    "Your pronouns are [pretty_pronouns]."
    menu:
        "Is that correct?"
        "Yes, those are my pronouns.":
            pass
        "No, I want to change them.":
            ## This resets the various pronoun variables, so the
            ## player can choose new ones.
            $ reset_pronoun_variables()
            jump pick_multiple_pronouns

    menu:
        "Which sort of terms do you prefer for yourself?"
        ## Note that you can only set terms to one of
        ## "neutral", "feminine", "masculine", or "custom".
        ## (At least, that's what's built into the Terms class; if you
        ## want to modify it, you can do so in the Terms class).
        "Neutral e.g. person, child, sibling, kid, spouse, partner":
            $ terms = "neutral"
        "Feminine e.g. woman, daughter, sister, girl, wife, girlfriend":
            $ terms = "feminine"
        "Masculine e.g. man, son, brother, boy, husband, boyfriend":
            $ terms = "masculine"
        "Base it off of my current pronouns.":
            $ terms = "custom"

    ## This menu only shows up if there are multiple pronouns the game
    ## can switch between.
    if len(player_pronouns) > 1:
        menu:
            "How often do you want to randomize which pronouns are used for you?"
            ## Similarly, you can only set this to one of
            ## "line", "scene", or None.
            ## "scene" in particular you will need to manage calls to
            ## randomize_pronouns() yourself wherever it makes sense for your
            ## script (see the multiple_pronouns_demo label for an example).
            "Every line":
                $ pronoun_switch_freq = "line"
            "Every new scene":
                $ pronoun_switch_freq = "scene"
            "I want to manually switch pronouns":
                $ pronoun_switch_freq = None

    "Summary:\nYour pronouns are [pretty_pronouns].\nYou prefer [terms] terms."
    if pronoun_switch_freq:
        "You want to randomize your pronouns every [pronoun_switch_freq]."
    else:
        "You want to manually switch your pronouns."
    menu:
        "Is that correct?"
        "Yes, that's correct.":
            pass
        "No, I want to change something.":
            ## Again, clear their pronouns so the player can re-enter them
            $ reset_pronoun_variables()
            jump pick_multiple_pronouns
    jump multiple_pronouns_demo

label multiple_pronouns_demo():
    ## This function will randomize the player's pronouns, but only if they
    ## have not chosen to manually change their pronouns.
    ## A callback handles randomizing the pronouns each line for you, so this
    ## function is most useful if the player has chosen to randomize their
    ## pronouns per-scene. You should put this call at the start of a new day
    ## or a new chapter, scene, etc, wherever it makes sense for your script.
    $ randomize_pronouns()

    "Your current pronouns are [they]/[them]."
    "If you have randomization enabled per line, you might notice your pronouns change over the course of these next demo lines."
    "If instead you have randomization enabled per scene, your pronouns are randomized at the start of the set of example sentences."
    call sample_pronoun_sentences()
    menu pronoun_end_choice:
        "Would you like to see the sample pronoun lines again?"
        "Yes":
            ## For demonstration purposes, we randomize
            ## their pronouns again here so you can test
            ## the per-scene randomization.
            $ randomize_pronouns()
            call sample_pronoun_sentences()
            jump pronoun_end_choice
        "No":
            pass
    jump test_select_pronouns
