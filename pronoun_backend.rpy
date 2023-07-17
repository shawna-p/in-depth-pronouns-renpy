################################################################################
## Python Classes and Functions
################################################################################
## This file contains Python classes and functions used to make the pronouns
## system work. None of the code in this file needs to be modified in order
## to get pronouns to work, so if you just want working pronouns in your game,
## you do not need to read through this file or understand it.
## That said, I do try to comment and explain my coding choices, so feel free
## to take a look as a learning tool.
##
## If this is the first file you're looking at, read the README to start! And
## then you can go to pronoun_setup.rpy for the intro blurb and actual
## changeable code.
##
################################################################################
## Mobile Input ################################################################
##
## This is a custom InputValue which does not begin as selected/ready for
## input and requires an action to be enabled. Pressing the Enter button
## will disable the input again.
##
## This makes it a good choice for most custom input screens, particularly
## on mobile devices where the keyboard can take up most of the screen space.
##
## Read more about InputValue here:
## https://www.renpy.org/doc/html/screen_python.html#inputvalue
##
## You can find this code on my EasyRenPyGUI template:
## https://github.com/shawna-p/EasyRenPyGui
init -10 python:

    class EnterInputValue(FieldInputValue):
        """
        Subclass of InputValue which allows the Enter key to dismiss
        the input button. Does not begin as selected (so, on mobile the
        keyboard won't immediately appear).
        """

        def __init__(self, object, field=None, default=False):
            if field is None:
                field = object
                object = renpy.store
            self.object = object
            self.field = field

            self.default = default

        def enter(self):
            """Disable this input when the user presses Enter."""
            renpy.run(self.Disable())
            raise renpy.IgnoreEvent()

