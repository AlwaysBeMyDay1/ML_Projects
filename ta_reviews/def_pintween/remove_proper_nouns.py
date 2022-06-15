# The way can remove proper nouns without wordnet
import nltk
from nltk.tag import pos_tag

sentence = "Michael Jackson likes to eat at McDonalds"
tagged_sent = pos_tag(sentence.split())
# [('Michael', 'NNP'), ('Jackson', 'NNP'), ('likes', 'VBZ'), ('to', 'TO'), ('eat', 'VB'), ('at', 'IN'), ('McDonalds', 'NNP')]
print(tagged_sent)
propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
# ['Michael','Jackson', 'McDonalds']

tagged_sentence = nltk.tag.pos_tag(sentence.split())
edited_sentence = [word for word,tag in tagged_sentence if tag != 'NNP' and tag != 'NNPS']
print(' '.join(edited_sentence))
# I am named