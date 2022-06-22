# The way can remove proper nouns without wordnet
from nltk.tag import pos_tag

# Tag   ||  Meaning              ||  English Examples
# ------------------------------------------------------------------------
# ADJ   ||  adjective            ||  new, good, high, special, big, local
# ADP   ||  adposition           ||  on, of, at, with, by, into, under
# ADV   ||  adverb               ||  really, already, still, early, now
# CONJ  ||  conjunction          ||  and, or, but, if, while, although
# DET   ||  determiner, article  ||  the, a, some, most, every, no, which
# NOUN  ||  noun                 ||  year, home, costs, time, Africa
# NUM   ||  numeral              ||  twenty-four, fourth, 1991, 14:24
# PRT   ||  particle             ||  at, on, out, over per, that, up, with
# PRON  ||  pronoun              ||  he, their, her, its, my, I, us
# VERB  ||  verb                 ||  is, say, told, given, playing, would
# .     ||  punctuation marks    ||  . , ; !
# X     ||  other                ||  ersatz, esprit, dunno, gr8, univeristy


def remove_proper_noun(text):
    tagged_text = pos_tag(text.split())
    non_propernouns = [word for word,tag in tagged_text if tag != 'NNP' and tag != 'NNPS']
    cleaned_text = ' '.join(non_propernouns)
    return cleaned_text

def extract_proper_noun(text):
    tagged_text = pos_tag(text.split())
    propernouns = [word for word,pos in tagged_text if pos == 'NNP']
    return propernouns

def extract_noun(text):
    tagged_text = pos_tag(text.split())
    nouns = [word for word,pos in tagged_text if pos == 'NN']
    cleaned_text = ' '.join(nouns)
    return cleaned_text

def remove_adjective(text):
    tagged_text = pos_tag(text.split())
    non_adjective = [word for word,tag in tagged_text if tag != 'JJ']
    cleaned_text = ' '.join(non_adjective)
    return cleaned_text

def extract_adjective(text):
    tagged_text = pos_tag(text.split())
    adjectives = [word for word,tag in tagged_text if tag == 'JJ']
    cleaned_text = ' '.join(adjectives)
    return cleaned_text

# return False if inputted word is all proper nouns
def distinct_proper_noun(word):
    cleaned_word = remove_proper_noun(word)
    return False if cleaned_word == '' else cleaned_word
