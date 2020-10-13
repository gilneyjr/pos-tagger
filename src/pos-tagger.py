#!/usr/bin/python3
from parser import Parser
from preproccess import cleanData
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[ERROR]: No file was passed as argument')
        quit()

    parser = Parser()
    sentences = parser.getSentences(parser.parse(sys.argv[1]))

    # clean data
    aux = []
    for i in range(len(sentences)):
        tmp = cleanData(sentences[i])
        aux = aux + [ x for x in tmp if not x in aux]

    aux.sort()
    for x in aux:
        print(x)