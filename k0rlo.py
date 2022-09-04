import os
import re
import sys

#
#Gather script information
#
script_path = os.path.abspath(sys.argv[0])

default_split = r'[,:;\s\t]+'
helpfile_extension = ".help"

script_help = script_path + helpfile_extension

#
#See if a help file exists
#
if os.path.exists(script_help):
    #
    #If the help file exists, read it in
    #
    f = open(script_help, "r")
    script_help = f.read()
    f.close()
else:
    #
    #No help file report no help
    #
    script_help = """
No script help file.
"""

def get_input(help, prompt):
    """
    Get input string from console.
    Print rapid logger help if "HELP" is specified and then ask for input again.
    Strip off all leading and trailing blanks on input string.
    Upcase input string if requested (Default).

    Arguments:
        help:   Text to print if help on this prompt is requested
        prompt: String to print as question prompt
        upcase: If True, upcase the input

    Returns:
        Tuple:  First string upcased input, second original input.
                If no input, a null string is returned ("") which is boolean
                False in Python.
    """

    while(True):
        #
        #Get input, strip blanks and upcase
        #
        text = str(input(prompt)).strip()

        #
        #If help is  requested, display entire program help
        #
        if text.upper() == "HELP":
            print(script_help)
            continue

        #
        #If "EXIT" entered, exit
        #
        if text.upper() == "EXIT":
            exit()

        #
        #If input is "?" or <Enter> without a default (question having a "[" in
        #it), print help text
        #
        if (text == "?") or not (text or re.search(r'\[', prompt)):
            print("""
Type "EXIT" to exit logger.
Type "?" for this help.
""" + help + """
Type "HELP" for more information.
""")
            continue

        break

    #
    #Return the text from the console
    #
    return(text)


def get_yes_no(help, prompt, default="Y"):
    """
    Get input string from console.
    Print rapid logger help if "HELP" is specified and then ask for input again.
    Strip off all leading and trailing blanks on input string.
    Upcase input string if requested (Default).

    Arguments:
        help:       Text to print if help on this prompt is requested
        prompt:     String to print as question prompt
        default:    Default, Y or N if nothing typed

    Returns:
        True if yes
        False if no
    """

    default_prompt = {"Y" : " [(Y), n]",
        "N" : " [(N), y]"}

    default = default[:1].upper()

    #
    #Runtime programming check: Make sure "Y" or "N" was supplied as a default.
    #If this fails, the program immediately exits.
    #
    if default not in default_prompt:
        print("""
Severe error: Default supplied for get_yes_no was "{}". It must be "Y" or "N"
""".format(default))
        exit (1)

    #
    #Keep trying until you get a "Y", "N" or an <Enter> (which says take the
    #default).
    #
    while(True):
    
        #
        #Ask the question and get an upcased response.
        #
        answer = get_input(help,
            prompt.rstrip() + default_prompt[default] + ": ").upper()

        #
        #If just <Enter>, set the response to the default.
        #
        if not answer:
            answer = default

        #
        #Reduce answer to first character and upcase
        #
        answer = answer[:1].upper()

        #
        #If valid response, return True if "Y", False if "N".
        #
        if answer in default_prompt:
            return(answer == "Y")

        #
        #Invalid response, report error and ask again.
        #
        print("""
Error: First character of answer must be 'Y' or 'N' or <Enter> to use the
       default of "{}".
""".format(default))

def valid_callsign(callsign, slash=True):
    """
    Validate the callsign against the expected format

    Arguments:
        callsign:   String containing callsign.
        slash:      True if a slash is allowed in the callsign name.

    Returns:
        String (True) if error with error text.
        False if callsign formatted correctly
    """

    if slash:
        if not re.fullmatch(r'[A-Z0-9]{3,}(/[A-Z0-9]+|$)', callsign):
            #
            #If an error is found, report it
            #
            return("""
Error: "{}" is not a valid format for a callsign. It must be three or
       more letters and digits only. Callsign may be terminated by a "/"
       followed by one or more letters and digits.
       Examples: "K0RLO", "W1JU" or "K0RLO/R1", "W1JU/MOBILE"
""".format(callsign))
    else:
        if not re.fullmatch(r'[A-Z0-9]{3,}', callsign):
            #
            #If an error is found, report it
            #
            return("""
Error: "{}" is not a valid format for a callsign. It must be three or
       more letters and digits only. It may NOT contain a "/"!
       Examples: "K0RLO" or "W1JU"
""".format(callsign))

    #
    #It's a correctly formatted callsign, return false.
    #
    return(False)

