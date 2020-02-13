#Reilly McBride
#2/23/18

import nltk, re, pprint
from nltk.corpus import conll2002

from matplotlib import pyplot as plt
import math
import random


#nltk.download('stopwords')
#nltk.download('conll2000')

emma = nltk.Text(nltk.corpus.gutenberg.words("austen-emma.txt"))
paradise = nltk.Text(nltk.corpus.gutenberg.words("milton-paradise.txt"))
sense = nltk.Text(nltk.corpus.gutenberg.words("austen-sense.txt"))
bible = nltk.Text(nltk.corpus.gutenberg.words("bible-kjv.txt"))
hamlet = nltk.Text(nltk.corpus.gutenberg.words("shakespeare-hamlet.txt"))
bryant = nltk.Text(nltk.corpus.gutenberg.words('bryant-stories.txt'))

def seven():
    print("EMMA")
    print(emma.concordance("However"))
    print("BIBLE")
    print(bible.concordance("However"))
    print("HAMLET")
    print(hamlet.concordance("However"))

def nine():
    print("emma")
    emma.similar("love")
    print("sense")
    sense.similar("love")
    emma.common_contexts(["love", "marriage"])
    sense.common_contexts(["love", "marriage"])

def twelve():
    entries = nltk.corpus.cmudict.entries()
    words = set(entry[0] for entry in entries)
    print(len(words))
    dictionary = nltk.corpus.cmudict.dict()
    unique = 0
    for key in dictionary.keys():
        if len(dictionary[key]) > 1:
            unique += 1
    print(unique/len(words))

def thirteen():
    number_with_none = 0
    synsets = list(nltk.corpus.wordnet.all_synsets('n'))
    for syn in synsets:
        if len(list(syn.hyponyms())) == 0:
            number_with_none += 1
    print((number_with_none/len(synsets)) * 100)

def fifteen():
    count = 0
    fdist = nltk.FreqDist(word for word in nltk.corpus.brown.words())
    for entry in fdist:
        if fdist[entry] >= 3:
            count += 1
    print(count)

def seventeen():
    fdist = nltk.FreqDist(word for word in emma if word.lower() not in nltk.corpus.stopwords.words('english') and word.isalpha())
    print(fdist.most_common(50))

def process_text(text):
    fdist = nltk.FreqDist(word.lower() for word in text)
    common_ranked = fdist.most_common(len(fdist))
    x_list = []
    y_list = []
    count = 1
    for i in common_ranked:
        x_list.append(count)
        count += 1
        y_list.append(math.log10(i[1]))
    plt.plot(x_list, y_list)
    plt.xlabel("Rank")
    plt.ylabel("Frequency: Log 10")
    plt.show()

def twentythree():
    #PART A:
    #process_text(nltk.corpus.brown.words())
    #PART B:
    test_string = ""
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', ' ']
    for i in range(1000000):
        temp = random.choice(chars)
        test_string = test_string + temp
    test_text = nltk.word_tokenize(test_string)
    process_text(test_text)

def twentysix():
    synsets = list(nltk.corpus.wordnet.all_synsets('n'))
    count = 0
    sum = 0
    for syn in synsets:
        hyps = list(syn.hyponyms())
        if len(hyps) != 0:
            count += 1
            sum += len(hyps)
    print(sum/count)


#CHAPTER SEVEN

class BigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sents]
        self.tagger = nltk.BigramTagger(train_data)

    def parse(self, sentence):
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag)
                     in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)



def three_seven():
    test_sentences = (nltk.corpus.conll2000.chunked_sents('train.txt', chunk_types=['NP']))
    grammar = r"""
        NP: 
            {<DT|PP\$>?<NN|NNS>*<JJ|JJR>*<CD>*<NN|NNS>} 
            {<DT|PP\$>?<JJ>?<NNP>+<CD>?<JJ>?<NN>?}   
            {<DT|PP\$>?<JJ>?<NN>+}
            {<PRP>+}
            {<WP>+}
        """
    #{<DT|PP\$>?<NN>*<JJ>*<NN>}
    cp = nltk.RegexpParser(grammar)
    #print(cp.parse(test_sentences[0]))
    chunkscore = cp.evaluate(test_sentences)
    for c in chunkscore.missed():
        print(c)
    print(chunkscore)

def seven_seven():
    test_sents = nltk.corpus.conll2000.chunked_sents('test.txt', chunk_types=['NP'])

    grammar = r"""
        NP: 
            {<DT|PP\$>?<NN|NNS>*<JJ|JJR>*<CD>*<NN|NNS>} 
            {<DT|PP\$>?<JJ>?<NNP>+<CD>?<JJ>?<NN>?}   
            {<DT|PP\$>?<JJ>?<NN>+}
            {<PRP>+}
            {<WP>+}
        """

    #grammar = r"NP: {<[CDJNP].*>+}"

    chunker = nltk.RegexpParser(grammar)

    chunkscore = chunker.evaluate(test_sents)
    print(chunkscore)
    #print(chunkscore.incorrect())
    #print(chunkscore.missed())

if __name__ == "__main__":
    #seven()
    #nine()
    #twelve()
    #thirteen()
    #fifteen()
    #seventeen()
    #twentythree()
    #twentysix()
    #three_seven()
    seven_seven()
