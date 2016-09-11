#!/usr/bin/python

from __future__ import division
import random
import sys


sentence = ""

def collect_grammar(filename):
    """ Collects grammar from the text file containing the grammar """
    try:
        f = open(filename+".txt")
        productions = list()
        for line in f.readlines():
            if line_not_ignorable(line):
                productions.append(line.strip())
        return productions
    except Exception:
        print "Could not open file " + filename + ".txt"
        sys.exit()


def line_not_ignorable(line):
    """ Returns true if the line read from the grammar file is actual grammar """
    return not line.startswith("#") and not line in ['\n', '\r\n']


def group_productions(productions):
    """ Puts together all the Non-terminals in the given list of productions  """
    grouped_productions = dict()
    for production in productions:
        if get_non_terminal(production) in grouped_productions:
            # if the non_terminal already exists in the dictionary, just merge the production to the existing one
            grouped_productions[get_non_terminal(production)] = grouped_productions[get_non_terminal(production)] + [production]
        else:
            # if the non_terminal doesn't exist in the dictionary, make a new entry
            grouped_productions[get_non_terminal(production)] = [production]
    return grouped_productions


def get_weight(production):
    """ Given a production, returns the weight of the production """
    return int(production.split("\t")[0])


def get_non_terminal(production):
    """ Given a production, returns the non terminal from the production """
    return production.split("\t")[1]


def get_right_hand_side(production):
    """ Given a production, returns the right hand side of the production """
    return production.split("\t")[2]


def select(symbol, grouped_productions):
    productions = grouped_productions[symbol]
    r = random.random()
    index = 0
    while(r >= 0 and index < len(productions)):
        r -= get_weight(productions[index]) / total_weight(productions)
        index += 1
    return productions[index - 1]

def total_weight(productions):
    total_weight = 0
    for production in productions:
        total_weight += get_weight(production)
    return total_weight

def symbol_to_terminal(symbol, gp):
    """ Takes the symbol and takes it up to a terminal """
    global sentence

    prod = select(symbol, gp)
    rhs = get_right_hand_side(prod)

    for symbol in rhs.split(" "):
        if symbol not in gp and symbol is not None:
            sentence += symbol + " "
        while symbol in gp:
            symbol = symbol_to_terminal(symbol, gp)
            if symbol not in gp and symbol is not None:
                sentence += symbol + " "


def generate(gp):
    global sentence

    start = select("START", gp)
    # From this point onward, we need to feed our generate machine right hand sides of productions
    symbol_to_terminal(get_right_hand_side(start), gp)
    print sentence


def main(argv):
    global sentence

    # Print error message if the command does not contain all the arguments
    if len(argv) != 3:
        sys.exit("Invalid command.\nUsage: ./generate filename number_of_sentences")
    # Otherwise, generate sentences based on the given arguments
    else:
        gp = group_productions(collect_grammar(argv[1])) # create a dictionary of grouped_productions from given grammar file
        for i in range(0, int(argv[2])):
            generate(gp)
            sentence = "" # Make sentence null before each generate function call


if __name__ == "__main__":
    main(sys.argv)    
