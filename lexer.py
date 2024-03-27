class IJKLexer:
    def __init__(self, debug):
        self.debug = debug
        self.text = ''
        self.tokens = {}

    def splitText(self):
        ntext = []
        nline = ''
        for i in (self.text):
            nline += i
            if i == '\n' or i == ';':
                ntext.append(nline)
                nline = ''
        ntext.append(nline)
        self.text = ntext

    def splitTokens(self):
        ltext = []
        t1 = 0
        t2 = 0
        i = 0
        for token in self.text:
            if token == '|':
                self.text.pop(i)
                t1 = t2
                t2 = i
                ltext.append(self.text[t1:t2:])
            i += 1
        self.text = ltext
    def formatText(self):
        ntext = []
        for line in self.text:
            if '#' in line:
                line = line[:line.find('#')]
            if '"' in line:
                eline = ''
                isstr = False
                for i in line:
                    if i == '"':
                        isstr = not isstr
                    elif i == ' ' and not isstr:
                        i = ''
                    eline = eline + i
                line = eline
            else:
                line = line.replace(' ', '')
            line = line.replace("\n", "").replace('\t', '')
            if line != '':
                ntext.append(line)
        self.text = ntext


    def replaceDeclares(self):
        declares = {}
        dtext = []
        for line in self.text:
            if line.startswith(self.tokens['declare']):
                declares[line[line.find('>') + 1::]] = line[9:line.find(">"):]
            else:
                dtext.append(line)
        ntext = []
        if declares != {}:
            for line in dtext:
                for declare in list(declares):
                    line = line.replace(declare, declares[declare])
                ntext.append(line)
            self.text = ntext

    def fixStrings(self):
        curstr = ''
        ntext = []
        isstr = False
        for i in self.text:
            if i[0] == 'sc':
                if isstr:
                    ntext.append(['string', curstr])
                    curstr = ''
                ntext.append(['sc', '"'])
                isstr = not isstr
            elif i[0] == 'string' and isstr:
                curstr += i[1]
            elif i[0] == 'number' and isstr:
                curstr += str(i[1])
            elif isstr:
                curstr += i[1]
            else:
                ntext.append(i)
        self.text = ntext

    def tokenizeText(self):
        ntext = []
        nline = ''
        for line in self.text:
            for i in line:
                nline = nline + i
                for token in self.tokens:
                    if nline == self.tokens[token]:
                        if self.debug:
                            print('TOKEN:', token, 'LINE:', nline, '100%')
                        ntext.append([token, self.tokens[token]])
                        nline = ''
                        break
                    elif self.tokens[token] in nline:
                        if self.debug:
                            print('TOKEN:', token, 'LINE:', nline, '50%')
                        lparam = nline[:nline.find(self.tokens[token])]
                        wparam = nline[nline.find(self.tokens[token])]
                        if lparam == self.tokens[token]:
                            if self.debug:
                                print('TOKEN:', token, 'W:', lparam, '100%', 'L:', wparam, '0%')
                            ntext.append([token, self.tokens[token]])
                            try:
                                ntext.append(['number', int(wparam)])
                            except ValueError:
                                ntext.append(['string', wparam] if len(wparam) > 1 else ['char', wparam])
                        elif wparam == self.tokens[token]:
                            if self.debug:
                                print('TOKEN:', token, 'W:', lparam, '0%', 'L:', wparam, '100%')
                            try:
                                ntext.append(['number', int(lparam)])
                            except ValueError:
                                ntext.append(['string', lparam] if len(lparam) > 1 else ['char', lparam])
                            ntext.append([token, self.tokens[token]])
                        nline = ''
            nline = ''
            ntext.append('|')
        self.text = ntext

    def lex(self, text):
        if self.debug:
            print('-'*40, '\n', 'LEXER DEBUG OUTPUT', '\n', '-'*40, '\n')
        self.text = text
        if self.debug:
            print('Basic text:\n', self.text, '\n')
        self.splitText()
        if self.debug:
            print('Splitted text: ', self.text, '\n')
        self.formatText()
        if self.debug:
            print('Formatted text: ', self.text, '\n')
        self.replaceDeclares()
        if self.debug:
            print('Formatted text 2: ', self.text, '\n')
        self.tokenizeText()
        if self.debug:
            print('\nTokenized text: ', self.text, '\n')
        self.fixStrings()
        if self.debug:
            print('Fixed text: ', self.text, '\n')
        self.splitTokens()
        if self.debug:
            print('Lexed text: ', self.text, '\n')
        return self.text

    def addToken(self, tokenName, tokenValue):
        self.tokens[tokenName] = tokenValue