################################################################################
##
## Custom Pronouns #############################################################
##
################################################################################
## A customizable screen for the player to enter custom pronouns.
################################################################################
screen enter_pronouns(confirm_action=Return(), cancel_action=Return("cancel")):

    modal True
    add "#21212d" alpha 0.7 # A background

    ## These are all the input values for the pronouns. They use the special
    ## EnterInputValue class from the top of this file, so the player has to
    ## click on the input to start typing and can hit Enter to dismiss the
    ## keyboard. You can also use the Tab key to move between inputs.
    default c_they = EnterInputValue(custom_pronouns, "they")
    default c_them = EnterInputValue(custom_pronouns, "them")
    default c_their = EnterInputValue(custom_pronouns, "their")
    default c_theirs = EnterInputValue(custom_pronouns, "theirs")
    default c_themself = EnterInputValue(custom_pronouns, "themself")

    ## This special code will let the player revert to the original
    ## custom pronouns. It saves the value of custom_pronouns when this
    ## screen was first shown.
    default old_pronouns = custom_pronouns.arg_tuple

    ########################################
    ## This is very particular code that's just a convenience for the player.
    ## It means you can hit "TAB" on this screen and it will automatically
    ## activate the next input box. Due to it using an internal but undocumented
    ## engine function, it's not guaranteed to work in future versions of
    ## Ren'Py. If it does break you can just remove it (it doesn't affect the
    ## rest of the screen).
    default current_input = c_they
    default all_inputs = [c_they, c_them, c_their, c_theirs, c_themself]
    key 'K_TAB':
        action [Function(renpy.set_editable_input_value, current_input, False),
            Function(renpy.set_editable_input_value,
                all_inputs[(all_inputs.index(current_input)+1)%len(all_inputs)],
                True),
            SetScreenVariable("current_input",
                all_inputs[(all_inputs.index(current_input)+1)%len(all_inputs)])]
    ########################################


    ## You will customize this screen however you like!
    ## Some sample styling has been applied for demonstrative purposes.
    frame:
        style_prefix 'pronouns'
        has vbox
        first_spacing 80
        hbox:
            vbox:
                xsize int(config.screen_width*0.36)
                use pronoun_entry(c_they, "Subject", "they",
                    "I heard [custom_pronouns.they] went to bed.")
                use pronoun_entry(c_them, "Object", "them",
                    "I met [custom_pronouns.them] at the store.")
                use pronoun_entry(c_their, "Possessive Adjective", "their",
                    "I saw [custom_pronouns.their] car at the store.")
            vbox:
                xsize int(config.screen_width*0.36)
                use pronoun_entry(c_theirs, "Independent Possessive", "theirs",
                    "That grocery bag is [custom_pronouns.theirs].")
                use pronoun_entry(c_themself, "Reflexive", "themself",
                    "I told [custom_pronouns.them] to do it [custom_pronouns.themself].")
                vbox:
                    label _("Which sounds more natural?")
                    hbox:
                        ## Let players pick whether verb conjugations should
                        ## be plural or singular.
                        style_prefix 'pcheck'
                        textbutton _("[custom_pronouns.they!c] are kind."):
                            action SetField(custom_pronouns, "is_plural", True)
                        textbutton _("[custom_pronouns.they!c] is kind."):
                            action SetField(custom_pronouns, "is_plural", False)
        hbox:
            textbutton _("Confirm"):
                xfill False xalign 0.5
                ## This ensures this button is only clickable if the player
                ## has entered something in all the inputs.
                sensitive custom_pronouns.no_blank_input
                ## By default, this action is Return() under the assumption that
                ## you are calling this screen during scripting. If you are
                ## making it part of a menu (like the save/load screens), then
                ## this action may be different depending on your needs.
                action confirm_action
            textbutton _("Cancel"):
                xfill False xalign 0.5
                ## Reset the pronouns to the ones saved earlier.
                action [Function(custom_pronouns.reset_pronouns, old_pronouns),
                    ## By default this action is Return("cancel").
                    ## Returning "cancel" here means we can tell the
                    ## difference between a player who backed out of
                    ## this screen and one who entered new pronouns.
                    cancel_action]

