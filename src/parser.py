#!/usr/bin/python3
import nltk
import re
import sys

class Parser:
    def tokenize(self, file):
        # ---- Tokens--------------
        # LPAR          <- '('
        # RPAR          <- ')'
        # ID            <- [^()]+
        # -------------------------

        tokens = []
        i = 0
        j = 0
        with open(file, 'r') as f:
            i = 1
            for line in f:
                lexems = nltk.tokenize.RegexpTokenizer('\(|\)|[^ ()\n\t]+').tokenize(line)
                j = 1
                for lexem in lexems:
                    if lexem == '(':
                        tokens.append( (lexem, 'LPAR', i, j) )
                    elif lexem == ')':
                        tokens.append( (lexem, 'RPAR', i, j) )
                    elif re.match('[^()]+', lexem):
                        tokens.append( (lexem, 'ID', i, j) )
                    else: # never enter here
                        tokens.append( (lexem, 'UNK', i, j) )
                    j = j+1
                i = i+1
        tokens.append( ('<EOF>', 'EOF', i, 0) )
        return tokens

    def matchToken(self, expected_label, tokens, index):
        if tokens[index][1] != expected_label:
            print('[ERROR]: It must be a token ' + str(expected_label) + '. Got token ' + str(tokens[index][1]) + '.\n\tLine: ' + str(tokens[index][2]) + '\n\tToken Position: ' + str(tokens[index][3]) + '\n\tLexem: ' + str(tokens[index][0]))
            quit()
        return tokens[index][0], index+1

    def sentences(self, tokens, index=0):
        # sentences     <- sentence+ EOF
        i = index

        # sentences+
        sentences = []

        sentence, i = self.sentence(tokens, i)
        sentences.append(sentence)

        while tokens[i][1] == 'LPAR':
            sentence, i = self.sentence(tokens, i)
            sentences.append(sentence)

        # EOF
        _, i = self.matchToken('EOF', tokens, i)

        return ('sentences', sentences), i


    def sentence(self, tokens, index):
        # sentence      <- LPAR sentence RPAR | tree
        i = index

        # sentence      <- LPAR sentence RPAR
        if tokens[index][1] == 'LPAR' and tokens[index+1][1] != 'ID':
            # LPAR
            _, i = self.matchToken('LPAR', tokens, i)

            # tree
            tree, i = self.sentence(tokens, i)

            # RPAR
            _, i = self.matchToken('RPAR', tokens, i)

            return tree, i
        # sentence      <- tree
        else:
            # tree
            tree, i = self.tree(tokens, i)
            return tree, i

    def tree(self, tokens, index=0):
        # tree          <- LPAR tag content RPAR
        i = index

        # LPAR
        _, i = self.matchToken('LPAR', tokens, i)

        # tag
        tag, i = self.tag(tokens, i)

        # content
        content, i = self.content(tokens, i)

        # RPAR
        _, i = self.matchToken('RPAR', tokens, i)

        return ('tree', (tag, content)), i

    def content(self, tokens, index):
        # content       <- word / tree+
        # word / tree+
        if tokens[index][1] == 'ID': # word
            return self.word(tokens, index)
        elif tokens[index][1] == 'LPAR': # tree+
            i = index
            trees = []
            tree, i = self.tree(tokens, i)
            trees.append(tree)
            while tokens[i][1] == 'LPAR':
                tree, i = self.tree(tokens, i)
                trees.append(tree)
            return ('content', trees), i
        else: # Error
            self.matchToken('ID or LPAR', tokens, index)

    def tag(self, tokens, index):
        # tag           <- ID
        # ID
        id_lexem, i = self.matchToken('ID', tokens, index)
        return ('tag', id_lexem), i

    def word(self, tokens, index):
        # word          <- ID
        # ID
        id_lexem, i = self.matchToken('ID', tokens, index)
        return ('word', id_lexem), i

    def parse(self, file):
        # ---- Grammar ---------------------
        # sentences     <- sentence+ EOF
        # sentence      <- LPAR sentence RPAR | tree
        # tree          <- LPAR tag content RPAR
        # content       <- word | tree+
        # tag           <- ID
        # word          <- ID
        # ----------------------------------

        # Generating tokens
        tokens = self.tokenize(file)

        # Parsing
        ast, _ =  self.sentences(tokens)
        return ast

    def getSentences(self, ast):
        sentences = []
        if ast[0] == 'sentences':
            for tree in ast[1]:
                leaves  = []
                self.calculateSetenceLeaves(tree, leaves)
                sentences.append(leaves)
        else: # Error
            sys.stderr.write('[ERRO]: ast param has a invalid structure. Root got is \'' + str(ast[0]) + '\' instead \'sentences\'.\n')
            quit()
        return sentences
    
    def calculateSetenceLeaves(self, ast, leaves):
        if ast[0] == 'tree':
            tag = ast[1][0]
            content = ast[1][1]

            if content[0] == 'word':
                leaves.append( (tag[1], content[1]) )
            else:
                self.calculateSetenceLeaves(content, leaves)
        elif ast[0] == 'content':
            for tree in ast[1]:
                self.calculateSetenceLeaves(tree, leaves)
        else: # Error
            sys.stderr.write('[ERRO]: ast param has a invalid structure. Type got is ' + str(ast[0]))
            quit()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[ERROR]: No file was passed as argument')
        quit()

    parser = Parser()
    # print('Parsing...')
    # sys.stderr.write('Parsing...\n')
    ast = parser.parse(sys.argv[1])

    # print('Getting leaves...')
    # sys.stderr.write('Getting sentences...\n')
    for sentence in parser.getSentences(ast):
        for leaf in sentence:
            print(str(leaf[0]) + ' ' + str(leaf[1]))
        print('')