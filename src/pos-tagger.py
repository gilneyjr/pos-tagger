#!/usr/bin/python3
from parser import Parser
from preproccess import cleanData, caseFolding, normalization
import sys


# JUST FOR TESTS (REMOVE AFTER) =============================== 
import re
def testPreprocessing(sentences):
    for sentence in sentences:
        for tag, word in sentence:
            if re.match('-NONE-|-LRB-|-RRB-', tag):
                print("[ERROR] Invalid tag (" + tag + ',' + word + ')')
            elif re.match('.*[A-Z].*', word):
                print("[ERROR] Upper case (" + tag + ',' + word + ')')
            elif re.match('.*[02-9]+.*', word):
                print("[ERROR] Number different to 1 (" + tag + ',' + word + ')')

class PosTagger:
    def __init__(self):
        self.data = None

# struct of data
# data = {
#     'a': {
#         'NN': 1,
#         'VB': 0
#         ...
#     },
#     'b': {
#         'NN': 6,
#         'VB': 3
#         ...
#     },
# }
    def train(self, sentences, accumulate=False):
        if not self.data or not accumulate:
            self.data = {}

        # train
        for sentence in sentences:
            for tag, word in sentence:
                # if word doesn't exist, create it
                if not word in self.data:
                    self.data[word] = {}
                # count (tag, word)
                self.data[word][tag] = 1 if not tag in self.data[word] else self.data[word][tag]+1

        # treat unknown
        unk = {}
        remove_after = []
        for word, content in self.data.items():
            # count word
            count = 0
            for val in content.values():
                count = count+val

            # if there's at most 4, make that word UNK
            if count < 5:
                # append content to unk
                for tag, tagCount in content.items():
                    # if UNK has never tagged with tag, tag it
                    if not tag in unk:
                        unk[tag] = 0

                    # sum tagCount to unk[tag]
                    unk[tag] = unk[tag]+tagCount

                # add word to remove_after
                remove_after.append(word)
        self.data['__UNK__'] = unk
        for w in remove_after:
            self.data.pop(w)

        self.wordTag = {}
        for word, content in self.data.items():
            # calculate the most frequent tag
            _max = None
            for tag, count in content.items():
                if _max == None or count > _max[1]:
                    _max = (tag,count)

            # add it to res
            if _max != None:
                self.wordTag[word] = _max[0]

        return self.wordTag

    def test(self, sentences):
        count_ok = 0
        count_fail = 0 
        for sentence in sentences:
            for tag, word in sentence:
                # test if word is UNK
                _word = word
                if not _word in self.wordTag:
                    _word = '__UNK__'

                if self.wordTag[_word] == tag:
                    count_ok = count_ok + 1
                else:
                    count_fail = count_fail + 1
        return (count_ok, count_fail)

# =============================================================

def parseAndPreprocess(file):
    # parse
    print('Parsing sentences...')
    parser = Parser()
    sentences = parser.getSentences(parser.parse(file))

    # pre-process
    print('Pre-processing data...')
    for i in range(len(sentences)):
        cleanData(sentences[i])
        caseFolding(sentences[i])
        normalization(sentences[i])

    return sentences

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[ERROR]: No train file was passed as argument')
        quit()

    if len(sys.argv) < 3:
        print('[ERROR]: No test file was passed as argument')
        quit()

    
    # parse and preprocess
    sentences_train = parseAndPreprocess(sys.argv[1])
    sentences_test  = parseAndPreprocess(sys.argv[2])

    # pos-tagger
    tagger = PosTagger()
    tagger.train(sentences_train)

    # print('tagger.data = {')
    # for k, v in tagger.data.items():
    #     print('\t' + str(k) + ': {')
    #     for k1, v1 in v.items():
    #         print('\t\t' + str(k1) + ': ' + str(v1))
    #     print('\t}')
    # print('}')

    # print('result = {')
    # for k, v in tagger.wordTag.items():
    #     print('\t' + str(k) + ': ' + str(v))
    # print('}')

    res = tagger.test(sentences_test)
    print('test:', res, ' (' + str(round( (res[0]/(res[0]+res[1]))*100, 2 )) + '%)')