## A small screen to simplify how you input pronouns.
screen pronoun_entry(input_value, title, example, sentence):
    vbox:
        hbox:
            spacing 25
            vbox:
                xmaximum 270 spacing 0
                label "[title!i]:"
                text "e.g. [example]" size 22 xalign 0.5
            button:
                ## This button is required for this sort of input to work.
                ## It needs the property key_events True so the player can
                ## type into the input without hovering over this button.
                key_events True
                ## And this is the action that will activate or deactivate
                ## the input for typing.
                action input_value.Toggle()
                ## And now the input which the button toggles.
                input value input_value:
                    ## You can put other restrictions, like pixel_width
                    ## or only allowing certain characters
                    length 16
        ## An example sentence is a good idea, because a lot of people
        ## won't know what the grammatical terms are for pronoun words.
        text "[sentence!i]"

## Some styles
style pronouns_frame:
    padding (45, 45) align (0.5, 0.5)
    background "#292835"
style pronouns_hbox:
    spacing 50 xalign 0.5
style pronouns_vbox:
    spacing 20
style pronouns_button:
    xfill True
    padding (6,6)
    align (0.0, 0.5)
    background "#f93c3e"
    hover_background "#ff8335"
    insensitive_background "#21212d"
style pronouns_button_text:
    color "#fff"
style pronouns_text:
    color "#fff"
style pronouns_label_text:
    color "#f7f7ed" bold True
    font gui.name_text_font
style pronouns_input:
    color "#f7f7ed"

################################################################################
## A customizable screen for the player to select multiple pronouns.
################################################################################
screen pick_multiple_pronouns():

    add "#21212d" alpha 0.7 # A background

    frame:
        background "#292835"
        padding (25, 20)  xsize 1450
        align (0.5, 0.5)
        has vbox
        spacing 10 align (0.0, 0.5)
        hbox:
            spacing 50
            use pick_pronouns_checkbox()
            vbox:
                style_prefix 'pcheck'
                label _("How often do you want to randomize your pronouns?")
                textbutton _("Every line"):
                    action SetVariable("pronoun_switch_freq", "line")
                textbutton _("Every new scene"):
                    action SetVariable("pronoun_switch_freq", "scene")
                textbutton _("I will manually change them"):
                    action SetVariable("pronoun_switch_freq", None)
            vbox:
                style_prefix 'pcheck'
                label ("Which terms do you prefer?")
                textbutton _("Neutral\n(e.g. spouse, sibling)"):
                    action SetVariable("terms", "neutral")
                textbutton _("Feminine\n(e.g. wife, sister)"):
                    action SetVariable("terms", "feminine")
                textbutton _("Masculine\n(e.g. husband, brother)"):
                    action SetVariable("terms", "masculine")
                textbutton _("Base it on my pronouns"):
                    action SetVariable("terms", "custom")
                textbutton _("Advanced"):
                    action Show("term_customization")
        null height 20
        hbox:
            spacing 75
            vbox:
                style_prefix 'pcheck' xsize None
                label _("Current Pronouns:")
                ## Players can click on their pronoun to change it.
                textbutton _("{}").format(pronoun if pronoun != "custom" else (custom_pronouns.they + "/" + custom_pronouns.them)):
                    xalign 0.5 left_padding 6
                    if pronoun in player_pronouns:
                        action CycleList(player_pronouns, 'pronoun')
            ####################################################################
            ## The following line can be uncommented if you would like to
            ## include multi-bar pronoun frequency sliders.
            ##
            # use pronoun_frequency_sliders()
            vbox:
                if len(player_pronouns) > 1:
                    ## Pronoun frequency sliders
                    label _("Adjust relative pronoun frequency:"):
                        style_prefix 'pcheck' align (0.5, 0.5)
                    for pron in player_pronouns:
                        hbox:
                            style_prefix 'pcheck'
                            xalign 0.5
                            ## This is a slider that lets the player set how often
                            ## they want to see this pronoun.
                            ## Again, special case for custom pronouns
                            label "{}: {:d}".format(pron if pron != "custom" else (custom_pronouns.they + "/" + custom_pronouns.them),
                                    pronoun_frequency[pron]):
                                xsize 300 text_adjust_spacing False yalign 0.5
                            bar value DictValue(pronoun_frequency, pron, 10, step=1):
                                xsize 500 yalign 0.5
                                ## Reset the pronoun frequency list so it's
                                ## regenerated when pronouns are randomized.
                                released SetVariable("pronoun_freq_list", None)
            ####################################################################

        null height 20
        textbutton _("Confirm"):
            style_prefix 'pronouns' xfill False xalign 0.5
            # They need to pick at least one pronoun
            sensitive len(player_pronouns) > 0
            action Return()

