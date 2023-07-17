################################################################################
##
## In-Depth Pronouns for Ren'Py
##
################################################################################
## A collection of classes, variables, functions and more to help you
## incorporate player-selected pronouns into your game.
##
## This code is designed for the English pronoun system, but can be adapted
## for other languages as well.
##
## It is designed to be as easy as possible to script for, while also
## boasting fairly minimal setup on the user's end.
##
## Notably, it also includes support for the player to have multiple pronouns,
## including the ability to set up frequencies for how often each pronoun
## should be used, and custom pronouns.
##
## Sample dialogue:
## "Don't say that to [them], [they_re] doing [their] best."
## "[they!c] told me [themself]."
## "Do you know what [they] usually [do]?"
##
## Depending on pronouns, this sort of line might display as:
## "Don't say that to him, he's doing his best."
## "Don't say that to them, they're doing their best."
## "Don't say that to her, she's doing her best."
##
## The steps to set up the code are included alongside it with examples
## and comments. If you haven't already, I also recommend you read the
## README first!
##
## If you use this code in your project,
## please credit me as Feniks @ feniksdev.com
## Also consider tossing me a ko-fi @ https://ko-fi.com/fen
################################################################################

################################################################################
## Variables and Constants
################################################################################
##
## General Setup ###############################################################
##
## A list of strings corresponding to the possible pronouns the player can
## choose from. These string names are arbitrary to some extent, but the
## strings they/them, she/her, and he/him specifically are used in the Term
## class to pick out the correct term to use based only on pronouns.
## These are the strings you will set the `pronoun` variable to to change the
## player's pronouns, e.g. $ pronoun = "she/her"
## This is also the order which pronoun words will be selected from for any
## Pronoun declarations (see below).
define possible_pronouns = [
    "they/them", "she/her", "he/him",
    ## Add more as you like.
    ## Also add any new strings to plural_pronouns (below) if they are plural.
    # "ey/em", "xe/xem", "ze/hir"

    ## The "custom" string is treated specially. If present, players
    ## will have the option to enter and use a custom set of pronouns.
    ## It should always be at the end of the list, so it doesn't conflict
    ## with indexing regular pronouns.
    "custom",
]

## The player's pronouns. This sets it up to the empty string, but you can
## also set it explicitly like
# default pronoun = "they/them"
default pronoun = ""

## One of "neutral", "feminine", "masculine", "custom". "custom" will base
## the terms off of the player's current pronouns. For most purposes,
## keeping terms as "custom" is fine unless you'd like to give the player
## additional control.
default terms = "custom"

## The player's custom pronouns. Only used if pronoun is "custom".
## This is set up as blank to start.
default custom_pronouns = CustomPronoun("", "", "", "", "", False)
## Other example CustomPronouns:
## CustomPronouns("ey", "em", "eir", "eirs", "eirself", is_plural=False)
## CustomPronouns("xe", "xem", "xyr", "xyrs", "xemself", is_plural=False)
## CustomPronouns("ze", "hir", "hir", "hirs", "hirself", is_plural=False)
## Generally, you will let players fill out a CustomPronouns class


## Pronouns which are considered plural for verb conjugations (e.g. "they are"
## instead of "she is"). You only need to add more strings to this if you're
## setting them up as default options; custom pronouns have an is_plural
## property included for you to specify. For most purposes, this can be
## left as-is.
define plural_pronouns = set(["they/them"])

################################################################################
##
## Script Pronoun Setup ########################################################
##
## The basic pronouns. These go in the order you declared possible_pronouns in,
## so in this case it's they/she/he. The special `custom` field is used to
## select an appropriate field from the CustomPronouns class - the fields are
## named after they/them/their etc. pronouns, so it will typically use these
## same values even if you add or remove pronoun sets.
define they = Pronoun("they", "she", "he", custom="they")
define them = Pronoun("them", "her", "him", custom="them")
define their = Pronoun("their", "her", "his", custom="their")
define theirs = Pronoun("theirs", "hers", "his", custom="theirs")
define themself = Pronoun("themself", "herself", "himself", custom="themself")
define they_re = Pronoun("they're", "she's", "he's", custom="they_re")
define they_ve = Pronoun("they've", "she's", "he's", custom="they_ve")