## Pronoun Classes #############################################################
##
## These classes are used to store information relating to pronouns. You will
## not need to change them, unless you're adding support for a new language.
## Unless you know what you're doing, you can skip looking at this whole
## init python block.
init -10 python:

    class CustomPronoun():
        """
        A class to store custom pronouns entered by the player. Because this
        is specific to English pronoun systems, you may want to copy this class
        and modify it to support different pronoun sets for other languages.

        Attributes:
        -----------
        they : string
        them : string
        their : string
        theirs : string
        themself : string
        they_re : string
        they_ve : string
        is_plural : bool
            True if this pronoun uses plural verb conjugations.
        """

        def __init__(self, they, them, their, theirs, themself, is_plural=True):
            """
            Create a Pronouns object (set of pronouns).

            Parameters:
            -----------
            they : string
            them : string
            their : string
            theirs : string
            themself : string
            is_plural : bool
                True if this pronoun uses plural verb conjugations.
            """
            self.they = they
            self.them = them
            self.their = their
            self.theirs = theirs
            self.themself = themself
            self.is_plural = is_plural

        @property
        def themselves(self):
            """A convenience property for an alternative reflexive pronoun."""
            return self.themself

        @property
        def they_re(self):
            """A conjugated version of the pronoun + the verb 'to be'."""
            return self.they + ("'re" if self.is_plural else "'s")
        @property
        def they_ve(self):
            """A conjugated version of the pronoun + the verb 'to have'."""
            return self.they + ("'ve" if self.is_plural else "'s")

        @property
        def arg_tuple(self):
            """A convenience method to save and restore a pronoun set."""
            return (self.they, self.them, self.their, self.theirs, self.themself, self.is_plural)

        @property
        def no_blank_input(self):
            """Return True if there are no blank fields in this object."""
            return all([getattr(self, field).strip() for field in ["they",
                "them", "their", "theirs", "themself"]])

        def reset_pronouns(self, args):
            """
            Reset the pronouns to the default values.

            Parameters:
            -----------
            args : tuple
                A tuple of arguments to pass to the constructor. Typically the
                return value of the arg_tuple property.
            """
            self.__init__(*args)

        def __eq__(self, other):
            """Check if two pronoun sets are equal."""
            if not isinstance(other, CustomPronoun):
                return False
            return (self.arg_tuple == other.arg_tuple)

        def __ne__(self, other):
            """Compat for Python 2."""
            return not self.__eq__(other)


    class Pronoun():
        """
        A helper class for picking the correct pronoun to use. The arguments
        should be ordered in the same way as possible_pronouns (declared
        in the pronoun_setup.rpy file).

        The special keyword 'custom' can be used to support custom pronouns.
        It should correspond to the name of a field in the CustomPronoun
        class (declared above).
        """
        def __init__(self, *args, **kwargs):
            """
            Declare words for each pronoun set declared in possible_pronouns.
            """
            self.args = args
            self.custom = kwargs.pop("custom", None)

        def __str__(self):
            """
            A string representation of this pronoun or word. Ren'Py fetches this
            when you interpolate this object in dialogue like "[them]", so it's
            possible to do logic here to get the right word.
            """

            ## Is the player using custom pronouns?
            if store.pronoun == "custom":
                # Yes, using custom pronouns.
                try:
                    return getattr(store.custom_pronouns, self.custom)
                except TypeError:
                    # custom field not provided
                    if config.developer:
                        raise TypeError("Must provide a custom field in order to use custom pronouns with this word")
                    else:
                        return self.args[0]

            ## See if there is a corresponding pronoun entry
            ## Find the pronoun index
            ind = store.possible_pronouns.index(store.pronoun)

            # Finally, get the entry corresponding specifically to this
            # pronoun set
            try:
                return self.args[ind]
            except IndexError:
                # Out of range
                if config.developer:
                    raise IndexError("Couldn't find a word associated with %r for pronouns" % store.pronoun)
                else:
                    return self.args[-1]
            except TypeError:
                # index is None
                if config.developer:
                    raise IndexError("Couldn't find %r in possible_pronouns. Did you forget to add it?" % store.pronoun)
                else:
                    return self.args[-1]

            return ""


    class PronounVerb():
        """
        A special class to easily conjugate verbs for pronouns.

        Attributes:
        -----------
        plural : string
            The plural verb conjugation.
        singular : string
            The singular verb conjugation.
        """
        def __init__(self, plural, singular):
            """Create a PronounVerb object."""
            self.plural = plural
            self.singular = singular

        def __str__(self):
            """
            A string representation of this verb based on the player's
            current pronouns.
            """
            ## Use the plural or singular based on whether this pronoun
            ## set is plural or singular.
            if (store.pronoun in store.plural_pronouns
                    or (store.pronoun == "custom"
                        and store.custom_pronouns.is_plural)):
                return self.plural
            else:
                return self.singular


    class Term():
        """
        A special class to choose gendered terms based on the player's
        preferences.

        Attributes:
        -----------
        neutral : string
            The neutral term.
        feminine : string
            The feminine term. Defaults to the neutral term if not provided.
        masculine : string
            The masculine term. Defaults to the neutral term if not provided.
        id : string
            A unique identifier for this term. Used to save the player's
            preferences for this term in a dictionary.
        description : string
            A description of what this collection of terms is referring to.
            Can be used in a screen later.
        possibilities : list
            A list of the unique words that are part of this Term.
        other : list
            A list of any other terms a player can choose from if using
            advanced term customization.
        """
        ALL_TERMS = [ ]
        ID_TO_TERM = dict()

        def __init__(self, neutral=None, feminine=None, masculine=None,
                id=None, description=None, other=None):
            """Create a Term object."""
            self.neutral = neutral or ""
            self.feminine = feminine or neutral
            self.masculine = masculine or neutral
            self.id = id
            ## Save the different words in a list without duplicates
            possibilities = [ ]
            if self.neutral:
                possibilities.append(self.neutral)
            if self.feminine and self.feminine not in possibilities:
                possibilities.append(self.feminine)
            if self.masculine and self.masculine not in possibilities:
                possibilities.append(self.masculine)
            self.possibilities = possibilities

            if not description:
                ## Make the description just the terms
                ## e.g. "person / woman / man"
                self.description = " / ".join(possibilities)
            else:
                ## Generally this is a description of sort of "group" these
                ## terms belong to, e.g. "Honorifics"
                self.description = description

            if other is not None:
                if not isinstance(other, list):
                    other = [ other ]
                self.possibilities += other

            ## The class attribute holds all the Terms declared in the game.
            self.ALL_TERMS.append(self)
            ## Also save it to the dictionary for easy lookup
            self.ID_TO_TERM[self.id] = self

        def get_term_from_preferences(self, pronoun):
            """
            Returns the player's preferred term, given their term preferences
            and the provided pronouns (if applicable).
            """
            if store.terms == "custom":
                ## The player wants the game to choose which terms to use
                ## based on their pronouns. Use feminine terms if the player
                ## uses she/her, masculine terms if the player uses he/him,
                ## and neutral terms otherwise.
                t = "feminine" if pronoun == "she/her" else "masculine" if pronoun == "he/him" else "neutral"
            else:
                t = store.terms

            if t == "feminine":
                return self.feminine
            if t == "masculine":
                return self.masculine
            else:
                return self.neutral

        def __str__(self):
            """
            A string representation of this term based on the player's
            current term preferences.
            """
            ## Grab the term from the player's custom terms dictionary
            return get_custom_term(self.id)


    def get_custom_term(id, selected_pronouns="unset"):
        """
        Returns the player's custom term for the given id.

        Parameters:
        -----------
        id : string
            The id corresponding to an instance of the Term class.
        selected_pronouns : string
            The pronoun set to use. If "unset", use the player's current
            pronouns.
        """
        if selected_pronouns == "unset":
            selected_pronouns = store.pronoun
        ## First, is there a specific entry for their pronouns?
        ret = store.custom_terms.get(selected_pronouns, None)
        ## If not, use the None key
        if ret is None:
            key = None
        else:
            key = selected_pronouns
            ## First, have they typed in a term for this?
            ret = store.player_inputted_terms.get(key, dict()).get(id, None)
            if ret:
                return ret

            ## Does the player have a custom term for this pronoun
            ## set with this id?
            ret = store.custom_terms.get(key, dict()).get(id, None)

            if ret is None:
                key = None

        ret = store.player_inputted_terms.get(key, dict()).get(id, None)
        if ret:
            return ret
        ret = store.custom_terms.get(key, dict()).get(id, None)

        if ret is None:
            ## Ultimately, they have not chosen a term for this.
            ## Grab the term normally.
            return Term.ID_TO_TERM[id].get_term_from_preferences(selected_pronouns)
        return ret

    class SetAllTerms(Action):
        """
        An Action which sets all terms of a particular category to the
        provided preference.
        """
        def __init__(self, key, term_type):
            """
            Create a SetAllTerms action.

            Parameters:
            -----------
            key : string
                The pronoun set to set the custom term for.
            term_type : string
                One of "neutral", "feminine", "masculine", or None, with which
                to set all terms to.
            """
            self.key = key
            self.term_type = term_type

        def __call__(self):
            """Execute this action."""
            ## Reset all the input as well
            for term in store.player_inputted_terms[self.key].keys():
                store.player_inputted_terms[self.key][term] = ""

            if self.term_type is None:
                ## That means they want to wipe all custom terms
                store.custom_terms[self.key] = dict()
            else:
                ## Otherwise, we're manually setting all terms to the
                ## provided type
                for term in Term.ALL_TERMS:
                    if self.term_type == "feminine":
                        store.custom_terms[self.key][term.id] = term.feminine
                    elif self.term_type == "masculine":
                        store.custom_terms[self.key][term.id] = term.masculine
                    else:
                        store.custom_terms[self.key][term.id] = term.neutral

            renpy.restart_interaction()

    class SetCustomTerm(Action):
        """
        An action which makes it simple to set a custom term preference.
        """
        def __init__(self, key, word):
            """
            Create a SetCustomTerm action.

            Parameters:
            -----------
            key : string
                The pronoun set to set the custom term for.
            word : string
                The word to set the term to.
            """
            self.key = key
            self.word = word

        def get_selected(self):
            """Return True if this term has been customized."""
            term = store.active_term.id
            return has_custom_term(self.key, term)

        def __call__(self):
            """Set the custom term."""
            term = store.active_term.id
            ## Make sure the player has a custom term dictionary
            if store.custom_terms is None:
                store.custom_terms = dict()
            ## Make sure the player has a dictionary for this pronoun set
            if store.custom_terms.get(self.key, None) is None:
                store.custom_terms[self.key] = dict()
            ## Set the custom term
            store.custom_terms[self.key][term] = self.word
            ## Also clear any typed terms, since this overrides that
            store.player_inputted_terms[self.key][term] = ""
            renpy.restart_interaction()


    class CycleCustomTerm(Action):
        """
        An action which makes it simple to cycle through a term preference.
        """
        def __init__(self, key, term, direction=1, loop=True):
            """
            Create a CycleCustomTerm action.

            Parameters:
            -----------
            key : string
                The pronoun set to set the custom term for.
            term : Term
                The term to cycle through.
            direction : int
                The direction to cycle in.
            loop : bool
                Whether to loop around when cycling.
            """
            self.key = key
            ## Get the next term
            lst = term.possibilities

            current_index = lst.index(get_custom_term(term.id, key))
            if current_index is None:
                self.sensitive = True
                self.next = lst[0]
                return

            self.sensitive = True
            if loop:
                self.next = lst[(current_index + direction) % len(lst)]
            else:
                self.next = lst[max(min((current_index + direction), len(lst)), 0)]
            ## Not sensitive if there's no next item.
            if self.next == current_index:
                self.sensitive = False

        def get_sensitive(self):
            """Return whether this action is sensitive."""
            return self.sensitive

        def get_selected(self):
            """Return True if this term has been customized."""
            term = store.active_term.id
            return has_custom_term(self.key, term)

        def __call__(self):
            """Set the custom term."""
            term = store.active_term.id
            ## Make sure the player has a custom term dictionary
            if store.custom_terms is None:
                store.custom_terms = dict()
            ## Make sure the player has a dictionary for this pronoun set
            if store.custom_terms.get(self.key, None) is None:
                store.custom_terms[self.key] = dict()
            ## Set the custom term
            store.custom_terms[self.key][term] = self.next
            ## Also clear any typed terms, since this overrides that
            store.player_inputted_terms[self.key][term] = ""
            renpy.restart_interaction()



    def has_custom_term(key, term):
        return (store.custom_terms.get(key, dict()).get(term, None) is not None
            or store.player_inputted_terms.get(key, dict()).get(term,
                None))


    class TermInputValue(DictInputValue):
        """
        A custom InputValue class to make it easy for players to input
        their own terms.

        Attributes:
        -----------

        """
        def __init__(self, term, pronoun):
            """
            Create a TermInputValue object.

            Parameters:
            -----------
            term : Term
                The term to set.
            pronoun : string
                The pronoun set to set the custom term for.
            """
            self.term = term
            self.pronoun = pronoun
            self.default = False
            self.returnable = False

        def get_text(self):
            return store.player_inputted_terms.setdefault(
                self.pronoun, dict()).setdefault(self.term.id, "")

        def set_text(self, text):
            store.player_inputted_terms.setdefault(
                self.pronoun, dict())[self.term.id] = text
            renpy.restart_interaction()

        def enter(self):
            """Disable this input when the user presses Enter."""
            renpy.run(self.Disable())
            raise renpy.IgnoreEvent()


    def create_term_input_values():
        """
        A helper function which creates a dictionary of TermInputValue
        objects corresponding to each Term in the game.
        This is needed so that the inputs can be toggled on the custom
        terms page.
        """
        ret = dict(zip(possible_pronouns+[None], [dict() for x in range(len(possible_pronouns)+1)]))
        for term in Term.ALL_TERMS:
            for pronoun in possible_pronouns+[None]:
                ret[pronoun][term.id] = TermInputValue(term, pronoun)
        return ret