## A helper screen to reduce indentation
screen pick_pronouns_checkbox():
    vbox:
        style_prefix 'pcheck'
        label _("Choose your pronouns")
        ## Filter is used because "custom" is handled separately
        for pron in filter(lambda x: x != "custom", possible_pronouns):
            textbutton pron action TogglePronoun(pron)

        if custom_pronouns.no_blank_input:
            ## If the player has entered custom pronouns, they can
            ## add them to their set of pronouns.
            textbutton _("[custom_pronouns.they]/[custom_pronouns.them]"):
                action TogglePronoun("custom")
            ## Also add a button to update the custom pronouns.
            textbutton _("Update custom pronouns"):
                action Show("enter_pronouns", None,
                    confirm_action=Hide("enter_pronouns"),
                    cancel_action=Hide("enter_pronouns"))
        else:
            textbutton _("Enter custom pronouns"):
                action Show("enter_pronouns", None,
                    ## The confirm/cancel actions are different because
                    ## we don't want to return after the player
                    ## finishes inputting their pronouns. Also, if the
                    ## player inputted custom pronouns, it's probably safe
                    ## to assume they want to use them.
                    confirm_action=[Hide("enter_pronouns"),
                        TogglePronoun("custom")],
                    cancel_action=Hide("enter_pronouns"))

style pcheck_vbox:
    xsize 400
style pcheck_label:
    top_margin 15 bottom_margin 10
style pcheck_label_text:
    color "#f93c3e" size gui.name_text_size
    font gui.name_text_font
style pcheck_button:
    selected_foreground Transform("#ff8335", xsize=8, xalign=0.0, yalign=0.5)
    padding (27, 6, 6, 6)
style pcheck_button_text:
    idle_color "#888888"
    selected_color "#fff"
    hover_color "#ff8335"
style pcheck_bar:
    left_bar "#ff8335"
    right_bar "#c05a1b"

################################################################################
## In-game pronoun adjustment
################################################################################
## A screen that lets the player adjust their pronouns in-game.
## It does not let them add or adjust their pronouns. If you want to allow that,
## you can simply use the `pick_multiple_pronouns` screen again!
screen in_game_pronouns():

    tag menu

    modal True

    add "#21212d" alpha 0.7 # A background

    frame:
        background "#292835"
        padding (25, 20)
        align (0.5, 0.5)
        has vbox
        spacing 10 align (0.0, 0.5)
        hbox:
            spacing 50
            hbox:
                spacing 75
                vbox:
                    style_prefix 'pcheck' xsize None
                    label _("Current Pronouns:")
                    if player_pronouns:
                        for pron in player_pronouns:
                            ## Players can click on their pronoun to change it.
                            textbutton _("{}").format(pron if pron != "custom" else (custom_pronouns.they + "/" + custom_pronouns.them)):
                                ## If they're switching pronouns every line,
                                ## there's no point letting them choose new ones.
                                if pronoun_switch_freq != "line":
                                    action SetVariable("pronoun", pron)

                    else:
                        textbutton _("{}").format(pronoun if pronoun != "custom" else (custom_pronouns.they + "/" + custom_pronouns.them))
            vbox:
                style_prefix 'pcheck'
                label _("How often do you want to randomize your pronouns?")
                textbutton _("Every line"):
                    action SetVariable("pronoun_switch_freq", "line")
                textbutton _("Every new scene"):
                    action SetVariable("pronoun_switch_freq", "scene")
                textbutton _("I will manually change them"):
                    action SetVariable("pronoun_switch_freq", None)

        null height 20
        textbutton _("Close"):
            style_prefix 'pronouns' xfill False xalign 0.5
            action Return()

## A screen which can be displayed in-game so the players can adjust their
## pronouns.
screen in_game_pronouns_button():
    if pronoun:
        ## Only show this button if the player has actually
        ## set up some pronouns
        textbutton _("Pronouns"):
            style_prefix 'pronouns' xfill False align (1.0, 0.0)
            action ShowMenu("in_game_pronouns")


################################################################################
## Term Customization
################################################################################
## An screen for more granular control over which terms the player is
## comfortable with.

