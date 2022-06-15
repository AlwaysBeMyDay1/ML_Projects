# The way can remove proper nouns without wordnet
import nltk
from nltk.tag import pos_tag

def extract_proper_noun(text):
    tagged_text = pos_tag(text.split())
    propernouns = [word for word,pos in tagged_text if pos == 'NNP']
    return propernouns

def remove_proper_noun(text):
    tagged_text = pos_tag(text.split())
    non_propernouns = [word for word,tag in tagged_text if tag != 'NNP' and tag != 'NNPS']
    cleaned_text = ' '.join(non_propernouns)
    return cleaned_text