################################################################################
##
## Multiple Pronouns ###########################################################
##
################################################################################
## Additional code for allowing players to choose and use multiple pronoun
## sets in the same playthrough.
################################################################################

init -10 python:

    class RandomBag(object):
        """
        Class that is used to create a 'random bag' of supplied choices.
        Adapted from https://www.patreon.com/posts/python-tricks-2-23663471
        by Ren'Py Tom (publicly available through Patreon).

        Attributes:
        -----------
        choices : list
            A list of choices. Can be booleans, strings, ints, a mix, etc.
        bag : list
            A shuffled list of the provided choices.
        """

        def __init__(self, choices):
            """Creates a RandomBag object."""
            self.choices = choices
            self.bag = [ ]

        def draw(self):
            """Removes an item from the bag."""
            # If the bag is empty,
            if not self.bag:
                # Replace it with a copy of choices,
                self.bag = list(self.choices)
                # Then randomize those choices.
                renpy.random.shuffle(self.bag)
            # Return something from the bag.
            return self.bag.pop(0)


    def pretty_print_pronouns():
        """
        A helper function which returns a "pretty" version of the player's
        pronouns, for use in the UI or in dialogue.
        Returns a string like "she/her, he/him, they/them, and xe/xem"
        """
        pretty_set = [x for x in store.player_pronouns if x != "custom"]
        if "custom" in store.player_pronouns:
            ret = ", ".join(pretty_set)
            if len(store.player_pronouns) > 1:
                if len(store.player_pronouns) > 2:
                    ret += ","
                ret += " and {}/{}".format(custom_pronouns.they, custom_pronouns.them)
            else:
                ret += "{}/{}".format(custom_pronouns.they, custom_pronouns.them)
        else:
            ret = ", ".join(pretty_set[:-1])
            if len(pretty_set) > 2:
                ret += ","
            if len(pretty_set) > 1:
                ret += " and "
            ret += pretty_set[-1]
        return ret

    def randomize_pronouns():
        """
        A function which will randomize the player's pronouns based on their
        preferences for frequency.
        """
        if store.pronoun_switch_freq is None:
            ## This player is manually changing their pronouns.
            ## Do not randomize anything.
            return

        if len(store.player_pronouns) == 1:
            ## There's only one pronoun that the player is using, so
            ## no randomization to do.
            return

        if not store.pronoun_frequency:
            ## The dictionary is empty; this means we'll have an equal
            ## chance of using each pronoun.
            store.pronoun = renpy.random.choice(store.player_pronouns)
            return

        ## Make sure at least one of the pronoun frequencies is not 0
        if not any(store.pronoun_frequency.values()):
            ## If they're all 0, just pick a random pronoun.
            return

        ## Take the "Random Bag" approach.
        if not store.pronoun_freq_list:
            ## If the list is empty, create it.
            freq_list = [ ]
            for pron in store.player_pronouns:
                ## If the player has specified a frequency for this
                ## pronoun, add it to the list that many times.
                freq_list.extend([pron for x in range(store.pronoun_frequency.get(pronoun, 1))])
            if not freq_list:
                ## If the list is empty, return
                return
            store.pronoun_freq_list = RandomBag(freq_list)
        else:
            ## Otherwise, just draw from the bag.
            store.pronoun = store.pronoun_freq_list.draw()

    def randomize_pronouns_per_line(*args, **kwargs):
        """
        An interaction callback which will randomize the player's pronouns on
        every line, if they have selected that option.
        """
        if store.pronoun_switch_freq != "line":
            return
        ## Otherwise yes, randomize.
        randomize_pronouns()

    ## Add this to interact_callbacks so that it will be automatically run
    ## on every new line of dialogue.
    config.start_interact_callbacks.append(randomize_pronouns_per_line)

    class OldPronoun(NoRollback):
        def __init__(self):
            super(OldPronoun, self).__init__()
            self.op = ''

    class CycleList(Action):
        """
        An action that cycles through a list and returns the next item
        according to the current one + the specified direction.

        Attributes:
        -----------
        field : string
            The name of the field to change.
        sensitive : bool
            True if this action is sensitive, False otherwise.
        next : string
            The next item in the list.
        """
        def __init__(self, lst, current, direction=1, loop=True):
            """
            Create a CycleList object
            lst : list
                The list to cycle through.
            current : string
                The current item in the list.
            direction : int
                The direction to cycle through the list. 1 for forward, -1 for
                backward.
            loop : bool
                Whether to loop around the list or not.
            """
            self.field = current
            var = getattr(store, current)
            current_index = lst.index(var)
            self.sensitive = True
            if loop:
                self.next = lst[(current_index + direction) % len(lst)]
            else:
                self.next = lst[max(min((current_index + direction), len(lst)), 0)]
            ## Not sensitive if there's no next item.
            if self.next == current_index:
                self.sensitive = False

        def get_sensitive(self):
            """Return whether this action is sensitive."""
            return self.sensitive

        def __call__(self):
            """Call this action."""
            setattr(store, self.field, self.next)
            renpy.restart_interaction()


    class TogglePronoun(Action):
        """
        An Action to make it easier to add and remove possible pronouns
        from the player's set of pronouns.
        """
        def __init__(self, pronoun):
            """
            Create a TogglePronoun object.

            Parameters:
            -----------
            pronoun : string
                The pronoun to toggle.
            """
            self.pronoun = pronoun

        def get_selected(self):
            return self.pronoun in store.player_pronouns

        def __call__(self):
            """
            Call this action. This code ensures that store.pronoun
            is never equal to something that isn't in the list of possible
            pronouns, even if clicking this button removes the player's current
            pronouns from the list of possible pronouns.
            """
            if self.pronoun in store.player_pronouns:
                ## Pick a different pronoun for the player
                if store.pronoun == self.pronoun:
                    if len(store.player_pronouns) > 1:
                        store.pronoun = renpy.random.choice([x for x in store.player_pronouns if x != self.pronoun])
                    else:
                        store.pronoun = ""
                store.player_pronouns.remove(self.pronoun)
            else:
                store.player_pronouns.append(self.pronoun)
                if store.pronoun == "" or len(store.player_pronouns) == 1:
                    store.pronoun = self.pronoun
            renpy.restart_interaction()


    def reset_pronoun_variables(reset_custom=False):
        """
        A convenience method to reset any pronouns, terms, etc. to
        their default values.

        Parameters:
        -----------
        reset_custom : bool
            If True, also reset the custom pronouns.
        """
        store.terms = "custom"
        store.pronoun = ""
        store.player_pronouns.clear()
        store.pronoun_switch_freq = None
        store.pronoun_freq_list = None
        store.pronoun_frequency = dict(zip(store.possible_pronouns, [1 for x in range(len(store.possible_pronouns))]))
        store.custom_terms = dict(zip(store.possible_pronouns+[None], [dict() for x in range(len(store.possible_pronouns)+1)]))
        store.player_inputted_terms = dict(zip(store.possible_pronouns+[None], [dict() for x in range(len(store.possible_pronouns)+1)]))
        store.active_term = None

        if reset_custom:
            store.custom_pronouns = CustomPronoun("", "", "", "", "", False)