screen term_customization():
    modal True

    ## The current pronoun set the player is adjusting terms for.
    ## `None` means adjusting all pronouns at once (except those with more
    ## specific preferences).
    default current_key = None

    add "#21212d" alpha 0.7 # A background

    frame:
        background "#292835"
        padding (25, 20)
        align (0.5, 0.5)
        has vbox
        spacing 10

        frame:
            background "#f93c3e" xalign 0.5
            has hbox
            xalign 0.5
            style_prefix 'which_pronoun'
            textbutton _("All"):
                action SetScreenVariable("current_key", None)
            ## Let the player switch between setting terms for each of their
            ## pronoun sets.
            for pron in player_pronouns:
                textbutton "{}".format(pron if pron != "custom" else (custom_pronouns.they + "/" + custom_pronouns.them)):
                    action SetScreenVariable("current_key", pron)
        hbox:
            style_prefix 'term_reset'
            textbutton _("Reset to Defaults"):
                action Confirm("Are you sure?\nThis will overwrite any custom\nterms you applied for this pronoun.",
                    ## This is a custom action defined in pronoun_backend.rpy
                    yes=SetAllTerms(current_key, None))
            textbutton _("Set all to Neutral"):
                action Confirm("Are you sure?\nThis will overwrite any custom\nterms you applied for this pronoun.",
                    yes=SetAllTerms(current_key, "neutral"))
            textbutton _("Set all to Feminine"):
                action Confirm("Are you sure?\nThis will overwrite any custom\nterms you applied for this pronoun.",
                    yes=SetAllTerms(current_key, "feminine"))
            textbutton _("Set all to Masculine"):
                action Confirm("Are you sure?\nThis will overwrite any custom\nterms you applied for this pronoun.",
                    yes=SetAllTerms(current_key, "masculine"))

        null height 35
        viewport:
            style_prefix "pronoun_vp"
            mousewheel True draggable True
            scrollbars "vertical"
            has vbox

            ## You can make your own list of Term objects to
            ## iterate over also; this is automatically generated
            ## from the Term.ALL_TERMS class attribute.
            for term in Term.ALL_TERMS:
                hbox:
                    style_prefix 'pick_term'
                    text term.description
                    textbutton get_custom_term(term.id, current_key):
                        selected has_custom_term(current_key, term.id)
                        xsize 290
                        action [SetVariable("active_term", term),
                            CaptureFocus("term_drop")]
                    button:
                        key_events True
                        background "#fff4" selected_foreground None
                        hover_background "#fff6"
                        xsize 290 ysize 54 xpadding 10
                        action create_term_input_values[current_key][term.id].Toggle()
                        input value create_term_input_values[current_key][term.id]:
                            pixel_width 270
                        if not player_inputted_terms.setdefault(current_key,
                                dict()).get(term.id, None):
                            ## Show a message that text can be typed in here
                            foreground Text(_("Type your own term"),
                                style='term_input_value_text')
                    textbutton _("Clear"):
                        selected_foreground None padding (5, 5)
                        text_align (0.5, 0.5)
                        background "#f93c3e" hover_background "#b42123"
                        insensitive_background "#21212d"
                        text_color "#fff"
                        sensitive player_inputted_terms[current_key].get(
                            term.id, "")
                        action SetDict(player_inputted_terms[current_key],
                            term.id, "")

                ## Add a little separator
                add "#ff8335" ysize 4

        null height 20
        textbutton _("Confirm"):
            style_prefix 'pronouns' xfill False xalign 0.5
            # They need to pick at least one pronoun
            action Hide("term_customization")

    ## A Help button
    textbutton _("?"):
        text_font gui.name_text_font
        text_size 60 text_bold True align (1.0, 0.0) xysize (130, 130)
        top_margin 30 right_margin 30 text_align (0.5, 0.6)
        background "#ff8335" text_color "#f93c3e"
        hover_background "#f7f7ed"
        action Show("term_help")

    ## The term dropdown
    if GetFocusRect("term_drop"):
        ## If the player clicks outside the frame, dismiss the dropdown.
        ## The ClearFocus action dismisses this dropdown.
        add "#21212d" alpha 0.6
        dismiss action [ClearFocus("term_drop")]

        ## This positions the displayable near (usually under) the button above.
        nearrect:
            focus "term_drop"

            ## Finally, this frame contains the choices in the dropdown, with
            ## each using ClearFocus to dismiss the dropdown.
            frame:
                style_prefix 'pronoun_drop'
                has vbox
                for poss in active_term.possibilities:
                    textbutton poss:
                        action [SetCustomTerm(current_key, poss),
                            ClearFocus("term_drop")]
                add "#ff8335" ysize 4 xsize 150
                textbutton _("(Clear)"):
                    text_idle_color "#888"
                    action [SetCustomTerm(current_key, None),
                        ClearFocus("term_drop")]