## Tip: If you only had two sets of possible pronouns (e.g. she/her and he/him)
## and no option for custom pronouns, then your declarations would follow this
## pattern:
# define possible_pronouns = ["she/her", "he/him"]
# define they = Pronoun("she", "he")
# define them = Pronoun("her", "him")
## etc.
## You should still use they/them/their as the variable names because
## 1) hers=them+their and 2) his=their+theirs ergo there is a naming
## conflict if you tried to use one or the other.
##
## Note, however, that there's no harm in keeping the existing pronoun setup
## and only allowing players to choose a subset of them.
##
## If you're including another pronoun set besides the ones here, it will get
## listed in the order it appears in possible_pronouns, so if you added
## "ey/em" to possible_pronouns like so:
# define possible_pronouns = [ "they/them", "she/her", "he/him", "ey/em" ]
## Then you would declare the various Pronoun objects like
# define they = Pronoun("they", "she", "he", "ey")
# define them = Pronoun("them", "her", "him", "em")
## In this case the custom field is optional depending on whether you're
## including custom pronouns or not.

################################################################################
##
## Script Verb Setup ###########################################################
##
## Special verb conjugations. The special `s` and `es` are for verbs that
## are regular, e.g. "[they] walk[s]" becomes "she walks" or "they walk"
## depending on the pronoun, but you don't need to declare a `walk` variable.
## These go in the order plural - singular, so the first word should make sense
## after the phrase "two people" as in "two people *are*" and the second should
## make sense after the phrase "one person" as in "one person *is*".
## They are named after the plural form of the verb aside from s/es, since
## you will be writing pronouns as [they] [are] rather than [they] [is].
define are = PronounVerb("are", "is")
define were = PronounVerb("were", "was")
define have = PronounVerb("have", "has")
define havent = PronounVerb("haven't", "hasn't")
define arent = PronounVerb("aren't", "isn't")
define do = PronounVerb("do", "does")
define dont = PronounVerb("don't", "doesn't")
define s = PronounVerb("", "s")
define es = PronounVerb("", "es")

################################################################################
##
## Script Term Setup ###########################################################
##
## Terms and other words you might want. You'll generally add to this
## as they come up during scripting. They come in the order
## neutral, feminine, masculine
## Neutral is also used for custom pronouns by default.
## The ID is used to identify this term for the Advanced term customization.
## Typically, it's sufficient to just make this id the same as the name of
## the Term object itself, as is done below.
define person = Term("person", "woman", "man", id="person")
## You may also want to provide a description for a particular term category.
## In this case, all the terms fall under the category "honorific". By adding
## a description, you can customize how the terms are displayed in the
## advanced term customization screen.
define Mx = Term("Mx.", "Ms.", "Mr.", id="honorific", description="Honorific",
    ## There's also a special "other" argument. Here, you can provide optional
    ## terms that will be displayed in the advanced term customization screen.
    ## In this case, Mx/Ms/Mr are the default options for
    ## neutral/feminine/masculine terms respectively, but a player can use the
    ## advanced terms customization to select a more specific term from this
    ## list if they so desire.
    other=["Mrs.", "Miss", "Mys.", "Dr.", "Sir", "Madam"])
define sibling = Term("sibling", "sister", "brother", id="sibling")
define child = Term("child", "daughter", "son", id="child")
define kid = Term("kid", "girl", "boy", id="kid")
define spouse = Term("spouse", "wife", "husband", id="spouse")
define partner = Term("partner", "girlfriend", "boyfriend", id="partner",
    other=["datefriend", "datemate", "sweetheart"])
## This one is a slightly special case because the neutral form is the same
## as the masculine form, so you can omit the masculine form.
define actor = Term("actor", "actress", id="actor")
## If more than one term has the same neutral form, you may want to add a
## number or other information to differentiate it. Both the name of the
## Term object and the id must be unique, but the actual words don't have to be.
define person2 = Term("person", "lady", "guy", id="person2")


################################################################################
## Variables for Multiple Pronouns
################################################################################
## These are variables relating to multiple pronouns. Unless you know what
## you're doing, most of these do not need to be changed (as they are
## typically adjusted by the player via screens or in-script).

## A list of the pronoun sets the player is using. You will generally not
## change this, unless you would like the player to start with a particular
## set of pronouns e.g. default player_pronouns = ["she/her", "they/them"]
default player_pronouns = list()

## A convenience variable to use in dialogue or UI (see the label for how
## it's used). Its initial value here is inconsequential.
default pretty_pronouns = ""