init 30:
    ############################################################################
    ## Variables for Multiple Pronouns and Custom Terms
    ############################################################################
    ## These are not intended to be changed, so they are kept here instead
    ## of in the pronoun_setup.rpy file.

    ## One of "line", to randomize pronouns every line, "scene", to randomize
    ## pronouns each new scene, or None, so the player must manually change
    ## their pronouns.
    ## You the creator are responsible for the calls to randomize_pronouns()
    ## when the player has selected "scene", but the interact callback is used
    ## for the "line" option. How to use this is demonstrated in the label
    ## below.Typically this is also a value you will not change, as you should
    ## let players choose whether they want to randomize their pronouns or not.
    default pronoun_switch_freq = None

    ## A dictionary of how frequently the player wants each of their pronouns
    ## used. Typically you will not change this.
    default pronoun_frequency = dict(zip(possible_pronouns, [1 for x in range(len(possible_pronouns))]))
    ## This is a special "random bag" which we'll pick pronouns from in order
    ## to reduce randomization from picking out the same pronoun over and over.
    ## Again, typically you will not change this.
    default pronoun_freq_list = None

    ############################################################################
    ## Variables for Custom Terms
    ############################################################################
    ## These are variables relating to custom terms. Unless you know what
    ## you're doing, most of these do not need to be changed (as they are
    ## typically adjusted by the player via screens or in-script).

    ## A dictionary of dictionaries such that custom_terms["she/her"]["person"]
    ## will return which term the player has set for "person" if they are using
    ## she/her pronouns. The special None key sets the defaults for all pronouns.
    default custom_terms = dict(zip(possible_pronouns+[None], [dict() for x in range(len(possible_pronouns)+1)]))

    ## The term the player is currently editing.
    ## You will generally not change this.
    default active_term = None

    ## Terms the player has typed into the custom term screen. You will
    ## generally not change this.
    default player_inputted_terms = dict(zip(possible_pronouns+[None], [dict() for x in range(len(possible_pronouns)+1)]))
    ## This is a special value which stores created InputValue objects
    ## for each of the possible pronouns.
    define create_term_input_values = create_term_input_values()