style term_reset_hbox:
    spacing 25 xalign 0.5
style term_reset_button:
    xsize 230
    padding (6,6)
    align (0.0, 0.5)
    hover_background "#f93c3e"
    background "#ff8335"
    insensitive_background "#21212d"
style term_reset_button_text:
    xalign 0.5 text_align 0.5 yalign 0.5
    idle_color "#fff"
    selected_color "#fff"
    hover_color "#f7f7ed"
    size 27 size_group "tr"
style which_pronoun_button:
    is term_reset_button
    size_group None
    background "#f93c3e"
    selected_background "#b42123"
    hover_background "#ff8335"
    xsize 240
style which_pronoun_button_text:
    is term_reset_button_text
    insensitive_color "#21212d"
    size 32
style which_pronoun_hbox:
    is term_reset_hbox spacing 0
style pronoun_drop_frame:
    background Window("#21212d", background="#f93c3e",
                    padding=(5, 5), style='empty')
    padding (28, 28)
    modal True xalign 0.5
style pronoun_drop_vbox:
    spacing 18 box_wrap True box_wrap_spacing 100
    ymaximum 400
style pronoun_drop_button:
    align (0.5, 0.5)
style pronoun_drop_button_text:
    color "#f7f7ed"
    hover_color "#ff8335"
    xalign 0.5 text_align 0.5 yalign 0.5
style pick_term_hbox:
    spacing 25
style pick_term_text:
    min_width 500 xalign 1.0
    color "#fff"
style pick_term_button:
    xalign 0.0
    selected_foreground Transform("#f93c3e", xysize=(10, 10), align=(0.0, 0.5))
    left_padding 25
    ypadding 5
style pick_term_button_text:
    color "#888"
    hover_color "#fff"
    selected_color "#fff"
style pronoun_vp_viewport:
    xysize (1300, 600)
style pronoun_vp_vbox:
    spacing 10
style pronoun_vp_vscrollbar:
    thumb "#ff8335"
    base_bar "#c05a1b"

################################################################################
## Term Help
################################################################################
## A help screen to explain what to do on the term customization screen.
## This code could be adapted to make tutorials on the other screens,
## if desired. It is not necessary to include this screen, but if you do,
## be sure to read over the text and make sure it makes sense for your game.
screen term_help():
    modal True

    default page = 1
    default num_pages = 9

    if page in (1, 2, 9):
        ## Dim the whole screen
        add "#21212d" alpha 0.8
    elif page in (3, 4):
        ## Dim the screen, but leave the tabs at the top undimmed
        add "#21212d" alpha 0.8 ysize 925 yalign 1.0
    elif page in (5, 6):
        ## Dim the screen, but leave the buttons at the top undimmed
        add "#21212d" alpha 0.8 ysize 800 yalign 1.0
    elif page in (7,8):
        ## Dim the screen, but leave the first pronoun line undimmed
        add "#21212d" alpha 0.8 ysize 300 yalign 0.0
        add "#21212d" alpha 0.8 ysize 700 yalign 1.0

    frame:
        style_prefix 'term_help'
        has vbox
        if page == 1:
            label _("Term Customization")
            text _("This screen gives you greater control over which terms you are comfortable with. There are several features to play with, so we'll go over them one by one.")
        elif page == 2:
            label _("Term Preferences")
            text _("By default, the game will use your preferences for terms as set on the previous screen (where you were asked if you prefer neutral, feminine, or masculine terms, or if you wanted to let them match your current pronouns).")
            text _("This screen gives you more control over which exact terms you would like the game to use for you. You can set a different term for each pronoun, or you can set a general term for all pronouns at once.")
        elif page == 3:
            label _("Pronoun Tabs")
            text _("These tabs at the top correspond to the pronouns you've picked out.")
            text _("The special \"All\" tab lets you set your general preferences for all pronouns at once, {b}unless{/b} you have a more specific preference in one of the pronoun tabs.")
            text _("For example, say you are using both he/him and they/them pronouns. If you set your honorific in \"All\" to \"Mx.\", then you will be referred to with \"Mx.\" both when you're using he/him and when you're using they/them.")
            text _("If you then set your honorific in the he/him tab to \"Mr.\", then you will be referred to with \"Mr.\" when you're using he/him, but \"Mx.\" when you're using they/them.")
        elif page == 4:
            label _("Pronoun Tabs")
            text _("If you added more pronouns, then they would also use the honorific you set in \"All\" until you set a more specific one in that pronoun's tab.")
            text _("In short, setting a specific term in \"All\" will override your general neutral/feminine/masculine preferences from the previous screen, and setting a specific term in a pronoun tab will override the term from \"All\".")
            text _("You can tell if you have a specific term set by the colour of the text. If it is white and has a red square beside it, then it has been customized. Otherwise, it's using the default based on your term preferences on the other screen.")
        elif page == 5:
            label _("\"Set All\" Options")
            text _("Next, there are four orange buttons that let you set all terms at once. These {b}only{/b} affect the terms in the current pronoun tab - for example, if you click one of these options on the \"All\" tab, any pronoun tabs {b}will NOT{/b} be affected, just the \"All\" tab.")
            text _("The first button will reset all terms to the default based on your term preferences on the other screen. So, if you picked that you generally prefer \"feminine\" terms, then the terms will be set to things like sister, daughter, wife, etc.")
            text _("This is most useful if your preference is to use your pronouns to determine your terms, but you want to tweak a few of them individually.")
        elif page == 6:
            label _("\"Set All\" Options")
            text _("The second button, \"Set all to Neutral\" will set all terms to neutral terms, like sibling, child, spouse, etc.")
            text _("And the same pattern follows for the Feminine and Masculine buttons.")
            text _("You can use these buttons to quickly set up a bunch of term preferences at once, and then tweak a few of them individually afterwards.")
        elif page == 7:
            label _("Selecting a Term")
            text _("To customize a term for a particular group, just click on the term you want to change. This will bring up a dropdown box of the different options for that term. \"(Clear)\" will reset the term to the default.")
            text _("Note that some terms will have more options than others. For example, the \"Honorific\" term has more than just one neutral, feminine, and masculine option. In some cases, using this screen will be the only way to see those terms, since regular term preferences will just give you the default neutral/feminine/masculine options.")
        elif page == 8:
            label _("Entering Your Own Terms")
            text _("You can also type your own term into the box on the right. This will override any of the other options for that term.")
            text _("Using the \"Set All\" buttons will {b}also{/b} clear any terms you've entered manually, so be careful if you've entered your own terms and then use one of those buttons.")
            text _("The \"Clear\" button to the right of the input box will reset the term to the default.")
        elif page == 9:
            label _("Final Notes")
            text _("You should be sure to also set your general term preferences on the previous screen as you like it, since if the game is updated with new term groups, they will use your preferences to determine which sort of terms to use.")
            text _("Hopefully this helps you customize your game experience better!")
            text _("Click \"Close\" to return to the term customization screen.")


        hbox:
            spacing 150 xalign 0.5
            textbutton _("Previous"):
                style_prefix 'pronouns' xfill False xalign 0.5
                sensitive page > 1
                action SetScreenVariable("page", max(page-1, 1))
            textbutton _("Close"):
                style_prefix 'pronouns' xfill False xalign 0.5
                action Hide("term_help")
            textbutton _("Next"):
                style_prefix 'pronouns' xfill False xalign 0.5
                sensitive page < num_pages
                action SetScreenVariable("page", min(page+1, num_pages))

style term_help_frame:
    background "#292835"
    padding (25, 20)
    align (0.5, 1.0) yoffset -120
    xsize 1200
style term_help_vbox:
    spacing 25 xalign 0.5
    first_spacing 35
style term_help_label:
    xalign 0.5 xsize None xminimum None xmaximum None
style term_help_label_text:
    font gui.name_text_font size 50
    color "#f93c3e" text_align 0.5
style term_help_text:
    color '#fff'
    layout "subtitle"
    xalign 0.5 text_align 0.5
style term_input_value_text:
    size 25 color "#aaa"
    align (0.5, 0.5)